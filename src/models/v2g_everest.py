"""
Integrates v2g scheduler with EVerest simulator
Monitors charging sessions and makes v2g decisions in real-time
"""

import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime

class V2GEverest:
    def __init__(self):
        self.mqtt_broker = "localhost"
        self.mqtt_port = 1883

        self.user_profiles = self.load_user_profiles()

        self.current_session = None

        self.optimal_hours = [17, 18, 19, 20]
        self.high_value_locations = ['apartment', 'resort']

    def load_user_profiles(self):
        import pandas as pd
        try:
            profiles = pd.read_csv('data/users/processed/user_profiles_nature.csv')
            return profiles.to_dict('records')
        except:
            print("No user profiles found, using defaults")
            return []

    def should_do_v2g(self, session_data):
        current_hour = datetime.now().hour

        user_id = session_data.get('user_id', 'unknown')
        user_profiles = self.get_user_profile(user_id)

        reason = []
        score = 0

        #1st check time window
        if current_hour in self.optimal_hours:
            reasons.append(f"Peak hour ({current_hour}:00)")
            score += 40

        #2nd check: user learned patterns
        if user_profiles:
            if user_profiles.get('v2g_available', 0) > 0.05: #user has v2g history
                reasons.append("User V2G-friendly")
                score+=30

        soc = session_data.get('soc', 50)
        if soc >= 60:
            reason.append(f"SOC sufficient ({soc}%)")
            score += 20
        else:
            return False, 0, "SOC too low, need to charge"


        # user preferences (future: from learning)
        preferences = user_profiles.get('preferences', {}) if user_profiles else {}
        if preferences.get('no_v2g_today', False):
            return False, 0, "User preferences: No V2G today"

        #decision
        if score >= 70:
            #calculate v2g power
            v2g_power = -5000   #-5kW discharge
            reason = " | ".join(reasons)
            return True, v2g_power, reason
        else:
            return False, 0, "Score too low: " + " | ".join(reasons)

    #get user profile from learned data
    def get_user_profile(self, user_id):
        for profile in self.user_profiles:
            if str(profile.get('UserID')) == str(user_id):
                return profile
        return None

    #MQTT connection
    def on_connect(self, client, userdata, flags, rc):
        print(f"connected to EVerest MQTT")

        client.subscribe("everest/modules/connector_1/impl/evse/var")
        client.subscribe("everest/modules/connector_1/impl/energy_grid/var")
        print(f"subscribed to EVerest topics")

    #mqtt messages from EVerest
    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()

        data = None
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            return

        if isinstance(data, dict) and "data" in data and "evse_state" in data["data"]:
            evse_state = data["data"]["evse_state"]
            print(f"[EVSE STATE] {evse_state}")
            self.handle_evse_state(client, evse_state)
            return

    def handle_evse_state(self, client, state):
        plugged_states = [
            "PluggedIn",
            "WaitForAuth",
            "Charging",
            "ChargingPausedEV",
            "PausedEVSE"
        ]

        if state == "Unplugged":
            if self.current_session is not None:
                print("\n=== EV DISCONNECTED ===")
                self.handle_session_end()
            return

        if state in plugged_states and  self.current_session is None:
            print("\n=== EV CONNECTED ===")
            session_data = {
                "user_id": "demo_user",
                "soc": 50,
                "location": "home"
            }
            self.handle_session_start(client, session_data)

    #handle new charging sessions
    def handle_session_start(self, client, data):
        print("\n" + "="*70)
        print(f" New Charging session detected")
        print("="*70)

        self.current_session ={
            'user_id': data.get('user_id', 'unknown'),
            'start_time': datetime.now(),
            'soc': data.get('soc', 50),
            'location': data.get('location', 'unknown')
        }

        print(f"   User: {self.current_session['user_id']}")
        print(f"   SOC: {self.current_session['soc']}")
        print(f"   Time: {datetime.now().strftime('%H:%M:%S')}")

        self.evaluate_v2g_opportunity(client)

    def handle_session_update(self, client, data):
        if not self.current_session:
            return
        self.current_session['soc'] = data.get('soc', self.current_session['soc'])


    #start of adaptive scheduling
    def evaluate_v2g_opportunity(self, client):
        if not self.current_session:
            return

        print("\n Evaluating V2G opportunity....")

        decision, power_limit, reason = self.should_do_v2g(self.current_session)

        print(f"   Decision:{'V2G' if decision else 'CHARGE'}")
        print(f"   Reason: {reason}")

        if decision:
            print(f"   Power limit: {power_limit}W (negative = discharge)")
            self.send_v2g_command(client, power_limit)
        else:
            print(f"   Action: Continue normal charging")

    def send_v2g_command(self, client, power_limit):
        command = {
            "power_limit": power_limit,
            "timestamp": datetime.now().isoformat(),
            "source": "v2g_scheduler"
        }

        # publish to EVererst EnergyManager
        topic = "everest/energy_manager/set_external_limits"
        client.publish(topic, json.dumps(command))

        print(f"\n SENT V2G COMMAND TO EVEREST:")
        print(f"   Topic: {topic}")
        print(f"   Power: {power_limit}W")

        self.log_decision(command, self.current_session)

    def handle_session_end(self):
        print("\n SESSION ENDED")

        if self.current_session:
            duration = (datetime.now() - self.current_session['start_time']).total_seconds() / 3600
            print(f"   Duration: {duration:.2f} hours")
            self.learn_from_session(self.current_session, duration)
        self.current_session = None

    #for future personalization
    def learn_from_session(self, session, duration):
        #todo : update user profile based on actual behaviour
        #i will build adaptive personalization here
        pass

    #for analysis
    def log_decision(self, command, session):
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_id': session['user_id'],
            'command': command,
            'session_data': session
        }

        with open('v2g_decisions.log', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')


    def run(self):
        #start v2g scheduler
        print("Starting V2G scheduler with EVerest ")
        print("="*69)

        #MQTT client
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        try:
            client.connect(self.mqtt_broker, self.mqtt_port, 60)
            print(f"   Connected to {self.mqtt_broker}:{self.mqtt_port}")
        except Exception as e:
            print(f"   Connection failed: {e}")
            return

        print("\n  Listening for charging sessions...")
        print("   (Use Node-RED UI to simulate car plugin)")
        print("="*69)

        client.loop_forever()

# =========== USAGE ==============

if __name__ == "__main__":
    scheduler = V2GEverest()
    scheduler.run()
