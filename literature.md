# Literature Review: Smart Charging and V2G Optimization in EVerest with LLM Decision Support

Author: Isaac Adeyeye<br>
Date: September 2025<br>
Course: CP493 - Directed research - Department of Physics and Computer Science <br>
Institution: Wilfrid Laurier University<br>

## Summary
  This review examines the intersections of 
  * Smart charging optimization 
  * Vehicle-to-Grid technology
  * ISO15118 communication protocols
  * Large Language Model decision support system.<br> 
  
  Within the context of the EVerest open source framework. <br>
  
  Research gaps: Protocol aware LLM decision making, EVerest framework optimization integration (? more as i read)
  
## 1. Introduction
  The rapid adoption of Electic Vehicles presents both opportunites and challenges for power grid stability and optimization. The integration of Vehicle-to-grid technology, enabled by standardized communication protocols like ISO15118, offers potential solutions for grid balancing and energy optimization. ...(more as i read)

  This review focuses on identifying opportunities for Large Language Models to enhance decision making for EV charging systems while respecting the constraints and capabilities of the ISO15118 communication standard in the EVerest framework. 

## 2.Survey Papers
  ### Survey paper 1: ISO 15118 as the Enabler of Vehicle-to-Grid Applications
  Author: Dr. Marc Muntin<br>
  Published via: IEEE Xplore<br>
  V2G Clarity, Germany

| Aspect | Details |
|---|---|
| Problem Addressed | The lack of secure, standardized and interoperable communication protocol to enable bidirectional power flow (V2G) between electric vehicles and the grid. This survey explores how ISO15118 addresses this need, especially as it improves to support V2G applications | 
| Key Methodologies | - Detailed review of ISO15118 standard parts (1-7)<br> - Protocol stack analysis mapped to OSI layers<br> - Explanation of V2G specific message flows and cryptographic mechanisms <br> - Comparison of AC vs. DC V2G communication implications   | 
| Main Findings & Contributions | ISO15118 is foundational for enabling smart, secure EV grid integration<br> - Edition 2 introduces full bidirectional power transfer support<br> - Clarfies message exchanges for negotiation of charge/discharge parameters <br> - Distiction between on-board(AC) and off-board(DC) power converter roles<br> - Grid code compliance via parameterized communication with SECC   |
| Limitations & Open Questions | V2G capability is still limited by real world standard adoption and hardware readiness<br> - Grid codes inconsistencies |
| Relevance to Project | - Directly informs ISO15118 protocol handling inside EVerest <br>- Provides foundational understanding of ISO15118, Important for developing protocol aware optimization algorithms. <br>- Message structures and parameters like (ChargeParameterDiscovery, ACBidirectionalControlRes) give foundation for LLM based decision making |

## Citation
M. Müntin, "ISO 15118 as the Enabler of Vehicle-to-Grid Applications," V2G Clarity, Karlsruhe, Germany. Available: IEEE Xplore, Sep. 2025.

## Key insight for project
* Protocol Aware Charging Profiles: ISO 15118-2(Edition 2) supports fine-grained communication for bidirectional power transfer, enabling intelligent charging/discharging control based on real time negotiation.
* Communication timing and message sequence are critical for safe V2G operation.  Layered message formats (V2GTP, EXI/XML, TLS). Ideal structure for LLM based parsing, anomaly detection in EV charging sessions.
* AC vs DC, complexity in AC V2G due to on-board converters presents a key use case for LLMs to assist with real time compliance decisions using semantic protocol interpreation.


### Survey Paper 2: A comprehensive review of vehicle-to-grid integration in electric vehicles: Powering the future
| Aspect | Details |
|---|---|

## 3. Research Papers
### Research Paper 1: Optimizing Electric Vehicles Charging using Large Language Models and Graph Neural Networks
| Aspect | Details |
|---|---|
| Problem Addressed | Challenge of optimizing large scale, real-time EV smart charging and Vehicle-to-Grid operations in dynamic, high dimentional environments, where traditional optimization and RL approaches fail to scale effectively |
| Key Methodologies | - Combines large language models for sequence modeling with Graph Neural Networks for relational data representation<br> - Uses offline reinforcement learning(Decision Transformer) trained on mixed datasets of optimal and random policy trajectories | 
| Main Findings and Contributions | - First integration of LLMs in EV charging optimization<br> - Novel graph embedding of the EV charging ecosystem<br> - Superior performance compared to heuristics, online RL like PPO, and traditional optimization<br> - Balances user satisfaction, cost, and grid constraints violations | 
| Limitiations & Open Questions | - Does not incorporate ISO15118 protocol constaints (real time messaging delays, handshake timing or SECC-EVCC communication states)<br> - Lacks integration with the actual communication stacks or real worls EVSE/EMS setups <br> - Assumes ideal low latency environments | 
| Relevance to project | Provides architectural and algorithmic foundation for integrating LLM based decision making in EVerest. But it overlooks ISO15118 timing and protocol layer behaviour. Project can extend this incorporating protocol aware decision support ensuring LLM actions comply with ISO15118 constraints like timing, message flows and EVSE status |

## Citation
S. Orfanoudakis, P. Palensky, and P. P. Vergara, “LLM-GNN Based Optimization for EV Smart Charging,” IEEE Transactions on Smart Grid, 2025.

## Technical details
* Dataset/testbed: EV2Gym simulator with 50 charging stations, dynamic power limits, and diverse EV arrival/departure times. Offline datasets include Optimal, Random, and Mixed trajectories.
* Performance Metrics: <br>- User satisfaction(average/minimum)<br> - Power grid violations (kW)<br> - Total cost/reward
* Key results: <br> - Outperformed baseline RL (PPO): higher satisfaction, lower grid violations<br>- Strong trade-off between user needs and grid stability<br> - Combined datasets (Optimal + Random) led to most robust policy

## Implementation: 