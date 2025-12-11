#!/usr/bin/env python
# coding: utf-8

# In[20]:


"""
v2g decision engine prototype
shows how my system decides WHEN to do v2g
yes or no based on time location and battery level
"""

from datetime import datetime
import json

#simple v2g decision logic
class V2GDecisionEngine:

    def __init__(self):
        #findings from user + grid data
        self.optimal_hours = [17,18,19,20] #5-8pm
        self.charge_hours = list(range(0,15)) + [23] #earlymoring,midday,late at night (low price electricity hours)
        self.high_val_locations = ['apartment', 'resort', 'camping']
        self.min_duration = 3.0 
        self.min_soc = 60 #do not discharge battery(v2g) when below 60%

    """
    Main decision function - answers: should we do V2G now?
    returns: (decision:bool, reason: str, confidence: int)
    """
    def should_do_v2g(self, session):
        reasons = []
        score = 0

        #1st check: time window (40 points)
        if session['hour'] in self.optimal_hours:
            reasons.append(f"Optimal hour ({session['hour']}:00)")
            score +=40
        else:
            reasons.append(f"Not optimal hour ({session['hour']}:00)")
            return False, "Outside 5-8pm window", 0

        #2nd check: Duration (30 point)
        if session['duration'] >= self.min_duration:
            reasons.append(f"Long enough ({session['duration']:.1f}h)")
            score+=30
        else:
            reasons.append(f"Too short ({session['duration']:.1f}h < 3h)")
            return False, "Session too short for V2G", score

        #3rd check Location (20 points)
        if session['location'] in self.high_val_locations:
            reasons.append(f"High value location ({session['location']})")
            score+=20
        else:
            reasons.append(f"moderate location ({session['location']})")
            score+=10

        #4th check battery level
        if session['soc'] >= self.min_soc:
            reasons.append(f"Battery sufficient ({session['soc']}%)")
            score+=10
        else:
            reasons.append(f" Battery too low ({session['soc']}%)")
            return False, "Need to charge first", score

        #decision
        decision = score >= 70
        reason = " | ".join(reasons)

        return decision, reason, score

    def demo_sessions(self):
        test_sessions = [
            {
                'id': 1,
                'user': 'User1',
                'location': 'apartment',
                'hour': 18,
                'duration': 8.5,
                'soc': 75,
                'description': 'Evening apartment charger'
            },
            {
                'id': 2,
                'user': 'User69',
                'location': 'public parking lot',
                'hour':18,
                'duration': 1.2,
                'soc': 45,
                'description': 'quick public charge'
            },
            {
                'id': 1,
                'user': 'User37',
                'location': 'company',
                'hour': 9,
                'duration': 8.0,
                'soc': 80,
                'description': 'morning work charger'
            },
            {
                'id': 4,
                'user': 'User2',
                'location': 'resort',
                'hour': 19,
                'duration' : 4.5,
                'soc':70,
                'description': 'Evening resort guest'
            }
        ]

        print("\n" + "="*60)
        print("V2G decision engine demo")
        print("="*60)

        v2g_count = 0

        for session in test_sessions:
            print(f"\n   Session {session['id']}: {session['description']}")
            print(f"   Location: {session['location']}")
            print(f"   Time: {session['hour']:02d}:00")
            print(f"   Duration: {session['duration']:.1f}h")
            print(f"   SOC: {session['soc']}%")

            decision, reason, score = self.should_do_v2g(session)

            print(f"\n Decision: {'DO V2G' if decision else 'SKIP'} (Score: {score}/100)")
            print(f" Reason: {reason}")

            if decision:
                v2g_count +=1

        print(f"\n" + "="*60)
        print(f"   RESULTS: {v2g_count}/{len(test_sessions)} sessions selected for V2G")
        print(f"   Selection rate: {v2g_count/len(test_sessions)*100:.1f}%")
        print("="*60)

if __name__ == "__main__":
    engine = V2GDecisionEngine()
    engine.demo_sessions()


# In[ ]:





# In[ ]:




