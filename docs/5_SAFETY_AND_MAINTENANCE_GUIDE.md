# Auto Sage KBS — 5. Safety Protocols & Maintenance Engineering Guide

**Course:** Knowledge-Based Systems (CT-359)  
**Project:** Auto Sage — Intelligent Automotive Fault Diagnosis System  

---

## 1. Safety-Critical Automotive Triage Philosophy

Vehicle diagnostics is inherently safety-critical. A misdiagnosis in a domestic home appliance may cause minor inconvenience, but a faulty diagnosis in an automotive braking, steering, or high-voltage circuit can lead to catastrophic collisions or thermal runaway.

Auto Sage enforces three non-negotiable safety principles:
1. **Never Replace Components on Software Advice Alone:** Software inference isolates *hypotheses*; physical measurement tools (multimeters, pressure gauges, micrometer calipers) confirm *reality*.
2. **Mandatory Bench Verification Before Disassembly:** Every rule defines a structured **Tier A Verification Check** table with quantitative pass/fail thresholds.
3. **Explicit Anti-Mistake Directives:** Every rule defines a **Do-Not-Replace Directive** warning users against premature, costly component swaps.

---

## 2. Safety Risk Stratification Matrix

Every fault candidate and diagnostic session is classified into one of four standardized risk levels:

| Risk Level | Visual Indicator | Criteria | Mandatory Action Protocol |
| :--- | :--- | :--- | :--- |
| **Critical** | Red (`CRITICAL SAFETY`) | Failure causes immediate loss of vehicle control, total brake failure, fuel fire, or high-voltage electric shock hazard. | **Cease driving immediately.** Escalate to certified workshop via flatbed tow truck. Do not attempt roadside trial-and-error. |
| **High** | Orange (`HIGH RISK`) | Failure compromises engine integrity, transmission lockup, severe overheating, or sudden stalling in traffic. | Drive with extreme caution only to nearest service bay ($< 10\text{ km}$). Cease operation if temperature warning triggers. |
| **Medium** | Yellow (`MODERATE RISK`) | Impaired efficiency, rough idle, abnormal noise, suspension wear, or reduced HVAC cooling capacity. | Safe for short-term local operation; schedule workshop inspection within 500 km to prevent secondary component damage. |
| **Low** | Blue / Slate (`LOW RISK`) | Minor cosmetic, accessory, sensor calibration, or minor emissions evap leak without drivability impact. | Inspect during regular scheduled vehicle maintenance service. |

---

## 3. Tier A: Physical Verification Check Protocols

Tier A checks bridge the gap between abstract symptom reporting and mechanical reality. Technicians must perform these tests sequentially:

### Example 1: Braking System — Brake Booster Vacuum Decay Test
- **Target Component:** Vacuum Brake Power Booster & Check Valve Assembly
- **Required Tools:** Vacuum Gauge (0–30 in-Hg), Hand Vacuum Pump
- **Required Expertise:** Certified Brake Technician
- **Step 1:** Disconnect vacuum supply line at booster check valve; connect vacuum gauge in series. Start engine and idle.
  - *Normal Reading:* Steady 18 to 22 in-Hg manifold vacuum.
  - *Abnormal Finding:* $< 16\text{ in-Hg}$ or erratic needle oscillation (indicates engine vacuum leak or obstructed line).
- **Step 2:** Shut off engine. Monitor vacuum gauge for 60 seconds without touching brake pedal.
  - *Normal Reading:* Vacuum drop $< 2\text{ in-Hg}$ in 60 seconds.
  - *Abnormal Finding:* Rapid vacuum decay to zero (confirms booster check valve seal failure or internal diaphragm rupture).

### Example 2: Electrical System — Starter Circuit Voltage Drop Test
- **Target Component:** Starter Solenoid & Heavy Current Cable Harness
- **Required Tools:** Digital Multimeter (CAT III), Remote Starter Switch
- **Required Expertise:** Automotive Electrical Specialist
- **Step 1:** Connect positive DMM lead to battery positive post; connect negative lead to starter B+ terminal. Crank engine for 5 seconds.
  - *Normal Reading:* Voltage drop across positive cable $< 0.2\text{V DC}$.
  - *Abnormal Finding:* Voltage drop $> 0.5\text{V DC}$ (indicates high-resistance corroded terminal or damaged cable strand; do not replace starter!).
- **Step 2:** Connect negative DMM lead to starter metal casing; connect positive lead to battery negative post. Crank engine.
  - *Normal Reading:* Ground circuit voltage drop $< 0.2\text{V DC}$.
  - *Abnormal Finding:* Voltage drop $> 0.3\text{V DC}$ (indicates corroded engine-to-chassis ground strap).

---

## 4. Tier B: Structured Maintenance Directives

Once physical checks confirm a fault, Auto Sage prescribes structured Tier B directives:

### 1. Corrective Action
Defines the exact technical procedure to rectify the identified mechanical defect in accordance with OEM workshop service manuals.

### 2. Preventive Measure
Prescribes scheduled maintenance routines (fluid flushes, hose inspections, torque checks) to prevent recurrence of the failure.

### 3. Objective Replacement Criteria
Establishes measurable physical wear limits before a component is discarded. Examples:
- *Brake Rotor:* Replace if thickness is less than minimum cast discard spec (e.g. $< 22.0\text{ mm}$) or if lateral runout exceeds $0.05\text{ mm}$ ($0.002\text{ inches}$).
- *Brake Pad:* Replace if friction lining thickness $< 3.0\text{ mm}$.
- *Coolant:* Replace if pH drops below 7.0 or if freeze protection point rises above $-25^\circ\text{C}$.

### 4. Do-Not-Replace Directives (Anti-Mistake Engineering)
The most common mistake in automotive repair is replacing an expensive actuator or sensor when the fault was caused by a dirty connector, blown fuse, or vacuum leak:

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    CRITICAL DO-NOT-REPLACE DIRECTIVE                       │
├────────────────────────────────────────────────────────────────────────────┤
│ "Do NOT replace the alternator if battery charging voltage is below 13.5V  │
│  until you have verified alternator drive belt tension and measured less   │
│  than 0.2V voltage drop across the alternator B+ output cable!"           │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Workshop Escalation Thresholds

Auto Sage explicitly instructs users to cease DIY procedures and escalate to an **ASE Master Technician** under the following critical conditions:
1. **Hydraulic Internal Bypass:** If brake pedal slowly sinks to floorboard under steady foot pressure at stoplights (internal master cylinder seal failure).
2. **Coolant System Pressurization:** If radiator hoses become rock-hard immediately after cold startup (combustion gas intrusion via blown head gasket or cracked cylinder block).
3. **Metallic Contamination:** If metallic shavings or bronze glitter are detected in drained engine oil or transmission pan (imminent bearing seizure).
4. **High-Voltage Isolation Loss:** Any DTC or warning indicator on 400V/800V hybrid or electric vehicle traction circuits.
