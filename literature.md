# Literature Review: Smart Charging and V2G Optimization in EVerest with LLM Decision Support
Research Focus: Identifying opportunities for Large Language Models to enhance decision making in EV charging systems while respecting the constraints and capabilities of the ISO15118 communication standard in the EVerest framework.

Author: Isaac Adeyeye<br>
Date: September 2025<br>
Course: CP493 - Directed research - Department of Physics and Computer Science <br>
Institution: Wilfrid Laurier University<br>

## 1. Summary
  This review examines the intersections of 
  * Smart charging optimization 
  * Vehicle-to-Grid technology
  * ISO15118 communication protocols
  * Large Language Model decision support system.<br> 
  
  Within the context of the EVerest open source framework. <br>
  
  Research gaps: Protocol aware LLM decision making, EVerest framework optimization integration (? more as i read)
  
## 2. Introduction
  The rapid adoption of Electic Vehicles presents both opportunites and challenges for power grid stability and optimization. The integration of Vehicle-to-grid technology, enabled by standardized communication protocols like ISO15118, offers potential solutions for grid balancing and energy optimization. ...(more as i read)

## 3.Survey Papers
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

## 3. Research Papers