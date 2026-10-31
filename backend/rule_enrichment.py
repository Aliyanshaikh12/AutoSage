"""Auto Sage - Domain Knowledge Enrichment for all 93 Automotive Rules.

This module provides verified automotive engineering metadata for every rule:
- affected_component: Exact mechanical / electrical component
- subsystem: Subsystem classification within category
- safety_level: Critical, High, Medium, Low
- required_expertise: Vehicle Owner, General Mechanic, Experienced Tech, Professional Specialist
- required_tools: List of physical bench & diagnostic tools
- maintenance_actions: Corrective action, preventive maintenance, replacement criteria, warnings
- diagnostic_questions: Dynamic follow-up questions for symptom verification & contradiction detection
- contradictory_evidence: Evidence that contradicts / rules out this fault candidate
"""

from __future__ import annotations
from typing import Any

RULE_ENRICHMENT_BY_SUBCATEGORY: dict[str, dict[str, Any]] = {
    "ABS Control Module": {
        "affected_component": "Anti-Lock Braking System (ABS) Electronic Control Unit & Hydraulic Block",
        "subsystem": "Anti-Lock Brake Electronics & Hydraulics",
        "safety_level": "Critical",
        "required_expertise": "Professional Automotive Technician / ASE Specialist",
        "required_tools": [
            "Dedicated OBD-II / ABS Diagnostic Scanner",
            "Digital Multimeter (CAT III)",
            "Wiring Harness Back-Probes"
        ],
        "maintenance_actions": {
            "corrective_action": "Inspect ABS power fuse and relay. Test harness ground and CAN bus continuity. If internal solenoid valve or microprocessor fault is confirmed by scan, replace ABS module and pressure-bleed system.",
            "preventive_maintenance": "Flush brake fluid every 2 years / 40,000 km to prevent moisture accumulation and solenoid corrosion in the ABS valve body.",
            "replacement_criteria": "Replace only if scanner confirms internal open/short in module solenoids or power driver circuit, with external wiring verified intact.",
            "do_not_replace_warning": "Do not replace the ABS module without first checking the ABS power fuse, chassis ground connection, and wheel speed sensor signals."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_BRK_ABS_FUSE",
                "question": "Did the ABS warning light illuminate immediately when the vehicle was turned on, before moving?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "A fault light at startup before vehicle motion points to power, ground, or module self-test failure rather than a wheel sensor pulse issue."
            },
            {
                "question_id": "Q_BRK_ABS_PULSE_DRY",
                "question": "Does the brake pedal pulsate or chatter on dry, non-slippery pavement under light braking?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Inappropriate ABS activation on dry pavement indicates false wheel speed signals or erratic control module command."
            }
        ],
        "contradictory_evidence": [
            "ABS warning light turns off after startup self-test and stays off",
            "Braking is smooth with zero pedal kickback on dry pavement"
        ]
    },
    "ABS Wheel Speed Sensor": {
        "affected_component": "Wheel Speed Reluctor Sensor & Tone Ring Assembly",
        "subsystem": "ABS Wheel Speed Sensing",
        "safety_level": "High",
        "required_expertise": "Experienced Technician or Well-Equipped DIYer",
        "required_tools": [
            "Digital Multimeter (AC Volts / Frequency / Ohms)",
            "Automotive Oscilloscope (optional)",
            "Jack and Rated Axle Stands"
        ],
        "maintenance_actions": {
            "corrective_action": "Inspect sensor harness for chafing or cut wires. Clean metallic debris from magnetic sensor tip and tone ring teeth. If sensor coil is open or hall sensor output is dead, replace wheel speed sensor.",
            "preventive_maintenance": "Inspect sensor wiring routing during tire rotations and brake pad replacements.",
            "replacement_criteria": "Replace if sensor resistance is out of factory specification (typically 800-1400 ohms for passive, or no square-wave pulse on active sensors).",
            "do_not_replace_warning": "Do not replace the sensor until inspecting the reluctor tone ring for cracked teeth, rust build-up, or excessive air gap."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_BRK_WSS_SPEED",
                "question": "Does the ABS light turn on only after the vehicle exceeds 15-20 km/h (10-15 mph)?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Wheel speed sensor signal loss faults typically trigger once the vehicle begins rolling and the ECU detects a missing frequency pulse."
            }
        ],
        "contradictory_evidence": [
            "ABS light never triggers during driving",
            "All 4 wheel speeds read identically on live scanner data"
        ]
    },
    "Brake Booster": {
        "affected_component": "Vacuum Brake Power Booster & Check Valve Assembly",
        "subsystem": "Brake Power Assist System",
        "safety_level": "Critical",
        "required_expertise": "Professional Automotive Technician / ASE Specialist",
        "required_tools": [
            "Handheld Vacuum Pump with Gauge (0-30 in-Hg)",
            "Tee Fitting and Vacuum Hose",
            "Metric Wrench Set"
        ],
        "maintenance_actions": {
            "corrective_action": "Inspect vacuum supply line from intake manifold for cracks, oil contamination, or collapse. Test one-way check valve operation. If booster diaphragm leaks vacuum internally, replace brake booster unit.",
            "preventive_maintenance": "Inspect rubber vacuum supply hose for softness, hardening, or engine oil ingress during major services.",
            "replacement_criteria": "Replace booster if it fails the pedal-drop holding test (pedal does not drop when engine starts, or hisses continuously during application).",
            "do_not_replace_warning": "Do not replace the brake booster without first confirming engine manifold vacuum supply (at least 16-20 in-Hg at idle) and check valve integrity."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_BRK_BOOSTER_START",
                "question": "When pressing the brake pedal before starting the engine, does the pedal drop down slightly once the engine starts running?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "No",
                "contradictory_answer": "Yes",
                "context": "Normal brake boosters draw vacuum on engine start, pulling the pedal down slightly; failure to drop indicates vacuum assist loss."
            },
            {
                "question_id": "Q_BRK_BOOSTER_HISS",
                "question": "Do you hear a continuous hissing sound from underneath the driver dashboard when you press or release the brake pedal?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "A hissing noise inside the cabin near the pedals indicates a ruptured internal booster rubber diaphragm leaking atmospheric air."
            }
        ],
        "contradictory_evidence": [
            "Brake pedal drops smoothly when engine starts",
            "Pedal effort is light and responsive with normal power assist"
        ]
    },
    "Brake Caliper": {
        "affected_component": "Hydraulic Disc Brake Caliper & Slider Pins Assembly",
        "subsystem": "Hydraulic Foundation Brakes",
        "safety_level": "Critical",
        "required_expertise": "Experienced Technician or Well-Equipped DIYer",
        "required_tools": [
            "Brake Caliper Piston Press Tool",
            "Torque Wrench",
            "Brake Line Clamp / Fluid Catch Pan",
            "Silicone Brake Grease"
        ],
        "maintenance_actions": {
            "corrective_action": "Inspect caliper guide slider pins for corrosion and seize-up. Check piston dust boot for tears and hydraulic leaks. Re-grease slider pins or replace seized caliper assembly, followed by hydraulic system bleeding.",
            "preventive_maintenance": "Clean and lubricate guide pins with high-temperature silicone ceramic brake grease at every pad replacement.",
            "replacement_criteria": "Replace caliper if piston is frozen in the bore, piston chrome is pitted, or fluid leaks past the internal square-cut seal.",
            "do_not_replace_warning": "Do not replace caliper for uneven pad wear until checking if slider pins are simply dry or sticking in their rubber boots."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_BRK_CALIPER_PULL",
                "question": "Does the vehicle consistently pull to one side when you brake, or does one wheel rim feel noticeably hotter than the others after driving?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "A seized caliper piston or guide pin keeps brake pads dragging, generating excessive wheel heat and steering pull."
            }
        ],
        "contradictory_evidence": [
            "Vehicle stops straight with hands lightly touching wheel",
            "All wheel hubs remain at identical moderate temperature after driving"
        ]
    },
    "Brake Hose": {
        "affected_component": "Flexible Hydraulic Reinforced Brake Hose",
        "subsystem": "Hydraulic Foundation Brakes",
        "safety_level": "Critical",
        "required_expertise": "Professional Automotive Technician / ASE Specialist",
        "required_tools": [
            "Flare Nut Line Wrenches (10mm/11mm)",
            "Brake Pressure Bleeder",
            "Clean DOT 3/DOT 4 Fluid Catch Container"
        ],
        "maintenance_actions": {
            "corrective_action": "Inspect rubber exterior for cracking, chafing, blistering, or fluid seepage under pressure. If internal hose layer collapses (acting as a one-way check valve) or leaks externally, replace flexible hose immediately.",
            "preventive_maintenance": "Replace flexible rubber brake hoses every 6-8 years or whenever deep weather-checking cracks appear.",
            "replacement_criteria": "Replace immediately if any external bulge, wetness, or deep cracking is visible.",
            "do_not_replace_warning": "Always use a flare-nut wrench on hydraulic fittings to prevent rounding soft steel brake line nuts."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_BRK_HOSE_BULGE",
                "question": "Does an assistant notice any ballooning or expansion along the flexible rubber brake hose when the pedal is pressed hard?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Internal cord failure causes hydraulic pressure to balloon the hose outward instead of clamping the brake pads."
            }
        ],
        "contradictory_evidence": [
            "Hoses are smooth, flexible, dry, and show zero expansion under heavy pedal pressure"
        ]
    },
    "Brake Master Cylinder": {
        "affected_component": "Tandem Hydraulic Brake Master Cylinder & Fluid Reservoir",
        "subsystem": "Hydraulic Brake Pressure Generation",
        "safety_level": "Critical",
        "required_expertise": "Professional Automotive Technician / ASE Specialist",
        "required_tools": [
            "Bench Bleeding Kit",
            "Flare Nut Wrenches",
            "Brake Fluid Moisture Tester"
        ],
        "maintenance_actions": {
            "corrective_action": "Check for external fluid seepage between master cylinder rear and booster face. Test for internal primary/secondary cup bypass. If pedal slowly sinks to floor under steady pressure, bench-bleed and install new master cylinder.",
            "preventive_maintenance": "Flush hydraulic fluid every 2 years to prevent moisture pitting in the aluminum cylinder bore.",
            "replacement_criteria": "Replace if pedal sinks slowly to the floorboard at stoplights while no external fluid leaks are found anywhere in the vehicle.",
            "do_not_replace_warning": "Ensure all 4 calipers and wheel cylinders are thoroughly bled of air bubbles before condemning the master cylinder."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_BRK_MC_SINK",
                "question": "While waiting at a red traffic light with your foot steadily on the brake pedal, does the pedal slowly creep or sink towards the floorboard?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Internal bypass of master cylinder piston seals allows high-pressure fluid to leak back into the low-pressure reservoir, causing pedal creep."
            }
        ],
        "contradictory_evidence": [
            "Brake pedal holds firm height indefinitely under constant foot pressure"
        ]
    },
    "Brake Pad": {
        "affected_component": "Semi-Metallic or Ceramic Disc Brake Friction Pads",
        "subsystem": "Hydraulic Foundation Brakes",
        "safety_level": "High",
        "required_expertise": "General Mechanic or Intermediate DIYer",
        "required_tools": [
            "Brake Lining Thickness Gauge",
            "Wheel Lug Wrench",
            "Floor Jack & Axle Stands",
            "C-Clamp / Piston Retractor"
        ],
        "maintenance_actions": {
            "corrective_action": "Measure remaining friction material thickness. Replace brake pads as an axle set (both left and right sides) if lining is below 3 mm. Clean caliper bracket slides and replace anti-rattle hardware clips.",
            "preventive_maintenance": "Inspect pad thickness at every oil change / 10,000 km tire rotation interval.",
            "replacement_criteria": "Mandatory replacement if lining is under 2 mm (0.08 in) or acoustic wear indicator squeals.",
            "do_not_replace_warning": "Never replace pads on only one wheel; always replace complete axle sets to maintain balanced braking."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_BRK_PAD_SQUEAL",
                "question": "Does a high-pitched metallic squealing sound occur during light braking, which stops when you release the brake pedal?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Mechanical acoustic wear indicators are spring-steel tabs designed to contact the rotor and squeal when pad lining drops below 3 mm."
            }
        ],
        "contradictory_evidence": [
            "Brake pad friction material measures greater than 6 mm with zero squealing"
        ]
    },
    "Brake Rotor": {
        "affected_component": "Cast Iron Ventilated or Solid Brake Disc Rotor",
        "subsystem": "Hydraulic Foundation Brakes",
        "safety_level": "High",
        "required_expertise": "Experienced Technician or Well-Equipped DIYer",
        "required_tools": [
            "Micrometer / Vernier Caliper",
            "Dial Indicator with Magnetic Base",
            "Impact Driver for Rotor Retaining Screws"
        ],
        "maintenance_actions": {
            "corrective_action": "Measure rotor thickness and lateral runout with dial indicator. Machine rotor if thickness exceeds minimum 'discard' specification stamped on rotor edge; otherwise install new balanced rotors in axle pairs.",
            "preventive_maintenance": "Torque wheel lug nuts in a star pattern with a calibrated torque wrench to prevent rotor warpage.",
            "replacement_criteria": "Replace if measured thickness is at or below the manufacturer discard minimum, or if deep thermal heat cracks / scoring grooves exceed 1.5 mm.",
            "do_not_replace_warning": "Do not machine or turn rotors that are already near discard minimum thickness, as thin rotors overheat and warp rapidly."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_BRK_ROTOR_SHAKE",
                "question": "Does the steering wheel or brake pedal violently shake or pulsate specifically when braking from highway speeds (80-100 km/h)?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Lateral runout or disc thickness variation (DTV) causes high-speed pedal kickback and steering oscillation under braking."
            }
        ],
        "contradictory_evidence": [
            "High-speed braking is smooth with zero pedal pulsation or steering vibration"
        ]
    },
    "Brake Shoe & Drum": {
        "affected_component": "Rear Drum Brake Friction Shoes, Return Springs & Wheel Cylinders",
        "subsystem": "Rear Drum Foundation Brakes",
        "safety_level": "High",
        "required_expertise": "Experienced Technician or Well-Equipped DIYer",
        "required_tools": [
            "Brake Drum Spring Pliers and Retaining Tool",
            "Brake Drum Micrometer",
            "Brake Cleaner & Drain Pan"
        ],
        "maintenance_actions": {
            "corrective_action": "Remove drum and inspect brake shoes for contamination from leaking wheel cylinders. Inspect return spring tension and auto-adjuster mechanism. Replace shoes and drum hardware; machine or replace drums.",
            "preventive_maintenance": "Inspect and clean rear drum brake assemblies every 40,000 km; check parking brake cable tension.",
            "replacement_criteria": "Replace shoes if lining thickness is under 1.5 mm or contaminated with brake fluid/axle oil.",
            "do_not_replace_warning": "Always clean drum components with dedicated brake cleaner; never use compressed air on brake dust."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_BRK_DRUM_GRIND",
                "question": "Do you hear a scraping or grinding noise specifically from the rear wheels when coming to a complete stop?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Worn rear drum shoes allow metal-to-metal contact between shoe backing tables and drum friction surfaces."
            }
        ],
        "contradictory_evidence": [
            "Rear brake shoes have adequate lining and drum surface is clean and smooth"
        ]
    },
    "Brake Fluid": {
        "affected_component": "Hygroscopic Glycol-Ether Hydraulic Brake Fluid (DOT 3 / DOT 4)",
        "subsystem": "Hydraulic Brake Fluid System",
        "safety_level": "Critical",
        "required_expertise": "General Mechanic or Intermediate DIYer",
        "required_tools": [
            "Electronic Brake Fluid Moisture Tester (or Test Strips)",
            "Hydraulic Vacuum Bleeder Kit",
            "Fresh Sealed Brake Fluid Bottle"
        ],
        "maintenance_actions": {
            "corrective_action": "Inspect master cylinder reservoir fluid level and color. If fluid is black/dark green or moisture content exceeds 3%, perform complete 4-wheel pressure flush until crystal clear fluid emerges from all bleeder screws.",
            "preventive_maintenance": "Flush and replace brake fluid every 2 years / 40,000 km regardless of vehicle mileage.",
            "replacement_criteria": "Flush immediately if moisture tester indicates greater than 3% water boiling point reduction or dark sludge is present.",
            "do_not_replace_warning": "Never use brake fluid from an open container that has sat on a shelf, as brake fluid rapidly absorbs atmospheric humidity."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_BRK_FLUID_LEVEL",
                "question": "Is the brake fluid level in the under-hood clear plastic reservoir sitting below the MIN line?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Low brake fluid indicates either worn friction pads or an active external hydraulic leak that must be identified."
            }
        ],
        "contradictory_evidence": [
            "Brake fluid is light amber/clear, test shows <1% moisture, and reservoir is at MAX line"
        ]
    },
    "Coolant/Antifreeze": {
        "affected_component": "Ethylene Glycol / Organic Acid Technology (OAT) Engine Coolant Mixture",
        "subsystem": "Engine Thermal Management System",
        "safety_level": "High",
        "required_expertise": "General Mechanic or Intermediate DIYer",
        "required_tools": [
            "Coolant Optical Refractometer / Hydrometer",
            "Cooling System Pressure Tester (0-30 psi)",
            "Drain Pan"
        ],
        "maintenance_actions": {
            "corrective_action": "Test freeze point and pH of coolant. Pressure-test cooling system to 15 psi to pinpoint active leaks. Drain, flush, and refill with 50/50 distilled water and OEM-specified antifreeze mix.",
            "preventive_maintenance": "Drain and refill coolant every 5 years / 100,000 km (or per manufacturer OAT schedule).",
            "replacement_criteria": "Replace coolant if pH drops below 7.0 (acidic) or refractometer indicates freeze protection weaker than -25°C.",
            "do_not_replace_warning": "THERMAL BURN HAZARD: Never open radiator or pressurized expansion tank cap while engine temperature is above ambient."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_COOL_PUDDLE",
                "question": "Do you see bright green, orange, or pink sweet-smelling fluid puddled under the front of your car after parking?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Bright colored fluid with a maple-syrup sweet odor indicates active external ethylene glycol coolant leakage."
            }
        ],
        "contradictory_evidence": [
            "Coolant level is stable at MAX line and refractometer reads exactly 50/50 concentration"
        ]
    },
    "Engine Cooling System": {
        "affected_component": "Engine Coolant Thermostat & Spring-Loaded Bypass Valve Housing",
        "subsystem": "Engine Temperature Regulation",
        "safety_level": "High",
        "required_expertise": "Experienced Technician or Well-Equipped DIYer",
        "required_tools": [
            "Infrared Thermometer Gun",
            "Thermostat Housing Gasket Scraper",
            "Cooling System Refill Funnel"
        ],
        "maintenance_actions": {
            "corrective_action": "Check upper and lower radiator hose temperature delta with infrared thermometer. If upper hose remains cold while engine overheats, thermostat is stuck closed. Replace thermostat and housing gasket.",
            "preventive_maintenance": "Replace thermostat whenever replacing water pump or during major cooling overhaul.",
            "replacement_criteria": "Replace if thermostat fails to open at stamped rated temperature (typically 82°C-90°C / 180°F-195°F) in boiling water test.",
            "do_not_replace_warning": "Ensure air pockets are thoroughly bled from cooling system before condemning a new thermostat."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_COOL_THERMO_HEAT",
                "question": "Does the engine overheat within 10-15 minutes of driving, while the cabin heater blows completely cold air?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "A stuck-closed thermostat or air-lock blocks coolant circulation, causing severe cylinder head overheating and cold heater vents."
            }
        ],
        "contradictory_evidence": [
            "Upper and lower radiator hoses both reach balanced operating temperature (85-92°C) smoothly"
        ]
    },
    "Heater Core": {
        "affected_component": "Cabin HVAC Heater Core Heat Exchanger",
        "subsystem": "Cabin Climate & Defrosting System",
        "safety_level": "Medium",
        "required_expertise": "Professional Automotive Technician / ASE Specialist",
        "required_tools": [
            "Cooling System Pressure Tester",
            "Bypass Hose Connector (5/8 in / 3/4 in)",
            "Interior Trim Removal Tools"
        ],
        "maintenance_actions": {
            "corrective_action": "Inspect passenger front footwell carpet for dampness and sweet coolant odor. Check windshield for greasy interior fogging. Replace leaking heater core (or temporarily bypass heater hoses in emergency).",
            "preventive_maintenance": "Keep cooling system corrosion inhibitors fresh by flushing coolant on schedule.",
            "replacement_criteria": "Replace if cabin floor carpet is saturated with coolant or pressure tester reveals pressure loss under dashboard.",
            "do_not_replace_warning": "Verify heater core inlet and outlet hoses are both hot before tearing down dashboard for a 'no heat' symptom (blend door may be stuck)."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_COOL_HEATER_FOG",
                "question": "When turning on the windshield defroster, does a sweet-smelling oily film or dense fog coat the inside of the front windshield?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Atomized coolant leaking from pinholes in the heater core vaporizes directly into the defroster air stream."
            }
        ],
        "contradictory_evidence": [
            "Passenger floor carpet is dry and windshield defroster blows clean, dry, odor-free air"
        ]
    },
    "Heater Hose": {
        "affected_component": "Reinforced EPDM Rubber Heater Inlet and Return Hoses",
        "subsystem": "Cabin Heating Fluid Circuit",
        "safety_level": "High",
        "required_expertise": "General Mechanic or Intermediate DIYer",
        "required_tools": [
            "Hose Clamp Pliers",
            "Hose Removal Pick",
            "Coolant Catch Pan"
        ],
        "maintenance_actions": {
            "corrective_action": "Squeeze heater hoses along their length to check for soft spongy spots, hardening, or swelling near firewall clamps. Replace swollen or leaking heater hoses and install fresh constant-tension clamps.",
            "preventive_maintenance": "Inspect heater hoses every 2 years; replace proactively at 100,000 km.",
            "replacement_criteria": "Replace if hose wall exhibits oil softening, dry-rot cracking, or bulging under pressure.",
            "do_not_replace_warning": "Be careful when removing stubborn hoses from plastic heater core nipples at the firewall to avoid cracking the heater core."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_COOL_HEATER_HOSE_SOFT",
                "question": "Are the rubber hoses running into the cabin firewall soft, spongy, or swollen near the clamp connections?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Electrochemical degradation (ECD) attacks rubber coolant hoses from the inside out, causing soft spots prone to sudden bursting."
            }
        ],
        "contradictory_evidence": [
            "Heater hoses are firm, flexible, free of oil contamination, and show zero clamp weeping"
        ]
    },
    "Radiator/Cooling Fan": {
        "affected_component": "Electric Radiator Cooling Fan Motor, Shroud & Controller Relay",
        "subsystem": "Forced Air Cooling System",
        "safety_level": "High",
        "required_expertise": "Experienced Technician or Well-Equipped DIYer",
        "required_tools": [
            "Digital Multimeter (12V DC test)",
            "Fused Jumper Wire (20A)",
            "Scan Tool Active Command"
        ],
        "maintenance_actions": {
            "corrective_action": "Check fan fuse and relay. Command fan on with scan tool or jumper 12V directly to fan motor harness. If motor does not spin or bearing squeals, replace electric fan assembly.",
            "preventive_maintenance": "Verify radiator fan engages automatically whenever the vehicle AC compressor is switched on.",
            "replacement_criteria": "Replace fan assembly if motor draws excessive amperage (blows fuse), has high internal resistance, or motor shaft is seized.",
            "do_not_replace_warning": "Verify engine coolant temperature sensor (ECT) reading before replacing fan motor, as a bad sensor will not trigger the fan relay."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_COOL_FAN_SPIN",
                "question": "When the engine temperature gauge climbs above the middle mark while idling at a standstill, does the electric radiator fan fail to spin?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Inoperative cooling fans cause overheating specifically in stop-and-go traffic or at idle, while highway airflow keeps temperatures normal."
            }
        ],
        "contradictory_evidence": [
            "Radiator cooling fan cycles on with high airflow when AC is activated or engine reaches 95°C"
        ]
    },
    "Radiator Hose": {
        "affected_component": "Upper and Lower Molded EPDM Radiator Coolant Hoses",
        "subsystem": "Primary Engine Heat Exchange Circuit",
        "safety_level": "High",
        "required_expertise": "General Mechanic or Intermediate DIYer",
        "required_tools": [
            "Spring Clamp Pliers",
            "Drain Pan",
            "Coolant Funnel"
        ],
        "maintenance_actions": {
            "corrective_action": "Inspect upper and lower radiator hoses for bulging, softening from engine oil leaks, or pinhole spray. Replace damaged hoses, clean radiator neck, and refill/bleed cooling system.",
            "preventive_maintenance": "Replace upper and lower radiator hoses every 5 years or 100,000 km.",
            "replacement_criteria": "Replace immediately if hose collapses flat when revving engine (internal spring missing) or exhibits weather cracking.",
            "do_not_replace_warning": "Ensure the hose clamp is positioned behind the raised retaining bead on the radiator inlet/outlet pipe."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_COOL_RAD_HOSE_COLLAPSE",
                "question": "Does the lower radiator hose collapse or pinch completely shut when the engine is revved or cooling down?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "A defective radiator cap vacuum valve or weakened hose wall causes atmospheric collapse, restricting water pump suction."
            }
        ],
        "contradictory_evidence": [
            "Radiator hoses maintain circular cross-section under all operating conditions with zero bulging"
        ]
    },
    "Water Pump": {
        "affected_component": "Centrifugal Mechanical Engine Water Pump & Impeller Assembly",
        "subsystem": "Engine Coolant Circulation",
        "safety_level": "High",
        "required_expertise": "Professional Automotive Technician / ASE Specialist",
        "required_tools": [
            "Mechanic's Stethoscope",
            "Pulley Holding Tool",
            "Torque Wrench",
            "RTV / Gasket Sealant"
        ],
        "maintenance_actions": {
            "corrective_action": "Inspect weep hole on water pump casting for dried coolant residue. Check water pump pulley for shaft play and grinding noise. Replace water pump, gasket, and drive belt.",
            "preventive_maintenance": "Replace timing belt-driven water pumps during scheduled timing belt replacements (every 100,000-150,000 km).",
            "replacement_criteria": "Replace if coolant drips from weep hole, shaft bearing has lateral play > 1 mm, or plastic impeller has separated from shaft.",
            "do_not_replace_warning": "A faint trace of dry discoloration around weep hole is normal venting; active dripping confirms mechanical seal failure."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_COOL_WPUMP_NOISE",
                "question": "Do you hear a loud rumbling, roaring, or squealing bearing noise from the front of the engine that rises with RPM?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Water pump shaft bearings rumble when coolant leaks past the internal ceramic seal and washes out bearing grease."
            }
        ],
        "contradictory_evidence": [
            "Water pump weep hole is bone-dry and pulley spins smoothly with zero wobble or bearing roughness"
        ]
    },
    "Coolant Reservoir": {
        "affected_component": "Pressurized Coolant Expansion Tank & Spring-Loaded Pressure Cap",
        "subsystem": "Cooling System Pressure & Expansion Storage",
        "safety_level": "Medium",
        "required_expertise": "Basic DIY / Vehicle Owner",
        "required_tools": [
            "Radiator Cap Pressure Adapter",
            "Cooling System Pressure Tester"
        ],
        "maintenance_actions": {
            "corrective_action": "Inspect plastic reservoir for stress hairline cracks and neck deformation. Pressure-test expansion cap release pressure (typically 14-18 psi / 1.1-1.3 bar). Replace cracked tank or defective cap.",
            "preventive_maintenance": "Inspect expansion tank plastic for yellowing, brittleness, and sludge accumulation every year.",
            "replacement_criteria": "Replace tank if plastic has turned dark/brittle or leaks at seams. Replace cap if it fails to hold rated relief pressure.",
            "do_not_replace_warning": "Never use an aftermarket cap with incorrect pressure rating; too low causes boil-over, too high risks radiator burst."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_COOL_RES_BOIL",
                "question": "Does coolant actively boil and violently overflow out of the reservoir neck after shutting off the engine?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "A weak pressure cap allows boiling point to drop from ~125°C to 100°C, causing boiling and overflow at normal engine operating temp."
            }
        ],
        "contradictory_evidence": [
            "Coolant reservoir cap holds rated 16 psi pressure test and tank plastic is clear and crack-free"
        ]
    },
    "Radiator": {
        "affected_component": "Aluminum Core / Plastic Tank Cross-Flow Engine Radiator",
        "subsystem": "Primary Engine Heat Exchange Circuit",
        "safety_level": "High",
        "required_expertise": "Experienced Technician or Well-Equipped DIYer",
        "required_tools": [
            "Cooling System Pressure Tester (0-30 psi)",
            "Drain Pan",
            "Fin Straightening Comb"
        ],
        "maintenance_actions": {
            "corrective_action": "Inspect aluminum cooling fins for blockage (leaves, dirt, bugs) and plastic side tanks for crimp-seam leaks. Pressure-test to 15 psi. Flush internal scale or replace punctured radiator assembly.",
            "preventive_maintenance": "Gently rinse radiator exterior fins with low-pressure garden hose during spring maintenance.",
            "replacement_criteria": "Replace if plastic end-tanks are cracked, crimp seal leaks, or internal core tubes are clogged with corrosion scale.",
            "do_not_replace_warning": "Do not use stop-leak additives in modern aluminum radiators, as they clog heater cores and small engine passages."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_COOL_RAD_FINS",
                "question": "Are the exterior metal cooling fins on the front of the radiator bent flat or heavily packed with dirt, road salt, or insects?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Blocked radiator fins prevent ambient air from drawing heat away from engine coolant, causing severe highway overheating."
            }
        ],
        "contradictory_evidence": [
            "Radiator core has clear airflow, zero bent fins, and holds 16 psi pressure test without dropping"
        ]
    },
    "AC Compressor": {
        "affected_component": "Air Conditioning Refrigerant Compressor & Magnetic Clutch Assembly",
        "subsystem": "Refrigeration & Cabin Air Conditioning",
        "safety_level": "Medium",
        "required_expertise": "Professional Automotive Technician / ASE Specialist",
        "required_tools": [
            "R134a / R1234yf Manifold Gauge Set",
            "Refrigerant Recovery Machine",
            "Digital Multimeter"
        ],
        "maintenance_actions": {
            "corrective_action": "Check compressor clutch coil resistance and air gap (0.35-0.65 mm). Connect manifold gauges to verify high/low pressure differential. Replace compressor, accumulator/drier, and orifice tube if compressor seized.",
            "preventive_maintenance": "Run vehicle AC for at least 10 minutes once every month (even in winter) to circulate compressor lubricating oil.",
            "replacement_criteria": "Replace if compressor clutch is burnt/slipping, shaft seal leaks green UV dye, or internal pistons produce metallic debris.",
            "do_not_replace_warning": "Refrigerant handling requires EPA Section 609 certification and dedicated recovery equipment. Never vent refrigerant to atmosphere."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_HVAC_COMP_CLICK",
                "question": "When you turn on the AC button, does the center hub of the AC compressor pulley fail to click and spin?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Low refrigerant pressure or a burned clutch coil prevents the magnetic clutch from engaging the compressor shaft."
            }
        ],
        "contradictory_evidence": [
            "AC compressor clutch engages smoothly, high side reaches 150-200 psi, and vents blow ice-cold air"
        ]
    },
    "AC Condenser": {
        "affected_component": "Microchannel Aluminum AC Refrigerant Condenser & Receiver-Drier",
        "subsystem": "Refrigerant Condensation & Heat Rejection",
        "safety_level": "Medium",
        "required_expertise": "Professional Automotive Technician / ASE Specialist",
        "required_tools": [
            "Electronic Refrigerant Sniffer / UV Leak Detection Light",
            "R134a / R1234yf Gauge Set",
            "Vacuum Pump"
        ],
        "maintenance_actions": {
            "corrective_action": "Inspect condenser face for road gravel rock punctures and green fluorescent UV dye stains. Evacuate refrigerant, replace punctured condenser and receiver-drier, pull 30 in-Hg vacuum, and recharge to factory spec.",
            "preventive_maintenance": "Inspect lower condenser fins for corrosion and road salt damage after winter months.",
            "replacement_criteria": "Replace if electronic halogen sniffer or UV lamp detects refrigerant leak from condenser tubes or end-welds.",
            "do_not_replace_warning": "Always replace the receiver-drier / desiccant bag whenever the AC system is opened to atmospheric humidity."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_HVAC_COND_DYE",
                "question": "Do you see oily yellow-green fluorescent dye stains on the front metal condenser grid behind the grille?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Automotive AC systems contain fluorescent PAG oil dye; rock punctures on the front condenser leave bright green oil stains."
            }
        ],
        "contradictory_evidence": [
            "Condenser holds deep 500-micron vacuum test for 30 minutes with zero UV dye presence"
        ]
    },
    "AC Evaporator": {
        "affected_component": "Under-Dash Cabin AC Evaporator Core & Expansion Valve",
        "subsystem": "Cabin Cooling & Dehumidification",
        "safety_level": "Medium",
        "required_expertise": "Professional Automotive Technician / ASE Specialist",
        "required_tools": [
            "Electronic Refrigerant Leak Detector",
            "Ozone / Evaporator Foam Cleaner",
            "Dashboard Removal Kit"
        ],
        "maintenance_actions": {
            "corrective_action": "Insert electronic leak detector into center AC duct and condensation drain tube. If R134a/R1234yf gas is detected in cabin air stream, remove dashboard assembly and replace leaking evaporator core.",
            "preventive_maintenance": "Clear HVAC condensation drain tube regularly to prevent standing water and mold mildew growth on evaporator fins.",
            "replacement_criteria": "Replace if refrigerant sniffer alarms in AC vent air and all under-hood components are leak-free.",
            "do_not_replace_warning": "Ensure condensation drain tube is not simply plugged with leaves before suspecting an evaporator core problem."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_HVAC_EVAP_SMELL",
                "question": "Is there a persistent musty, moldy, or sweet chemical smell coming from the AC vents when the fan is turned on?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Stagnant condensation or pinhole evaporator refrigerant leaks create distinct musty or chemical vapor odors inside the cabin."
            }
        ],
        "contradictory_evidence": [
            "Cabin air is completely odor-free and condensation drains freely beneath vehicle during AC operation"
        ]
    },
    "Cabin Air Filter": {
        "affected_component": "Electrostatic / Activated Charcoal Passenger Cabin Air Filter",
        "subsystem": "Cabin HVAC Filtration",
        "safety_level": "Low",
        "required_expertise": "Basic DIY / Vehicle Owner",
        "required_tools": [
            "Hands / Flashlight / Phillips Screwdriver"
        ],
        "maintenance_actions": {
            "corrective_action": "Open glove box or under-hood access cowl. Remove old cabin filter element and vacuum debris from housing. Insert new high-efficiency particulate air (HEPA) or charcoal filter in correct airflow direction.",
            "preventive_maintenance": "Replace cabin air filter every 12 months or 20,000 km (more frequently in dusty environments).",
            "replacement_criteria": "Replace if pleated media is grey/black with trapped soot, leaves, and dust, or airflow is noticeably reduced.",
            "do_not_replace_warning": "Pay attention to the airflow direction arrow printed on the filter frame during installation."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_HVAC_CABIN_AIRFLOW",
                "question": "Has the airflow volume blowing out of the dashboard vents become significantly weaker even when the blower fan is set to maximum speed?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "A clogged cabin air filter acts like a dense wall, severely restricting cabin vent airflow and straining the blower motor."
            }
        ],
        "contradictory_evidence": [
            "Cabin air filter is clean and white, and vent airflow is forceful across all fan speed settings"
        ]
    },
    "Heater Blower Motor": {
        "affected_component": "12V DC HVAC Squirrel-Cage Cabin Blower Motor Assembly",
        "subsystem": "Cabin Air Distribution",
        "safety_level": "Low",
        "required_expertise": "Experienced Technician or Well-Equipped DIYer",
        "required_tools": [
            "Digital Multimeter (12V DC test)",
            "Torx / Hex Bit Set",
            "Fused Jumper Lead"
        ],
        "maintenance_actions": {
            "corrective_action": "Check blower fuse and verify 12V power and ground at motor connector. Inspect squirrel-cage fan wheel for mice nesting or leaf debris. If motor has 12V but does not spin or shaft bearings rattle, replace blower motor.",
            "preventive_maintenance": "Keep cabin air filter clean to prevent leaves and dirt from entering the blower fan cage.",
            "replacement_criteria": "Replace motor if internal carbon brushes are worn out, motor armature has dead spots, or fan cage is out of balance.",
            "do_not_replace_warning": "Tap the blower motor housing gently while turned on; if it starts spinning, carbon brushes are worn and motor must be replaced."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_HVAC_BLOWER_DEAD",
                "question": "Does the blower fan make a loud chirping, vibrating, or clicking sound, or does it refuse to blow any air on every single fan speed?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Bearing wear causes loud chirping vibrations, while worn carbon brushes cause complete failure across all speed settings."
            }
        ],
        "contradictory_evidence": [
            "Blower motor runs whisper-quiet with strong balanced airflow on all speeds"
        ]
    },
    "Heater Blower Motor Resistor": {
        "affected_component": "HVAC Stepped Resistor Pack / Pulse-Width Modulation (PWM) Blower Controller",
        "subsystem": "Cabin Fan Speed Regulation",
        "safety_level": "Low",
        "required_expertise": "General Mechanic or Intermediate DIYer",
        "required_tools": [
            "Digital Multimeter (Ohms / Continuity)",
            "Socket Set (8mm/10mm)",
            "Wire Stripper & Heat Shrink"
        ],
        "maintenance_actions": {
            "corrective_action": "Inspect electrical connector for melted plastic or overheated terminals. Test resistor coils for open circuit with ohmmeter. Replace resistor module and repair heat-damaged wire pigtail connector.",
            "preventive_maintenance": "Replace worn blower motor if high current draw caused the resistor module to overheat and fail.",
            "replacement_criteria": "Replace if fan only operates on highest speed (Speed 4) and is dead on lower speeds (1, 2, 3), or fan speeds fluctuate uncontrollably.",
            "do_not_replace_warning": "A failing, high-friction blower motor draws excessive current that will rapidly destroy a new resistor pack; check motor amp draw."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_HVAC_RESISTOR_HIGH_ONLY",
                "question": "Does the cabin heater fan only work when turned to the highest speed setting (Position 4), while completely dead on speeds 1, 2, and 3?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Highest fan speed bypasses the resistor pack directly via a relay, so a burned resistor pack leaves only the high speed functional."
            }
        ],
        "contradictory_evidence": [
            "All blower fan speeds (1, 2, 3, 4) function with distinct, correctly graduated airflow steps"
        ]
    },
    "Steering Noise": {
        "affected_component": "Hydraulic Power Steering Rotary Vane Pump & High-Pressure Hose",
        "subsystem": "Hydraulic Power Steering Assist",
        "safety_level": "High",
        "required_expertise": "Experienced Technician or Well-Equipped DIYer",
        "required_tools": [
            "Power Steering Pressure Gauge Kit",
            "Line Flare Nut Wrenches",
            "Fluid Syringe / Turkey Baster"
        ],
        "maintenance_actions": {
            "corrective_action": "Inspect power steering fluid level and condition. Check for foaming fluid (air suction leak at pump inlet O-ring). Bleed steering air by turning wheel lock-to-lock. If pump continues whining, replace power steering pump.",
            "preventive_maintenance": "Flush power steering fluid every 60,000 km to remove metal particulates from rack seals.",
            "replacement_criteria": "Replace pump if internal vanes are worn (low hydraulic assist at low parking speeds) or bearing whine persists after air bleed.",
            "do_not_replace_warning": "A loud buzzing whine that occurs only when turning is often caused by air sucked through a hardened 50-cent reservoir inlet O-ring."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_STR_PUMP_WHINE",
                "question": "Does the steering emit a loud groaning or whining noise that gets louder specifically when you turn the steering wheel while parking?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Power steering vane pump cavitation from low fluid or aerated fluid produces a pronounced groan under hydraulic steering load."
            }
        ],
        "contradictory_evidence": [
            "Steering wheel turns smoothly with zero groaning noise and power steering fluid is free of bubbles"
        ]
    },
    "Shaft and Tires": {
        "affected_component": "Radial Tire Tread Condition & Dynamic Wheel Balancing Weights",
        "subsystem": "Wheel & Tire Assembly",
        "safety_level": "High",
        "required_expertise": "General Mechanic or Intermediate DIYer",
        "required_tools": [
            "Tire Tread Depth Gauge",
            "Precision Tire Pressure Gauge",
            "Dynamic Wheel Balancer (Shop Equipment)"
        ],
        "maintenance_actions": {
            "corrective_action": "Inspect tire tread for cupping, feathering, or broken internal steel belts. Perform 4-wheel dynamic road-force wheel balancing. Rotate tires and inspect suspension ball joints.",
            "preventive_maintenance": "Rotate tires every 8,000-10,000 km and inspect tread depth across all three tread ribs.",
            "replacement_criteria": "Replace tire immediately if tread depth is below 2/32 in (1.6 mm), or if tire tread face shows a distinct physical lump/bulge.",
            "do_not_replace_warning": "Rebalance wheel assemblies before replacing tires for a highway speed vibration."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_STR_TIRE_SHAKE",
                "question": "Does the vehicle body or seat vibrate at steady cruising speeds (90-110 km/h) even when you are NOT touching the brakes?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Unbalanced tires or tire tread runout generate centrifugal harmonic vibrations that peak at highway cruising speeds."
            }
        ],
        "contradictory_evidence": [
            "Ride is completely smooth on highway pavement and tire tread is evenly worn with >4 mm depth"
        ]
    },
    "Power Steering Fluid": {
        "affected_component": "Power Steering Hydraulic Fluid & Return Line Cooler",
        "subsystem": "Hydraulic Power Steering Assist",
        "safety_level": "High",
        "required_expertise": "Basic DIY / Vehicle Owner",
        "required_tools": [
            "Clean Fluid Catch Container",
            "Fluid Extraction Syringe",
            "Approved OEM Power Steering Fluid (ATF / CHF)"
        ],
        "maintenance_actions": {
            "corrective_action": "Inspect fluid level on reservoir dipstick. If fluid is burnt black or smells scorched, evacuate old fluid, clean reservoir mesh filter screen, and flush with fresh OEM-specified power steering fluid.",
            "preventive_maintenance": "Check power steering fluid level at every engine oil change interval.",
            "replacement_criteria": "Flush fluid if black, burnt, or contaminated with moisture or metallic sheen.",
            "do_not_replace_warning": "Always use the exact fluid type specified in the owner manual; using standard ATF in systems requiring synthetic hydraulic fluid (e.g., CHF 11S) destroys seals."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_STR_PS_LOW",
                "question": "Is the power steering fluid level in the under-hood reservoir sitting below the MIN / ADD mark?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Low fluid level starves the pump vanes, causing jerky steering assist and rapid pump cavitation wear."
            }
        ],
        "contradictory_evidence": [
            "Power steering fluid is clean, clear amber or red, and resting at the COLD/HOT full mark"
        ]
    },
    "Wheel Bearing": {
        "affected_component": "Sealed Double-Row Angular Contact Wheel Hub Bearing Assembly",
        "subsystem": "Wheel Hub & Suspension Support",
        "safety_level": "Critical",
        "required_expertise": "Experienced Technician or Well-Equipped DIYer",
        "required_tools": [
            "Floor Jack & Axle Stands",
            "Hub Puller / Slide Hammer",
            "Torque Wrench (high torque 150-250 Nm)",
            "New Axle Nut"
        ],
        "maintenance_actions": {
            "corrective_action": "Elevate wheel on jack stand. Grasp tire at 12 and 6 o'clock positions to check for lateral free-play. Spin wheel by hand while holding suspension spring to feel bearing roughness. Replace defective wheel hub bearing assembly.",
            "preventive_maintenance": "Avoid hitting curbs and inspect bearing seals after driving through deep standing water.",
            "replacement_criteria": "Replace immediately if wheel has detectable mechanical play or produces a continuous roaring growl that changes pitch during lane changes.",
            "do_not_replace_warning": "Always torque the central axle drive nut to exact manufacturer specification with a torque wrench; under/over-torquing ruins new bearings within 1,000 km."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_STR_BEARING_ROAR",
                "question": "Does a deep humming or roaring noise sound like a propeller airplane, and does the sound get louder when you gently swerve in one direction?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Damaged bearing races growl under vehicle weight; turning loads the outside wheel bearing, making the roar substantially louder."
            }
        ],
        "contradictory_evidence": [
            "Wheels spin silently with zero free-play at 12 and 6 o'clock positions"
        ]
    },
    "Tire Pressure Monitoring System (TPMS)": {
        "affected_component": "Valve-Stem Mounted Radio Frequency TPMS Pressure Sensor & Battery",
        "subsystem": "Tire Safety & Pressure Monitoring",
        "safety_level": "Medium",
        "required_expertise": "General Mechanic or Intermediate DIYer",
        "required_tools": [
            "Digital Tire Pressure Gauge",
            "Electronic TPMS Diagnostic Activation Tool",
            "Valve Core Tool"
        ],
        "maintenance_actions": {
            "corrective_action": "Measure physical tire pressures on all 4 tires (and spare) with calibrated manual gauge. If physical pressures are correct, scan sensor IDs with TPMS tool to check internal battery status. Replace failed sensor and relearn to ECU.",
            "preventive_maintenance": "Check tire pressures manually once a month; replace TPMS rubber valve seals and cores during new tire installation.",
            "replacement_criteria": "Replace sensor if internal lithium coin battery is depleted (typically 7-10 year lifespan) or sensor valve stem is corroded.",
            "do_not_replace_warning": "If the TPMS light flashes for 60 seconds at startup before staying solid, it indicates a system communication/sensor fault, not low tire pressure."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_STR_TPMS_FLASH",
                "question": "Does the yellow horseshoe TPMS warning light flash for approximately one minute when you start the car, before staying solid?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "A flashing TPMS light signifies an electronic sensor battery failure or communication fault rather than physical low air pressure."
            }
        ],
        "contradictory_evidence": [
            "All four tire pressures match the door jamb sticker and the TPMS dash light remains dark"
        ]
    },
    "Wheel Hub": {
        "affected_component": "Forged Steel Wheel Hub Flange & Hardened Wheel Studs",
        "subsystem": "Wheel Mounting & Hub Assembly",
        "safety_level": "Critical",
        "required_expertise": "Professional Automotive Technician / ASE Specialist",
        "required_tools": [
            "Dial Indicator with Magnetic Base",
            "Hydraulic Hub Press",
            "Torque Wrench"
        ],
        "maintenance_actions": {
            "corrective_action": "Check hub flange lateral runout using dial indicator mounted to suspension knuckle (runout must be < 0.001 in / 0.025 mm). Inspect wheel studs for stretched or stripped threads. Replace bent hub flange or damaged wheel studs.",
            "preventive_maintenance": "Always hand-start lug nuts before using impact tools; torque to factory specification.",
            "replacement_criteria": "Replace wheel hub if flange face runout exceeds 0.002 in or wheel mounting studs are bent or loose.",
            "do_not_replace_warning": "Never drive with missing or broken wheel studs; one broken stud severely overloads adjacent studs, risking wheel detachment."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_STR_HUB_WOBBLE",
                "question": "Can you physically wobble the elevated road wheel back and forth even after verifying that all lug nuts are fully tightened?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Excessive hub flange runout or bearing core failure allows the wheel to physically tilt off its true rotational axis."
            }
        ],
        "contradictory_evidence": [
            "Hub flange runout measures well within 0.001 in and all wheel studs are straight and undamaged"
        ]
    },
    "Battery Replacement": {
        "affected_component": "12V Lead-Acid / Absorbed Glass Mat (AGM) Starter Battery & Clamps",
        "subsystem": "12V Power Storage & Cranking System",
        "safety_level": "High",
        "required_expertise": "Basic DIY / Vehicle Owner",
        "required_tools": [
            "Digital Battery Conductance Analyzer / Load Tester",
            "Terminal Wire Brush",
            "Safety Goggles & Acid Neutralizer (Baking Soda)"
        ],
        "maintenance_actions": {
            "corrective_action": "Clean white/blue sulfate corrosion off battery posts using wire brush and baking soda solution. Test resting open-circuit voltage (should be >12.6V). Apply 15-second carbon pile load test. If battery drops below 9.6V under load, install fresh group-size battery.",
            "preventive_maintenance": "Coat clean battery posts with dielectric silicone grease or protective anti-corrosion spray washers.",
            "replacement_criteria": "Replace battery if resting voltage is <12.2V after charging, conductance tester indicates <60% rated Cold Cranking Amps (CCA), or plastic case is swollen.",
            "do_not_replace_warning": "WEAR EYE PROTECTION: Lead-acid batteries emit flammable hydrogen gas during charging and contain sulfuric acid."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ELEC_BAT_SLOW_CRANK",
                "question": "When turning the ignition key to start the car in the morning, does the starter motor turn very sluggishly ('rur... rur... rur') or make a single click?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "A depleted or sulfated 12V battery cannot deliver the hundreds of cold-cranking amps required to spin the engine starter motor."
            },
            {
                "question_id": "Q_ELEC_BAT_JUMP",
                "question": "Does the vehicle start up normally and immediately when connected to booster jumper cables from another car?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Successful jump-starting proves the starter motor and ignition circuits work, isolating the fault to weak 12V battery capacity."
            }
        ],
        "contradictory_evidence": [
            "Battery holds 12.6V resting charge and starter cranks with rapid, energetic speed",
            "Battery conductance test passes at 100% rated CCA"
        ]
    },
    "Charging System": {
        "affected_component": "Alternator, Internal Rectifier Diodes & Voltage Regulator Assembly",
        "subsystem": "Electrical Generation & Voltage Regulation",
        "safety_level": "High",
        "required_expertise": "Experienced Technician or Well-Equipped DIYer",
        "required_tools": [
            "Digital Multimeter (DC Volts / AC Ripple)",
            "Inductive Current Clamp (Amp Probe)",
            "Serpentine Belt Tool"
        ],
        "maintenance_actions": {
            "corrective_action": "Inspect alternator drive belt tension. Measure battery terminal voltage with engine idling at 2,000 RPM (charging voltage must be 13.8V-14.7V). Test AC ripple voltage (<0.5V AC). If regulator or diodes are dead, replace alternator.",
            "preventive_maintenance": "Check alternator drive belt tension and rib condition every 20,000 km.",
            "replacement_criteria": "Replace alternator if charging voltage is <13.2V under electrical load (headlights + blower on) or AC ripple >0.5V AC indicates blown diodes.",
            "do_not_replace_warning": "Never disconnect the positive battery cable while the engine is running to 'test' the alternator; modern ECU electronics can be fried by inductive voltage spikes."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ELEC_ALT_BAT_LIGHT",
                "question": "Does the red battery warning symbol remain illuminated on the instrument cluster while the engine is running down the road?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "The battery dashboard light indicates an electrical voltage differential between battery and alternator output, signifying alternator charging failure."
            },
            {
                "question_id": "Q_ELEC_ALT_DIM_LIGHTS",
                "question": "Do your headlights and dashboard lights become noticeably dimmer at idle and brighten up when you press the gas pedal?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "A failing alternator cannot produce adequate current at idle speed, relying on battery discharge to sustain lighting."
            }
        ],
        "contradictory_evidence": [
            "Alternator produces a steady 14.2V at idle with headlights and blower motor turned on",
            "Battery warning light turns off immediately upon engine start"
        ]
    },
    "Door Window Motor": {
        "affected_component": "Permanent Magnet 12V DC Power Window Motor & Drive Gear",
        "subsystem": "Body Electrical & Power Windows",
        "safety_level": "Low",
        "required_expertise": "General Mechanic or Intermediate DIYer",
        "required_tools": [
            "Digital Multimeter / 12V Test Light",
            "Door Panel Trim Pry Tools",
            "Torx Screwdrivers"
        ],
        "maintenance_actions": {
            "corrective_action": "Remove inner door trim panel. Test for 12V power and ground at motor electrical connector while pressing window rocker switch. If 12V is present at motor terminals but motor does not turn, replace window motor.",
            "preventive_maintenance": "Lubricate window felt glass run channels with dry pure silicone spray annually to reduce motor dragging load.",
            "replacement_criteria": "Replace motor if internal thermal circuit breaker trips continuously or motor armature is open-circuit.",
            "do_not_replace_warning": "Verify the master window lockout switch on the driver door is not accidentally engaged before removing door panels."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ELEC_WIN_MOTOR_CLICK",
                "question": "When pressing the window switch, do you hear a faint click inside the door panel, but the window glass refuses to move at all?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "A click inside the door confirms the switch and relay are delivering 12V power, isolating the failure to a seized or dead window motor."
            }
        ],
        "contradictory_evidence": [
            "Window rolls up and down smoothly, quietly, and evenly within 3-4 seconds"
        ]
    },
    "Door Window Regulator": {
        "affected_component": "Window Regulator Cable, Pulley Drum & Mechanical Lift Track",
        "subsystem": "Body Electrical & Power Windows",
        "safety_level": "Low",
        "required_expertise": "Experienced Technician or Well-Equipped DIYer",
        "required_tools": [
            "Door Panel Clip Pliers",
            "Masking / Painters Tape (to secure glass)",
            "10mm Socket Wrench"
        ],
        "maintenance_actions": {
            "corrective_action": "Secure glass with tape. Inspect regulator cables for bird-nesting (frayed wire spooled off pulley) or snapped plastic slide guides. Replace damaged regulator assembly and re-clamp door glass to lift carriage.",
            "preventive_maintenance": "Avoid forcing frozen windows down in freezing winter weather to prevent snapping plastic cable guides.",
            "replacement_criteria": "Replace regulator if cable has jumped plastic pulley grooves, cable wire is kinked/frayed, or glass has dropped into door cavity.",
            "do_not_replace_warning": "Secure the window glass to the door frame with heavy painter's tape before loosening regulator mounting bolts to prevent glass shattering."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ELEC_REG_GRIND",
                "question": "Do you hear the electric motor whirring or crunching/grinding inside the door, while the window glass stays crooked or drops completely down into the door?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Motor whirring with no window movement proves the motor works, but the mechanical regulator cable or plastic slide guide has snapped."
            }
        ],
        "contradictory_evidence": [
            "Window regulator mechanism holds glass rigidly level and travels smoothly throughout its stroke"
        ]
    },
    "Headlamp Bulb": {
        "affected_component": "Halogen (H7/H11/9005) or High-Intensity Discharge / LED Headlamp Bulb",
        "subsystem": "Vehicle Exterior Lighting & Illumination",
        "safety_level": "Medium",
        "required_expertise": "Basic DIY / Vehicle Owner",
        "required_tools": [
            "Nitrile Clean Gloves",
            "Flathead Screwdriver",
            "Digital Multimeter"
        ],
        "maintenance_actions": {
            "corrective_action": "Inspect bulb socket for melted plastic terminals. Remove bulb and inspect tungsten filament for breakage or glass blackening. Replace bulb with correct wattage bulb. Verify headlamp beam vertical/horizontal alignment.",
            "preventive_maintenance": "Replace halogen headlamp bulbs in pairs (both left and right sides) to ensure matched beam output and lifespan.",
            "replacement_criteria": "Replace immediately if filament is broken, capsule has cloudy white gas leak, or glass bulb is burned dark.",
            "do_not_replace_warning": "NEVER touch quartz halogen bulb glass with bare skin; natural skin oils create localized hot-spots that shatter the bulb upon heating."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ELEC_BULB_BURN",
                "question": "Is only one single headlight dark while the other headlight functions completely normally?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Single-bulb darkness typically isolates the failure to that specific bulb filament rather than a master headlamp switch, fuse, or relay."
            }
        ],
        "contradictory_evidence": [
            "Both left and right headlamps illuminate brightly with intact clean filaments and matched beam patterns"
        ]
    },
    "Ignition Distributor Cap": {
        "affected_component": "High-Tension Ignition Distributor Cap & Rotor Button Assembly",
        "subsystem": "High-Voltage Secondary Ignition System",
        "safety_level": "Medium",
        "required_expertise": "General Mechanic or Intermediate DIYer",
        "required_tools": [
            "Spark Plug Wire Marker Labels",
            "Screwdriver / Small Socket Set",
            "Clean Lint-Free Cloth"
        ],
        "maintenance_actions": {
            "corrective_action": "Label plug wire order. Inspect distributor cap underside for hairline carbon tracking cracks, moisture condensation, and corroded brass towers. Replace distributor cap and rotor button as a matched set.",
            "preventive_maintenance": "Replace distributor cap and rotor button every 50,000 km or whenever replacing ignition wire sets.",
            "replacement_criteria": "Replace if conductive black carbon tracks cross terminal towers or brass electrodes are eroded flat.",
            "do_not_replace_warning": "Always transfer spark plug wires to the new distributor cap one by one in exact original firing order to prevent engine misfiring."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ELEC_CAP_WET",
                "question": "Does the engine misfire, stumble, or fail to start specifically on damp, rainy, or high-humidity mornings?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Microscopic cracks in an aged distributor cap absorb atmospheric moisture, shorting high-voltage spark pulses directly to engine ground."
            }
        ],
        "contradictory_evidence": [
            "Distributor cap interior is dry, free of carbon tracks, and brass terminals show zero erosion"
        ]
    },
    "Ignition Wire Set": {
        "affected_component": "Silicone-Insulated High-Voltage Secondary Spark Plug Wires",
        "subsystem": "High-Voltage Secondary Ignition System",
        "safety_level": "Medium",
        "required_expertise": "General Mechanic or Intermediate DIYer",
        "required_tools": [
            "Digital Multimeter (Ohms range)",
            "Spark Plug Wire Puller Pliers",
            "Dielectric Silicone Grease"
        ],
        "maintenance_actions": {
            "corrective_action": "Measure spark plug wire resistance with ohmmeter (specification is typically 3,000-10,000 ohms per foot of wire). Inspect wire boots for spark puncture holes and oil contamination. Replace complete ignition wire set.",
            "preventive_maintenance": "Apply a dab of dielectric silicone grease inside both boots to prevent moisture intrusion and boot sticking.",
            "replacement_criteria": "Replace set if resistance on any single wire exceeds 15,000 ohms, or if electrical arcing is visible in a dark garage with engine running.",
            "do_not_replace_warning": "Never pull on the flexible wire cable itself when removing; always grasp and twist the molded rubber spark plug boot."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ELEC_WIRE_SPARK_ARC",
                "question": "In the dark with the hood open and engine idling, do you see blue electrical sparks arcing off the plug wires to the engine metal?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Degraded silicone insulation permits high-voltage ignition pulses (25,000+ volts) to jump to the nearest metal ground, causing cylinders to misfire."
            }
        ],
        "contradictory_evidence": [
            "All ignition wires measure within manufacturer resistance specification (typically 4,000-7,000 ohms) with zero electrical arcing"
        ]
    },
    "Power Door Lock Actuator": {
        "affected_component": "12V Reversible DC Motor & Door Latch Actuator Assembly",
        "subsystem": "Body Electrical & Central Locking",
        "safety_level": "Low",
        "required_expertise": "General Mechanic or Intermediate DIYer",
        "required_tools": [
            "Door Panel Trim Removal Set",
            "12V Test Light / Multimeter",
            "Torx / Phillips Screwdrivers"
        ],
        "maintenance_actions": {
            "corrective_action": "Remove inner door card. Check for 12V reverse-polarity pulse at lock actuator connector when toggling lock switch. If voltage pulse is received but mechanical lock rod fails to move, replace door lock actuator assembly.",
            "preventive_maintenance": "Spray dry PTFE lubricant onto mechanical door latch lock linkages every 2 years.",
            "replacement_criteria": "Replace actuator if internal DC motor has a dead commutator spot, internal nylon gear teeth are stripped, or it buzzes loudly without locking.",
            "do_not_replace_warning": "Verify lock mechanism is not mechanically binding due to dry old grease or bent linkage rods before replacing electrical actuator."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ELEC_LOCK_BUZZ",
                "question": "When pressing the key fob lock button, do all doors lock except for one door that makes a buzzing or ratcheting noise?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "A buzzing sound from one door confirms electrical power is delivered, but the internal nylon gears inside that actuator are stripped."
            }
        ],
        "contradictory_evidence": [
            "All doors lock and unlock instantly with solid mechanical latch action on key fob command"
        ]
    },
    "Starter Motor": {
        "affected_component": "High-Torque Permanent Magnet Starter Motor & Solenoid Bendix Drive",
        "subsystem": "Engine Starting System",
        "safety_level": "High",
        "required_expertise": "Experienced Technician or Well-Equipped DIYer",
        "required_tools": [
            "Digital Multimeter (Voltage Drop Test)",
            "Remote Starter Switch",
            "Socket Set and Extensions"
        ],
        "maintenance_actions": {
            "corrective_action": "Perform voltage drop test on positive starter cable and ground return. Verify 12V 'S-terminal' signal when turning key. If 12V signal is present at solenoid but starter only clicks or spins freely without engaging flywheel, bench-test and replace starter motor.",
            "preventive_maintenance": "Ensure heavy starter power cables and engine chassis grounds are clean, tight, and free of corrosion.",
            "replacement_criteria": "Replace if solenoid contacts are burnt, armature has high resistance, or Bendix clutch slips on engine flywheel teeth.",
            "do_not_replace_warning": "DISCONNECT NEGATIVE BATTERY TERMINAL before working on starter wiring; the heavy 12V cable is un-fused directly from the battery."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ELEC_STARTER_CLICK",
                "question": "When turning the key to START, does the engine emit a single loud 'CLACK' sound from the starter, while the headlights remain bright?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "A single loud click with bright headlights confirms full battery voltage is reaching the starter solenoid, but the solenoid contacts or motor brushes have failed."
            }
        ],
        "contradictory_evidence": [
            "Starter motor engages instantaneously and spins the engine flywheel with rapid, healthy cranking speed"
        ]
    },
    "Windshield Washer Pump": {
        "affected_component": "12V Submersible Washer Fluid Impeller Pump",
        "subsystem": "Windshield Wiper & Washer System",
        "safety_level": "Low",
        "required_expertise": "Basic DIY / Vehicle Owner",
        "required_tools": [
            "Sewing Needle / Safety Pin (to clear nozzle)",
            "12V Test Light",
            "Clean Container"
        ],
        "maintenance_actions": {
            "corrective_action": "Clear spray nozzle orifices with a fine pin. Listen for pump motor whirring when washer stalk is pulled. Verify 12V power at pump harness. If pump has 12V but motor does not spin, pop pump out of rubber reservoir grommet and install new pump.",
            "preventive_maintenance": "Always use winter windshield washer fluid containing methanol in cold climates to prevent fluid freezing and splitting the plastic pump casing.",
            "replacement_criteria": "Replace pump if motor is burned open-circuit or internal impeller is cracked and seized.",
            "do_not_replace_warning": "Disconnect rubber spray hose under hood and test spray; if fluid squirts freely from the disconnected hose, the washer nozzles are merely clogged."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ELEC_WASHER_WHIRR",
                "question": "When you pull the wiper lever to spray the windshield, is there complete silence with zero motor whirring sound from the front bumper area?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Total silence indicates electrical power failure, a blown wiper fuse, or a burned washer pump motor."
            }
        ],
        "contradictory_evidence": [
            "Washer pump runs eagerly and delivers two strong, well-aimed spray jets across the windshield"
        ]
    },
    "Wiper Motor": {
        "affected_component": "Two-Speed Windshield Wiper Motor & Mechanical Crank Linkage",
        "subsystem": "Windshield Wiper & Washer System",
        "safety_level": "Medium",
        "required_expertise": "Experienced Technician or Well-Equipped DIYer",
        "required_tools": [
            "Windshield Wiper Arm Puller",
            "Socket Set (10mm/12mm/14mm)",
            "Digital Multimeter"
        ],
        "maintenance_actions": {
            "corrective_action": "Inspect wiper transmission linkage pivots for corrosion seizure. Check motor electrical connector for 12V power on low, high, and park terminals. Replace seized linkage or replace wiper motor assembly and align park position.",
            "preventive_maintenance": "Clear wet leaves, pine needles, and ice dams from windshield cowl drainage basin.",
            "replacement_criteria": "Replace motor if motor draws excessive current, park switch contacts are burned, or motor gear is stripped.",
            "do_not_replace_warning": "Do not turn wipers on when blades are frozen to windshield glass; ice resistance strips linkage bushings and burns motor windings."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ELEC_WIPER_PARK",
                "question": "Do the wiper blades stop dead in the middle of your windshield when you switch them off, instead of returning down to the bottom cowl?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Failure to park at the bottom of the windshield indicates defective internal wiper motor park switch contacts or a faulty park relay."
            }
        ],
        "contradictory_evidence": [
            "Wiper arms sweep smoothly across both low and high speeds and park cleanly at the base of the glass"
        ]
    },
    "Horn": {
        "affected_component": "High/Low Dual-Tone Electromagnetic Diaphragm Horn & Horn Relay",
        "subsystem": "Audible Warning Signaling System",
        "safety_level": "Medium",
        "required_expertise": "General Mechanic or Intermediate DIYer",
        "required_tools": [
            "Digital Multimeter / 12V Test Light",
            "Fused Jumper Wire",
            "Wrench Set"
        ],
        "maintenance_actions": {
            "corrective_action": "Check horn fuse and swap horn relay. Inspect steering wheel clock-spring ground contacts. Test for 12V at horn terminal behind front grille while helper presses steering horn pad. Replace corroded horn unit.",
            "preventive_maintenance": "Ensure horn trumpets point downward to prevent rainwater collection inside the metal resonator diaphragm.",
            "replacement_criteria": "Replace horn if 12V and ground are verified at horn terminals but diaphragm emits only a dull click or no sound.",
            "do_not_replace_warning": "Ensure the horn mounting bracket has clean metal-to-metal contact with the vehicle chassis if the horn uses case grounding."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ELEC_HORN_RELAY",
                "question": "When you press the center of the steering wheel, can you hear a faint click from the fuse box under the hood, but no horn sound?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "A relay click in the engine fuse box confirms the steering wheel clock-spring switch works, isolating the issue to the horn fuse, wiring, or the horn itself."
            }
        ],
        "contradictory_evidence": [
            "Horn sounds instantly with a crisp, authoritative dual-tone audible blast upon pressing steering wheel pad"
        ]
    },
    "Windshield Washer Fluid": {
        "affected_component": "Windshield Washer Fluid Fluid Reservoir & Level Float Sensor",
        "subsystem": "Windshield Cleaning System",
        "safety_level": "Low",
        "required_expertise": "Basic DIY / Vehicle Owner",
        "required_tools": [
            "Funnel",
            "Washer Fluid (Rain-X or Standard De-icer)"
        ],
        "maintenance_actions": {
            "corrective_action": "Inspect washer fluid reservoir for physical level. If reservoir is empty, refill with all-season washer fluid. If fluid level light stays on with full reservoir, clean or replace stuck float sensor.",
            "preventive_maintenance": "Top up washer fluid before long road trips; switch to sub-zero de-icing fluid before winter freeze.",
            "replacement_criteria": "Replace reservoir if plastic tank is split from winter freezing or mounting tabs are broken.",
            "do_not_replace_warning": "Never use plain tap water in cold climates; frozen water in washer lines expands and cracks the reservoir tank and fluid pump."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ELEC_WASHER_FLOAT",
                "question": "Is the low washer fluid dashboard warning icon on, but looking in the engine bay shows the plastic reservoir is completely full?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "A stuck float sensor or gummed level sensor terminals will illuminate the low washer warning despite a full fluid reservoir."
            }
        ],
        "contradictory_evidence": [
            "Washer reservoir is filled, spray flows forcefully, and low fluid warning indicator remains off"
        ]
    },
    "Canister Purge Valve": {
        "affected_component": "EVAP Canister Purge Solenoid Valve",
        "subsystem": "Evaporative Emission Control System (EVAP)",
        "safety_level": "Medium",
        "required_expertise": "General Mechanic or Intermediate DIYer",
        "required_tools": [
            "Handheld Vacuum Pump with Gauge",
            "OBD-II Diagnostic Scanner (DTC Reader)",
            "Digital Multimeter"
        ],
        "maintenance_actions": {
            "corrective_action": "Disconnect purge valve electrical plug and vacuum line. Apply handheld vacuum pump; valve must hold vacuum with no electrical power. If valve leaks vacuum when de-energized (stuck open), replace purge valve.",
            "preventive_maintenance": "Do not 'top off' or click the fuel nozzle multiple times after it clicks off at gas pumps; liquid fuel floods EVAP valves.",
            "replacement_criteria": "Replace valve if it fails vacuum holding test unpowered (stuck open causing hard start after refueling) or solenoid coil is open.",
            "do_not_replace_warning": "A stuck-open purge valve typically sets code P0441 or P0496 and causes extended engine cranking specifically right after filling up with gas."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_EMIS_PURGE_GAS_FILL",
                "question": "Does the vehicle crank for an extended time or struggle to start immediately after you fill up the gas tank at a service station?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "A stuck-open purge valve dumps raw fuel vapors directly into the intake manifold during refueling, severely flooding the engine."
            }
        ],
        "contradictory_evidence": [
            "Purge valve holds vacuum perfectly unpowered and engine starts instantaneously after gas tank fill-ups"
        ]
    },
    "Catalytic Converter": {
        "affected_component": "Three-Way Ceramic Honeycomb Catalytic Converter Exhaust Monolith",
        "subsystem": "Exhaust Aftertreatment & Emissions",
        "safety_level": "Medium",
        "required_expertise": "Professional Automotive Technician / ASE Specialist",
        "required_tools": [
            "Infrared Thermometer Gun",
            "Exhaust Backpressure Gauge (0-15 psi)",
            "OBD-II Live Graphing Scanner"
        ],
        "maintenance_actions": {
            "corrective_action": "Compare inlet and outlet converter temperatures (outlet should be 20-50°C hotter than inlet). Graph upstream vs downstream O2 sensors on live scan data. If downstream sensor mirrors upstream sensor switching, catalytic efficiency is degraded; replace converter.",
            "preventive_maintenance": "Fix engine misfires immediately; unburned raw fuel entering the hot exhaust melts catalytic converter honeycomb cores within minutes.",
            "replacement_criteria": "Replace converter if diagnostic code P0420/P0430 is set with confirmed good O2 sensors, or exhaust backpressure exceeds 1.5 psi at 2,500 RPM (clogged core).",
            "do_not_replace_warning": "Never replace a catalytic converter without first identifying and repairing what destroyed it (e.g. engine oil burning, coolant leak, or misfires)."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_EMIS_CAT_SULFUR",
                "question": "Do you smell a strong rotten-egg or sulfur odor coming from the exhaust pipe, especially under hard vehicle acceleration?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "A poisoned or overwhelmed catalytic converter cannot properly oxidize hydrogen sulfide compounds in exhaust gases, producing rotten-egg sulfur odor."
            },
            {
                "question_id": "Q_EMIS_CAT_POWER_LOSS",
                "question": "Does the engine feel severely restricted or choked, unable to rev past 3,000-4,000 RPM when climbing hills or accelerating?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "A melted or disintegrated catalytic converter ceramic substrate creates massive exhaust backpressure, choking engine breathing."
            }
        ],
        "contradictory_evidence": [
            "Downstream oxygen sensor voltage is a steady flat line (0.6V-0.7V) and exhaust backpressure is <0.5 psi at 2,500 RPM"
        ]
    },
    "Charcoal Canister": {
        "affected_component": "Activated Carbon EVAP Vapor Storage Canister",
        "subsystem": "Evaporative Emission Control System (EVAP)",
        "safety_level": "Medium",
        "required_expertise": "Experienced Technician or Well-Equipped DIYer",
        "required_tools": [
            "Automotive EVAP Smoke Machine (0.5 psi regulated)",
            "Low-Pressure Gauge",
            "Scan Tool EVAP Vent Command"
        ],
        "maintenance_actions": {
            "corrective_action": "Perform regulated low-pressure EVAP smoke test to identify canister cracks. Shake canister to check if internal charcoal pellets have broken loose and escaped into purge lines. Replace saturated or cracked canister assembly.",
            "preventive_maintenance": "Never top-off the gas tank after automatic pump nozzle shutoff to prevent liquid gasoline from ruining the activated charcoal bed.",
            "replacement_criteria": "Replace canister if liquid gasoline has saturated the charcoal bed (heavy canister weight) or charcoal pellets are found inside EVAP purge lines.",
            "do_not_replace_warning": "If charcoal pellets have entered the vacuum lines, all EVAP lines must be blown out with compressed air to protect the new purge solenoid."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_EMIS_CANISTER_GAS_SMELL",
                "question": "Is there a strong smell of gasoline fumes lingering around the rear wheels or fuel filler area when the car is parked?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "A cracked charcoal canister or saturated carbon bed allows raw fuel tank vapors to escape directly into ambient air instead of being trapped."
            }
        ],
        "contradictory_evidence": [
            "EVAP smoke test holds 0.5 psi test pressure with zero smoke leakage from charcoal canister body"
        ]
    },
    "Exhaust Manifold": {
        "affected_component": "Cast Iron / Tubular Stainless Steel Exhaust Header Manifold",
        "subsystem": "Exhaust Gas Collection & Scavenging",
        "safety_level": "High",
        "required_expertise": "Professional Automotive Technician / ASE Specialist",
        "required_tools": [
            "Mechanic's Stethoscope with Tube",
            "Straight Edge Precision Ruler",
            "Penetrating Thread Oil & Torx / Stud Extractor"
        ],
        "maintenance_actions": {
            "corrective_action": "Inspect manifold casting for thermal stress cracks, especially near center runners. Check for broken exhaust manifold studs on cylinder head. Machine mating flange flat or replace cracked exhaust manifold with fresh hardware.",
            "preventive_maintenance": "Ensure engine heat shields are intact to protect surrounding hoses and brake lines from radiant exhaust heat.",
            "replacement_criteria": "Replace manifold if structural cracks allow exhaust gas leakage or flange warpage exceeds 0.006 in (0.15 mm).",
            "do_not_replace_warning": "CARBON MONOXIDE HAZARD: Cracked exhaust manifolds leak toxic odorless carbon monoxide gas into the vehicle cabin ventilation system."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_EMIS_MANIFOLD_TICK",
                "question": "Do you hear a loud rhythmic 'ticking' or 'puffing' sound from the engine bay when first started cold, which becomes quieter as the engine warms up?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Hairline exhaust manifold cracks leak loudly when cold; as thermal expansion heats the metal, the crack temporarily pinches shut, silencing the tick."
            }
        ],
        "contradictory_evidence": [
            "Exhaust manifold is free of black soot carbon tracking and runs whisper-quiet from cold startup to operating temp"
        ]
    },
    "Exhaust Manifold Gasket": {
        "affected_component": "Multi-Layer Steel (MLS) Exhaust Manifold-to-Cylinder Head Gasket",
        "subsystem": "Exhaust Flange Sealing",
        "safety_level": "Medium",
        "required_expertise": "Experienced Technician or Well-Equipped DIYer",
        "required_tools": [
            "Torque Wrench",
            "Gasket Scraper & Degreaser",
            "Replacement High-Temp Exhaust Studs"
        ],
        "maintenance_actions": {
            "corrective_action": "Inspect cylinder head flange for black carbon soot trails indicative of gasket blowout. Remove exhaust manifold, clean cylinder head surface, install new MLS gasket, and torque manifold bolts in sequence from center outward.",
            "preventive_maintenance": "Check manifold stud tightness if minor exhaust ticking begins.",
            "replacement_criteria": "Replace gasket whenever exhaust manifold is removed or if soot staining confirms exhaust blow-by.",
            "do_not_replace_warning": "Always use new copper-plated or hardened prevailing-torque exhaust nuts to prevent fasteners from backing out under thermal cycling."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_EMIS_GASKET_SOOT",
                "question": "Can you see black powdery soot stains on the side of the engine cylinder head around the exhaust ports?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Hot exhaust gas leaking past a blown manifold gasket leaves conspicuous black carbon soot spray marks on aluminum engine surfaces."
            }
        ],
        "contradictory_evidence": [
            "Cylinder head exhaust ports are clean and shiny with zero carbon soot tracking around gasket edges"
        ]
    },
    "Fuel Tank Pressure Sensor": {
        "affected_component": "EVAP Fuel Tank Vapor Pressure Piezoelectric Transducer",
        "subsystem": "EVAP Leak Detection Monitoring",
        "safety_level": "Medium",
        "required_expertise": "Experienced Technician or Well-Equipped DIYer",
        "required_tools": [
            "OBD-II Scan Tool (Live Data PID reading in In-H2O / Volts)",
            "Digital Multimeter"
        ],
        "maintenance_actions": {
            "corrective_action": "View live FTPS voltage with fuel gas cap removed (should read atmospheric baseline ~1.5V or 0 in-H2O). If sensor reads fixed high/low voltage regardless of tank pressure, drop fuel tank or access sender module to replace sensor.",
            "preventive_maintenance": "Keep EVAP vent filter clean to prevent dust from fouling pressure sensor ports.",
            "replacement_criteria": "Replace if sensor output is erratic, stuck at 0V or 5V reference, or fails OBD-II EVAP self-test monitor.",
            "do_not_replace_warning": "Verify 5V reference supply and ground from ECU before replacing sensor, as damaged wiring harness over fuel tank causes identical fault codes."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_EMIS_FTPS_GAS_CAP",
                "question": "Does the 'Check Fuel Cap' warning light appear on the dashboard even when you have tightened the gas cap until it clicks multiple times?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "The ECU uses the Fuel Tank Pressure Sensor to detect tank seal; a faulty sensor cannot measure tank vacuum, triggering false gas cap warnings."
            }
        ],
        "contradictory_evidence": [
            "Fuel tank pressure sensor reads atmospheric baseline voltage with gas cap off and responds accurately to tank vacuum"
        ]
    },
    "Knock Sensor": {
        "affected_component": "Piezoelectric Acoustic Engine Detonation / Knock Sensor",
        "subsystem": "Ignition Timing & Knock Control",
        "safety_level": "High",
        "required_expertise": "Professional Automotive Technician / ASE Specialist",
        "required_tools": [
            "Digital Multimeter (AC mV test)",
            "Torque Wrench (crucial for knock sensor calibration)",
            "Oscilloscope"
        ],
        "maintenance_actions": {
            "corrective_action": "Inspect knock sensor plastic housing for heat cracks. Measure internal resistance and test AC millivolt spike when gently tapping engine block with a brass punch. Replace cracked knock sensor and torque to exact OEM spec.",
            "preventive_maintenance": "Always use the minimum octane rating specified by the vehicle manufacturer to avoid true engine pre-ignition knock.",
            "replacement_criteria": "Replace if sensor circuit is open/shorted or produces zero AC voltage signal during acoustic tap testing.",
            "do_not_replace_warning": "KNOCK SENSOR TORQUE IS CRITICAL: Over-tightening or under-tightening the mounting bolt alters sensor piezoelectric frequency response."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_EMIS_KNOCK_PING",
                "question": "Do you hear a sharp metallic pinging, rattling, or 'marbles in a tin can' sound from the engine specifically when accelerating uphill?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Engine detonation occurs when fuel-air mixture explodes prematurely; a failing knock sensor fails to notify the ECU to retard ignition timing."
            }
        ],
        "contradictory_evidence": [
            "Engine operates under heavy load with zero pre-ignition pinging and knock sensor circuit resistance is within spec"
        ]
    },
    "M.A.P. Sensor": {
        "affected_component": "Manifold Absolute Pressure (MAP) Silicon Piezo-Resistive Sensor",
        "subsystem": "Engine Air Intake & Load Sensing",
        "safety_level": "Medium",
        "required_expertise": "General Mechanic or Intermediate DIYer",
        "required_tools": [
            "Handheld Vacuum Pump with Gauge",
            "Digital Multimeter (DC Volts)",
            "Scan Tool Live Data"
        ],
        "maintenance_actions": {
            "corrective_action": "Check vacuum port on intake manifold for oil sludge or carbon blockage. Apply known vacuum levels (0-20 in-Hg) with hand pump while monitoring output voltage; voltage must drop smoothly with vacuum. Replace contaminated MAP sensor.",
            "preventive_maintenance": "Keep engine PCV system clean to prevent engine blow-by oil vapors from coating intake MAP sensor ports.",
            "replacement_criteria": "Replace sensor if output voltage does not change smoothly with vacuum changes or scan tool shows fixed barometric pressure reading.",
            "do_not_replace_warning": "Inspect the rubber vacuum hose or intake manifold O-ring seal; an external vacuum leak mimics a bad MAP sensor."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_EMIS_MAP_STUMBLE",
                "question": "Does the engine stumble, buck, or hesitate severely when you suddenly step on the accelerator pedal from a standstill?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "The MAP sensor immediately informs the ECU of sudden throttle opening to enrich fuel mixture; delayed MAP signal causes severe tip-in stumble."
            }
        ],
        "contradictory_evidence": [
            "MAP sensor output reads exactly barometric pressure (approx 101 kPa / 29.9 in-Hg) key-on engine-off and drops to ~30 kPa at warm idle"
        ]
    },
    "Oxygen Sensor": {
        "affected_component": "Heated Zirconia Lambda Oxygen (O2) Sensor (Bank 1 / Bank 2)",
        "subsystem": "Exhaust Air-Fuel Ratio Closed-Loop Feedback",
        "safety_level": "Medium",
        "required_expertise": "Experienced Technician or Well-Equipped DIYer",
        "required_tools": [
            "Slotted Oxygen Sensor Socket (22mm / 7/8 in)",
            "Digital Multimeter (Heater Resistance)",
            "OBD-II Live Graphing Scanner"
        ],
        "maintenance_actions": {
            "corrective_action": "Check O2 sensor internal heater circuit resistance (typically 4-15 ohms cold). Graph sensor voltage switching on live scanner (upstream sensor must oscillate rapidly between 0.1V and 0.9V at least 1-2 times per second). Replace sluggish O2 sensor.",
            "preventive_maintenance": "Replace upstream lambda oxygen sensors proactively every 120,000-150,000 km to optimize fuel efficiency.",
            "replacement_criteria": "Replace sensor if internal heater circuit is open (code P0135/P0141) or sensor voltage is lazy / stuck lean or rich.",
            "do_not_replace_warning": "Apply high-temperature anti-seize paste to threads of new O2 sensor, but keep anti-seize away from the perforated sensor sniffer tip."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_EMIS_O2_GAS_MILEAGE",
                "question": "Has your vehicle fuel economy dropped significantly (e.g. 15-25% more fuel consumed) alongside a Check Engine Light?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "A degraded or lazy upstream O2 sensor defaults the engine management system into rich open-loop fuel delivery, dramatically increasing fuel consumption."
            }
        ],
        "contradictory_evidence": [
            "Upstream O2 sensor cross-counts rapidly between 0.15V and 0.85V at warm idle and fuel trims are within +/- 5%"
        ]
    },
    "Balance Shaft": {
        "affected_component": "Counter-Rotating Engine Harmonic Balance Shaft & Drive Bearings",
        "subsystem": "Engine Mechanical Reciprocating Balance",
        "safety_level": "High",
        "required_expertise": "Professional Automotive Technician / ASE Specialist",
        "required_tools": [
            "Mechanic's Stethoscope",
            "Engine Timing Alignment Kit",
            "Oil Pressure Gauge"
        ],
        "maintenance_actions": {
            "corrective_action": "Check engine timing belt/chain alignment for balance shaft timing marks. Inspect balance shaft bearing journals for oil starvation wear. Replace worn balance shaft bearings and reset timing.",
            "preventive_maintenance": "Maintain regular oil change intervals using correct viscosity oil to preserve balance shaft pressurized hydrodynamic bearings.",
            "replacement_criteria": "Replace shaft or bearings if excessive radial play causes loud rumbling engine vibration that peaks at specific RPMs.",
            "do_not_replace_warning": "Verify engine harmonic balancer / crankshaft pulley rubber damper has not delaminated before disassembling balance shaft assemblies."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ENG_BALANCE_VIBE",
                "question": "Does the entire vehicle cabin experience a pronounced rhythmic shaking vibration that intensifies sharply as engine RPM passes 2,500-3,000?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Out-of-phase balance shafts fail to cancel secondary engine reciprocating forces, creating strong resonance vibrations at medium RPMs."
            }
        ],
        "contradictory_evidence": [
            "Engine revs smoothly through entire RPM range with zero harmonic buzz or cabin floor vibration"
        ]
    },
    "Boost Pressure": {
        "affected_component": "Turbocharger Wastegate Actuator, Boost Control Solenoid & Intercooler Hoses",
        "subsystem": "Forced Induction Turbocharger System",
        "safety_level": "Medium",
        "required_expertise": "Experienced Technician or Well-Equipped DIYer",
        "required_tools": [
            "Handheld Pressure / Vacuum Pump",
            "Smoke Machine for Charge Air Piping",
            "OBD-II Live Boost Pressure Scanner"
        ],
        "maintenance_actions": {
            "corrective_action": "Perform smoke test on charge air cooler (intercooler) and silicone couplers for boost leaks. Test wastegate actuator diaphragm with handheld pump (actuator rod must move smoothly at 8-12 psi). Replace leaking intercooler hose or wastegate solenoid.",
            "preventive_maintenance": "Inspect turbocharger intercooler silicone boot couplers for oil soaking and clamp tightness every 40,000 km.",
            "replacement_criteria": "Replace boost hoses if split; replace wastegate actuator if internal diaphragm does not hold pressure.",
            "do_not_replace_warning": "A high-pitched whooshing or hissing noise under heavy acceleration almost always indicates a blown intercooler hose coupler rather than a dead turbo."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ENG_BOOST_HISS",
                "question": "Do you hear a loud rushing or whooshing air leak sound from the front of the car specifically when the turbo is spooling under hard acceleration?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Pressurized charge air escaping through split intercooler piping or loose clamps produces a distinct whooshing hissing noise under boost."
            }
        ],
        "contradictory_evidence": [
            "Manifold boost pressure meets target spec (typically 12-18 psi) on scan tool with zero air leak sounds"
        ]
    },
    "Diesel Injection Pump": {
        "affected_component": "High-Pressure Diesel Common-Rail Fuel Injection Pump (HPFP)",
        "subsystem": "High-Pressure Diesel Fuel Delivery",
        "safety_level": "High",
        "required_expertise": "Professional Automotive Technician / ASE Specialist",
        "required_tools": [
            "Diesel High-Pressure Diagnostic Gauge (2000+ Bar rating)",
            "OBD-II Common Rail Pressure Scanner",
            "Diesel Fuel Cleanliness Test Kit"
        ],
        "maintenance_actions": {
            "corrective_action": "Check low-pressure lift pump feed pressure to HPFP inlet. Inspect diesel fuel filter for metallic glitter debris. If common rail pressure fails to reach cranking threshold (typically 250-300 bar), replace high-pressure injection pump and flush entire fuel system.",
            "preventive_maintenance": "Replace diesel fuel filters religiously every 20,000-30,000 km and never run a common-rail diesel tank completely empty.",
            "replacement_criteria": "Replace pump if internal cam/roller generates metal glitter in fuel filter bowl or rail pressure cannot maintain setpoint under load.",
            "do_not_replace_warning": "EXTREME HYDRAULIC INJURY HAZARD: High-pressure common-rail fuel operates at up to 2,000 bar (30,000 psi). Never loosen fittings while running."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ENG_DIESEL_HPFP_METAL",
                "question": "When opening the diesel fuel filter canister, do you see shiny bronze or metallic flakes shimmering in the bottom of the fuel bowl?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Metallic flakes in the diesel filter canister are conclusive evidence of internal high-pressure injection pump roller/cam flaking failure."
            }
        ],
        "contradictory_evidence": [
            "Common rail fuel pressure hits required 300 bar cranking threshold instantly and fuel filter bowl is pristine"
        ]
    },
    "Diesel Glow Plug": {
        "affected_component": "In-Cylinder High-Temperature Diesel Glow Plug & Controller Relay",
        "subsystem": "Diesel Cold-Start Pre-Heating System",
        "safety_level": "Medium",
        "required_expertise": "Experienced Technician or Well-Equipped DIYer",
        "required_tools": [
            "Digital Multimeter (low ohms test)",
            "Deep Glow Plug Sockets",
            "Penetrating Thread Oil & Torque Wrench"
        ],
        "maintenance_actions": {
            "corrective_action": "Measure individual glow plug electrical resistance to ground (good glow plugs read 0.5 - 2.0 ohms; open circuit reads infinity). Replace burned-out glow plugs with engine warm using penetrating oil to avoid shearing.",
            "preventive_maintenance": "Cycle glow plugs twice on freezing mornings before cranking to reduce cold-start battery and starter strain.",
            "replacement_criteria": "Replace plug if resistance is open-circuit (>5 ohms) or tip carbon buildup prevents preheating.",
            "do_not_replace_warning": "DO NOT FORCE STUBBORN GLOW PLUGS: Glow plug shear limit is low (approx 20-35 Nm); breaking a plug off in the cylinder head requires head removal."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ENG_GLOW_COLD_SMOKE",
                "question": "Does the diesel engine struggle to start on cold mornings, and when it finally catches, does it run rough and emit clouds of gray/white fuel smoke?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Cold cylinders without glow plug preheat fail to ignite diesel fuel cleanly, blowing raw unburned white/gray diesel smoke until heated."
            }
        ],
        "contradictory_evidence": [
            "All glow plugs measure between 0.7 and 1.2 ohms resistance and engine starts cleanly on cold mornings"
        ]
    },
    "Engine Mounts": {
        "affected_component": "Hydraulic / Vulcanized Rubber Engine & Transmission Isolator Mounts",
        "subsystem": "Powertrain Structural Isolation",
        "safety_level": "Medium",
        "required_expertise": "General Mechanic or Intermediate DIYer",
        "required_tools": [
            "Floor Jack with Wooden Block (to support oil pan)",
            "Pry Bar",
            "Metric Socket Set & Torque Wrench"
        ],
        "maintenance_actions": {
            "corrective_action": "Perform engine power-brake torque test while helper observes engine movement (movement should not exceed 1-2 inches). Inspect rubber for oil saturation, tears, or leaked hydraulic fluid. Replace collapsed engine mounts in pairs.",
            "preventive_maintenance": "Fix engine oil leaks promptly; motor oil dripping onto rubber mounts chemically breaks down and softens the rubber.",
            "replacement_criteria": "Replace mount if rubber is completely torn through, hydraulic fluid has leaked out, or metal bracket bottoms out against chassis.",
            "do_not_replace_warning": "Always place a broad wooden block between the hydraulic floor jack and the engine oil pan to prevent denting or punching through the pan."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ENG_MOUNT_CLUNK",
                "question": "Do you feel a heavy clunk or lurch under your feet when shifting an automatic car from Park into Drive or Reverse?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Torn engine mounts allow the powertrain to rotate violently on its axis when torque is applied during gear engagement."
            }
        ],
        "contradictory_evidence": [
            "Engine stays solidly located with <1 inch deflection during forward and reverse stall torque tests"
        ]
    },
    "Exhaust Valve": {
        "affected_component": "Cylinder Head Poppet Exhaust Valve & Stellite Hardened Valve Seat",
        "subsystem": "Cylinder Head Gas Exchange & Valvetrain",
        "safety_level": "High",
        "required_expertise": "Professional Automotive Technician / ASE Specialist",
        "required_tools": [
            "Cylinder Leak-Down Tester (with shop air)",
            "Compression Gauge (0-300 psi)",
            "Borescope Camera"
        ],
        "maintenance_actions": {
            "corrective_action": "Perform cylinder compression test followed by compressed air leak-down test at TDC. If air hisses audibly out the exhaust tailpipe, the exhaust valve is burned or bent. Remove cylinder head, recut valve seats, and lap new exhaust valves.",
            "preventive_maintenance": "Maintain correct engine valve clearance lash (on non-hydraulic lifter engines) and avoid lean fuel mixtures.",
            "replacement_criteria": "Replace valve if edge is burned / notched, valve stem is bent, or cylinder leak-down past exhaust valve exceeds 20%.",
            "do_not_replace_warning": "Always perform a wet compression test (adding a teaspoon of oil into cylinder); if compression stays low, valves are leaking rather than piston rings."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ENG_VALVE_LEAKDOWN",
                "question": "During a cylinder leak-down test with the piston at Top Dead Center, can you hear compressed air rushing directly out the exhaust tailpipe?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Compressed air escaping out the tailpipe proves a mechanical seal failure of the exhaust valve face against the cylinder head valve seat."
            }
        ],
        "contradictory_evidence": [
            "All cylinder compressions are within 10% of each other (typically 160-190 psi) with zero exhaust leakage"
        ]
    },
    "Fuel Injector": {
        "affected_component": "High-Pressure Solenoid Multi-Hole Fuel Injection Nozzle",
        "subsystem": "Electronic Fuel Injection (EFI)",
        "safety_level": "High",
        "required_expertise": "Experienced Technician or Well-Equipped DIYer",
        "required_tools": [
            "Digital Multimeter (Injector Coil Ohms)",
            "NOID Light Set (to test pulse signal)",
            "Fuel Pressure Gauge Kit"
        ],
        "maintenance_actions": {
            "corrective_action": "Check injector coil resistance (typically 11-16 ohms for high-impedance). Use NOID light to verify ECU pulse command. Test fuel pressure drop on injector balance test. Ultrasonic clean or replace clogged / leaking fuel injector.",
            "preventive_maintenance": "Use high-detergent Top Tier gasoline to prevent carbon deposit baking on precision injector nozzle spray holes.",
            "replacement_criteria": "Replace injector if coil is open-circuit, pintle leaks fuel under rest pressure (flooding cylinder), or spray pattern is a solid stream instead of mist.",
            "do_not_replace_warning": "Always replace injector top and bottom Viton rubber O-rings whenever an injector is pulled from the fuel rail to prevent fire hazards."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ENG_INJECTOR_CLICK",
                "question": "Using a mechanic's screwdriver or stethoscope on each injector while idling, does one injector remain completely silent with no rhythmic clicking?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Healthy fuel injectors emit a sharp, rapid rhythmic metallic click as the internal pintle solenoid snaps open and closed."
            }
        ],
        "contradictory_evidence": [
            "All injectors click with uniform rhythm, coil resistances match within 0.3 ohms, and balance test shows equal fuel flow"
        ]
    },
    "Idle Air Control Valve": {
        "affected_component": "Idle Air Control (IAC) Stepper Motor / PWM Bypass Air Valve",
        "subsystem": "Idle Speed Control & Throttle Bypass",
        "safety_level": "Medium",
        "required_expertise": "General Mechanic or Intermediate DIYer",
        "required_tools": [
            "Throttle Body / Carb Cleaner Spray",
            "Lint-Free Rags",
            "Digital Multimeter"
        ],
        "maintenance_actions": {
            "corrective_action": "Remove IAC valve from throttle body. Clean heavy black carbon gum deposits off plunger pintle and air passage using throttle body cleaner. Test stepper motor coil resistances. If pintle is seized or electrical windings open, install new IAC valve.",
            "preventive_maintenance": "Clean throttle body air passages and IAC valve every 50,000 km.",
            "replacement_criteria": "Replace if motor coils are open/shorted or pintle does not extend and retract during ECU idle calibration cycle.",
            "do_not_replace_warning": "Clean the carbon out first before buying a new valve; 80% of idle hunting issues are resolved simply by spraying away gummy carbon."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ENG_IAC_STALL_STOP",
                "question": "Does the engine idle smoothly when driving, but immediately stall or die the moment you take your foot off the gas to stop at a red light?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "When the throttle plate snaps closed at a stop, the IAC valve must open instantly to provide idle air; a carbon-gummed valve stalls the engine."
            }
        ],
        "contradictory_evidence": [
            "Engine maintains rock-solid idle speed (700-750 RPM) with AC compressor and headlights switched on"
        ]
    },
    "Intake Valve": {
        "affected_component": "Cylinder Head Intake Poppet Valve, Spring & Valve Guide",
        "subsystem": "Cylinder Head Valvetrain",
        "safety_level": "High",
        "required_expertise": "Professional Automotive Technician / ASE Specialist",
        "required_tools": [
            "Cylinder Leak-Down Tester",
            "Borescope Camera",
            "Engine Compression Tester"
        ],
        "maintenance_actions": {
            "corrective_action": "Perform cylinder leak-down test with piston at TDC. If air hisses audibly out the intake throttle body, the intake valve is leaking or carbon-fouled. For Gasoline Direct Injection (GDI) engines, perform walnut shell media blasting on intake valves.",
            "preventive_maintenance": "Install an oil catch can or use premium fuel with intake detergent additives to minimize direct injection valve carbon caking.",
            "replacement_criteria": "Replace valve if valve face is pitted/bent, or carbon buildup is so severe that mechanical valve seating is compromised.",
            "do_not_replace_warning": "On GDI engines, heavy valve carbon deposits mimic bent valves; perform walnut shell decoking before pulling the cylinder head."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ENG_INTAKE_BACKFIRE",
                "question": "Does the engine pop or backfire through the air filter box / intake manifold when you accelerate hard?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "An intake valve that fails to seal allows combustion fire to flash backward up through the intake manifold runners into the air intake."
            }
        ],
        "contradictory_evidence": [
            "Intake valves are clean and sealed with zero air hissing through the throttle body on leak-down test"
        ]
    },
    "Oil Pump": {
        "affected_component": "Crankshaft-Driven Trochoid / Gear Internal Engine Oil Pump",
        "subsystem": "Engine Pressurized Lubrication System",
        "safety_level": "Critical",
        "required_expertise": "Professional Automotive Technician / ASE Specialist",
        "required_tools": [
            "Mechanical Oil Pressure Test Gauge (0-100 psi)",
            "Feeler Gauges (for pump rotor clearance)",
            "Engine Support Beam"
        ],
        "maintenance_actions": {
            "corrective_action": "Connect mechanical oil pressure gauge to oil pressure switch port. Verify warm idle pressure (specification is typically >15 psi at idle and >40 psi at 3,000 RPM). If mechanical pressure is low, remove oil pan, inspect oil pickup tube screen, and replace oil pump.",
            "preventive_maintenance": "Change engine oil and OEM filter at recommended mileage intervals; never run engine low on oil.",
            "replacement_criteria": "Replace pump if internal rotor-to-body or tip clearances exceed 0.005 in (0.12 mm) or pressure relief valve spring is broken.",
            "do_not_replace_warning": "CRITICAL ENGINE RISK: Stop engine immediately if red oil pressure light flickers; driving with low oil pressure destroys engine rod bearings within seconds."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ENG_OIL_LIGHT_HOT",
                "question": "Does the red oil can warning lamp flicker on specifically when the engine is fully warmed up and idling at a stop?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Hot oil thins out; worn pump rotors or excessive bearing clearances cause oil pressure to plummet below the 5-7 psi warning switch threshold."
            }
        ],
        "contradictory_evidence": [
            "Mechanical oil pressure gauge reads a healthy 20+ psi at hot idle and 45-60 psi at 3,000 RPM"
        ]
    },
    "Piston Rings": {
        "affected_component": "Combustion Compression Rings & Multi-Piece Oil Control Ring Pack",
        "subsystem": "Cylinder Piston & Crankcase Sealing",
        "safety_level": "High",
        "required_expertise": "Professional Automotive Technician / ASE Specialist",
        "required_tools": [
            "Dry and Wet Compression Tester",
            "Cylinder Leak-Down Tester",
            "Borescope Inspection Camera"
        ],
        "maintenance_actions": {
            "corrective_action": "Perform dry compression test, record values, add 1 tablespoon of clean motor oil into spark plug hole, and re-test (wet test). If compression jumps significantly (by >30 psi), the piston rings or cylinder walls are worn. Disassemble block, hone cylinders, and re-ring pistons.",
            "preventive_maintenance": "Avoid prolonged engine idling and replace engine oil regularly to prevent oil control rings from sticking with carbon sludge.",
            "replacement_criteria": "Re-ring pistons if blow-by pressure forces oil out the dipstick tube, wet compression test confirms ring leakage, or oil consumption exceeds 1 quart per 1,000 km.",
            "do_not_replace_warning": "Check the PCV valve first; a plugged PCV valve builds crankcase pressure that mimics worn piston ring blow-by."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ENG_RING_BLUE_SMOKE",
                "question": "Does the exhaust pipe emit continuous blue-gray smoke during heavy acceleration, accompanied by heavy oil consumption?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Worn or stuck piston oil control rings allow crankcase oil to be drawn up past the pistons into the combustion chambers, burning with blue smoke."
            }
        ],
        "contradictory_evidence": [
            "Dry compression is balanced and high across all cylinders, with zero blue exhaust smoke and negligible oil consumption"
        ]
    },
    "Timing Belt": {
        "affected_component": "Reinforced Rubber Synchronous Cogged Engine Timing Belt & Tensioner",
        "subsystem": "Valvetrain Synchronization System",
        "safety_level": "Critical",
        "required_expertise": "Professional Automotive Technician / ASE Specialist",
        "required_tools": [
            "Engine Timing Alignment Pin / Cam Lock Kit",
            "Tensioner Tool",
            "Crankshaft Pulley Counter-Holder Wrench"
        ],
        "maintenance_actions": {
            "corrective_action": "Inspect timing belt for missing cogs, oil contamination, fraying cords, or excessive slack. If timing has jumped or belt mileage interval is exceeded, replace timing belt, hydraulic tensioner, idler pulleys, and water pump.",
            "preventive_maintenance": "Mandatory replacement every 7 years or 100,000-160,000 km (consult owner manual for exact interval).",
            "replacement_criteria": "Replace immediately upon visual inspection showing rubber cracking, tooth separation, or oil contamination.",
            "do_not_replace_warning": "INTERFERENCE ENGINE WARNING: If a timing belt snaps on an interference engine, pistons collide with open valves, destroying the cylinder head."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ENG_TIMING_BELT_SPIN",
                "question": "Did the engine suddenly die while driving, and now when turning the key, does the starter motor crank abnormally fast with a light, smooth, 'whirring' sound?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "A snapped timing belt leaves valves stationary and cylinders with zero compression, allowing the starter motor to spin the crankshaft with zero resistance."
            }
        ],
        "contradictory_evidence": [
            "Timing marks on crankshaft and camshaft gears align with laser accuracy at TDC cylinder 1"
        ]
    },
    "Valve Cover Gasket": {
        "affected_component": "Perimeter Elastomeric Valve Cover / Cam Cover Gasket & Spark Plug Tube Seals",
        "subsystem": "Cylinder Head External Sealing",
        "safety_level": "Medium",
        "required_expertise": "General Mechanic or Intermediate DIYer",
        "required_tools": [
            "Inch-Pound Torque Wrench",
            "RTV Silicone for Cam Corners",
            "Gasket Scraper & Degreaser"
        ],
        "maintenance_actions": {
            "corrective_action": "Inspect exterior of cylinder head and spark plug tubes for standing engine oil. Remove valve cover, scrape old gasket residue, degrease mating surface, install new gasket and tube seals, apply small dabs of RTV at cylinder head joints, and torque to spec.",
            "preventive_maintenance": "Inspect valve cover perimeter for weeping oil at every 20,000 km service.",
            "replacement_criteria": "Replace if rubber gasket has hardened to brittle plastic or oil leaks onto hot exhaust manifold.",
            "do_not_replace_warning": "Do not over-torque valve cover bolts; over-tightening splits modern rubber gaskets and cracks plastic or cast magnesium covers."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ENG_PLUG_TUBE_OIL",
                "question": "When you pull out the spark plug boots, are the spark plugs sitting soaked in a pool of motor oil inside the spark plug tubes?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Hardened spark plug tube seals allow oil under the valve cover to flood down into the spark plug wells, causing ignition misfires."
            }
        ],
        "contradictory_evidence": [
            "Valve cover exterior and spark plug tubes are bone-dry with zero oil weeping or burning smell"
        ]
    },
    "Fan Belt": {
        "affected_component": "Engine Cooling Fan V-Belt / Accessory Drive Belt",
        "subsystem": "Auxiliary Fan Mechanical Drive",
        "safety_level": "High",
        "required_expertise": "Basic DIY / Vehicle Owner",
        "required_tools": [
            "Belt Tension Gauge",
            "Pry Bar / Belt Adjustment Wrench",
            "Flashlight"
        ],
        "maintenance_actions": {
            "corrective_action": "Check belt deflection (should be ~1/2 in / 12 mm under thumb pressure between pulleys). Inspect underside for missing chunks or glazed shiny sidewalls. Adjust alternator / fan bracket tension or install new belt.",
            "preventive_maintenance": "Check belt tension and condition every 20,000 km.",
            "replacement_criteria": "Replace belt if underside has more than 3 cracks per inch or sidewalls are glazed slick.",
            "do_not_replace_warning": "Never spray belt dressing chemicals on modern synthetic EPDM belts; belt dressings attract abrasive dirt."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ENG_FAN_BELT_SQUEAL",
                "question": "Does a piercing high-pitched belt squeal occur when you first start the car or rev the engine quickly?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "A loose or glazed fan belt slips around the drive pulley under mechanical load, creating a loud high-friction squeal."
            }
        ],
        "contradictory_evidence": [
            "Fan belt is properly tensioned, free of cracks, and drives pulleys with zero slip or noise"
        ]
    },
    "Engine Belt": {
        "affected_component": "Serpentine Multi-Rib Accessory Drive Belt & Automatic Spring Tensioner",
        "subsystem": "Front Engine Accessory Drive (FEAD)",
        "safety_level": "High",
        "required_expertise": "General Mechanic or Intermediate DIYer",
        "required_tools": [
            "Serpentine Belt Tensioner Tool / Long Breaker Bar",
            "Belt Wear Gauge",
            "Torque Wrench"
        ],
        "maintenance_actions": {
            "corrective_action": "Check automatic tensioner indicator marks for excessive belt stretch. Inspect rib grooves with EPDM wear depth gauge. Rotate tensioner arm to release tension and install new serpentine belt, ensuring correct routing diagram.",
            "preventive_maintenance": "Replace serpentine drive belt every 100,000 km or 6 years.",
            "replacement_criteria": "Replace belt if rib depth is worn flush with gauge or tensioner pulley bearing rattles when spun by hand.",
            "do_not_replace_warning": "Always inspect the automatic belt tensioner pulley and idler bearings when replacing the belt; a seized idler pulley snaps a new belt immediately."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ENG_SERP_BELT_CRACKS",
                "question": "Does the ribbed underside of the wide serpentine engine belt show numerous cracks, missing rib chunks, or frayed string edges?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Age and heat harden the synthetic rubber ribs of the serpentine belt, leading to chunking and sudden belt snap."
            }
        ],
        "contradictory_evidence": [
            "Serpentine belt ribs are deep, supple, track straight on pulleys, and tensioner marks are centered"
        ]
    },
    "Air Filter": {
        "affected_component": "Pleated Cellulose / Synthetic Engine Air Cleaner Filter Element",
        "subsystem": "Engine Air Induction Filtration",
        "safety_level": "Low",
        "required_expertise": "Basic DIY / Vehicle Owner",
        "required_tools": [
            "Hands / Air Box Retaining Clips",
            "Shop Vacuum"
        ],
        "maintenance_actions": {
            "corrective_action": "Unclip air filter housing. Remove filter and hold up to bright light; if light cannot penetrate the pleats, vacuum housing box and install new engine air filter.",
            "preventive_maintenance": "Replace engine air filter every 20,000-30,000 km (more frequently in dusty gravel driving conditions).",
            "replacement_criteria": "Replace if paper media is darkened with embedded dirt, clogged with insects, or oil-soaked.",
            "do_not_replace_warning": "Never tap or blow dirty air filters with high-pressure air and reinstall; high-pressure air tears microscopic holes in filter fibers, allowing abrasive silica into engine cylinders."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ENG_AIR_FILTER_DIRTY",
                "question": "When you open the air box, is the paper air filter element dark brown or black with dirt, leaves, and insects trapped in the pleats?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "A heavily choked air filter restricts engine intake airflow like breathing through a straw, lowering power output and throttle response."
            }
        ],
        "contradictory_evidence": [
            "Air filter pleats are clean, light-colored, and allow bright light to shine through with zero restriction"
        ]
    },
    "Engine Control Unit (ECU)": {
        "affected_component": "Electronic Powertrain Control Module (PCM / ECM) Microprocessor",
        "subsystem": "Engine Electronic Management",
        "safety_level": "High",
        "required_expertise": "Professional Automotive Technician / ASE Specialist",
        "required_tools": [
            "Bi-Directional Scan Tool",
            "Oscilloscope",
            "Wiring Schematics & Breakout Box"
        ],
        "maintenance_actions": {
            "corrective_action": "Verify all ECU power feeds, constant battery 12V, ignition switched 12V, and clean chassis grounds. Check for communication on CAN bus pins. If ECU has good power and grounds but fails to communicate or drive internal injector/coil circuits, re-flash or replace ECU module.",
            "preventive_maintenance": "Ensure engine battery terminals and body grounds are tight; voltage spikes and loose grounds can damage electronic control modules.",
            "replacement_criteria": "Condemn ECU only after every power, ground, and sensor input circuit is physically verified good with a multimeter.",
            "do_not_replace_warning": "ECUs are rarely defective; 90% of suspected 'bad ECU' cases are actually broken ground wires, blown fuses, or chewed wiring harnesses."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ENG_ECU_NO_COMMS",
                "question": "Does a diagnostic OBD-II scan tool display 'No Communication' or 'Link Error' when plugged into the car's diagnostic port with key on?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Failure of the OBD-II scanner to establish a data link indicates loss of ECU power, bad network ground, or a fried module processor."
            }
        ],
        "contradictory_evidence": [
            "Scan tool communicates instantaneously, reads all live engine sensor data, and bidirectional controls operate normally"
        ]
    },
    "Engine Oil": {
        "affected_component": "Full Synthetic / Semi-Synthetic Engine Lubrication Oil & Spin-On Oil Filter",
        "subsystem": "Engine Pressurized Lubrication System",
        "safety_level": "Critical",
        "required_expertise": "Basic DIY / Vehicle Owner",
        "required_tools": [
            "Oil Filter Wrench",
            "Drain Pan (10-quart capacity)",
            "Funnel & Fresh OEM Oil"
        ],
        "maintenance_actions": {
            "corrective_action": "Pull dipstick to check oil level, color, and viscosity. If level is below MIN mark, top up with manufacturer-specified grade. If oil is pitch black, thick, or smells of fuel, perform complete engine oil and filter change.",
            "preventive_maintenance": "Change engine oil every 8,000-12,000 km (synthetic) or 5,000 km (conventional).",
            "replacement_criteria": "Change oil if service interval is exceeded, oil has gritty feel on fingers, or oil level is critically low.",
            "do_not_replace_warning": "CRITICAL ENGINE RISK: Never drive with the oil level below the bottom dipstick hole; oil starvation causes catastrophic crankshaft bearing seizure."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ENG_OIL_DIPSTICK_LOW",
                "question": "When you pull the under-hood engine oil dipstick and wipe it, does the oil level fail to reach even the bottom indicator mark?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Low engine oil level starves the oil pickup tube during cornering and braking, causing fatal metal-on-metal bearing contact."
            }
        ],
        "contradictory_evidence": [
            "Engine oil level is sitting squarely at the FULL mark on dipstick and oil is golden amber with clean viscosity"
        ]
    },
    "Fuel Filter": {
        "affected_component": "High-Pressure Inline Fuel Filter / In-Tank Fuel Filter Sock",
        "subsystem": "Fuel Supply & Filtration System",
        "safety_level": "High",
        "required_expertise": "General Mechanic or Intermediate DIYer",
        "required_tools": [
            "Fuel Line Disconnect Tools",
            "Safety Glasses & Fuel Catch Container",
            "Fuel Pressure Gauge"
        ],
        "maintenance_actions": {
            "corrective_action": "Depressurize fuel system by pulling fuel pump fuse while engine idles until it stalls. Disconnect fuel line quick-connect clips. Replace fuel filter in correct flow direction indicated by arrow on canister.",
            "preventive_maintenance": "Replace external inline fuel filters every 40,000-60,000 km.",
            "replacement_criteria": "Replace if fuel pressure drops under high-RPM engine load or dirty black fuel drains backward from filter inlet.",
            "do_not_replace_warning": "FIRE SAFETY: Disconnect negative battery terminal and keep a Class B fire extinguisher nearby when opening fuel lines."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ENG_FUEL_FILTER_BOG",
                "question": "Does the engine start and idle normally, but bog down and cut out when you demand full power at highway speeds?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "A clogged fuel filter allows enough low-flow fuel volume for idle, but starves the engine of volume under high-speed demand."
            }
        ],
        "contradictory_evidence": [
            "Fuel pressure maintains rated specification (typically 45-60 psi) steadily under wide-open throttle acceleration"
        ]
    },
    "PCV Valve": {
        "affected_component": "Positive Crankcase Ventilation (PCV) Spring-Loaded Check Valve",
        "subsystem": "Crankcase Vapor Ventilation System",
        "safety_level": "Low",
        "required_expertise": "Basic DIY / Vehicle Owner",
        "required_tools": [
            "Pliers / Wrench",
            "Replacement PCV Hose"
        ],
        "maintenance_actions": {
            "corrective_action": "Remove PCV valve from valve cover and shake it; it must click crisply. Verify vacuum suction at idle. If valve is gummed shut, stuck open, or hose is collapsed from oil softening, clean or replace PCV valve and hose.",
            "preventive_maintenance": "Inspect and clean or replace PCV valve every 50,000 km.",
            "replacement_criteria": "Replace if internal check ball does not rattle when shaken, or valve allows air to blow through in both directions.",
            "do_not_replace_warning": "A stuck-closed PCV valve creates positive crankcase pressure that forces oil past valve cover gaskets and main oil seals."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ENG_PCV_RATTLE",
                "question": "When you pull the PCV valve out of the valve cover and shake it back and forth, does it feel clogged with sludge and fail to rattle?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "A working PCV valve has a spring-loaded internal pintle that rattles like a spray paint can; a clogged valve is stuck solid with oil sludge."
            }
        ],
        "contradictory_evidence": [
            "PCV valve rattles crisply when shaken and draws strong, steady vacuum at idle"
        ]
    },
    "Throttle Body": {
        "affected_component": "Electronic Throttle Body (ETB) Butterfly Valve & Servo Motor",
        "subsystem": "Engine Air Induction Control",
        "safety_level": "Medium",
        "required_expertise": "General Mechanic or Intermediate DIYer",
        "required_tools": [
            "Dedicated Throttle Body / Air Intake Cleaner",
            "Lint-Free Microfiber Cloth",
            "Scan Tool Throttle Relearn"
        ],
        "maintenance_actions": {
            "corrective_action": "Remove air intake duct. Inspect throttle butterfly bore for black gummy oil carbon buildup. Spray lint-free rag with throttle body cleaner and wipe bore clean. Perform scan tool electronic throttle position relearn procedure.",
            "preventive_maintenance": "Clean throttle body throat and butterfly valve edge every 50,000 km to prevent sticking.",
            "replacement_criteria": "Replace throttle body if internal drive gears are stripped or throttle actuator motor has high internal resistance.",
            "do_not_replace_warning": "Do not spray aerosol cleaner directly into the electronic motor housing or force motorized throttle plates open aggressively by hand."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ENG_TB_CARBON_RING",
                "question": "Looking into the throttle body throat with the intake tube off, is there a thick black ring of gummy carbon deposits around the brass butterfly plate?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Carbon deposits around the throttle plate perimeter disrupt precision idle airflow, causing erratic hunting idle and sticky throttle tip-in."
            }
        ],
        "contradictory_evidence": [
            "Throttle bore is spotless aluminum and butterfly plate opens and closes with lightning-fast electronic response"
        ]
    },
    "Fuel Pressure Regulator": {
        "affected_component": "Vacuum-Modulated Fuel Rail Pressure Regulator & Diaphragm",
        "subsystem": "Electronic Fuel Injection (EFI)",
        "safety_level": "High",
        "required_expertise": "Experienced Technician or Well-Equipped DIYer",
        "required_tools": [
            "Fuel Rail Pressure Gauge with Bleed Valve",
            "Handheld Vacuum Pump",
            "Metric Wrench"
        ],
        "maintenance_actions": {
            "corrective_action": "Pull vacuum reference hose off regulator; check for raw gasoline dripping from vacuum nipple (indicates torn internal diaphragm). Connect fuel pressure gauge; verify pressure increases by 5-10 psi when vacuum line is disconnected. Replace regulator if diaphragm leaks.",
            "preventive_maintenance": "Inspect regulator vacuum reference line for dry rot cracking every 2 years.",
            "replacement_criteria": "Replace immediately if gasoline is present in the vacuum port or fuel rail pressure is out of specification.",
            "do_not_replace_warning": "Raw fuel leaking past a ruptured regulator diaphragm gets sucked directly into intake manifold vacuum, causing severe engine flooding and oil dilution."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ENG_FPR_VAC_GAS",
                "question": "When you pull the small rubber vacuum hose off the fuel pressure regulator, does raw liquid gasoline drip out of the vacuum nipple?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Any fuel inside the vacuum nipple proves the internal rubber diaphragm has ruptured, dumping raw fuel into the engine vacuum system."
            }
        ],
        "contradictory_evidence": [
            "Regulator vacuum port is bone-dry and fuel rail pressure responds instantly to vacuum changes"
        ]
    },
    "Fuel Pump": {
        "affected_component": "In-Tank Electric High-Pressure Turbine Fuel Pump & Check Valve",
        "subsystem": "Fuel Supply System",
        "safety_level": "High",
        "required_expertise": "Experienced Technician or Well-Equipped DIYer",
        "required_tools": [
            "Fuel Pressure Test Gauge",
            "Fuel Pump Lock-Ring Tool",
            "Digital Multimeter"
        ],
        "maintenance_actions": {
            "corrective_action": "Connect fuel pressure gauge to fuel rail Schrader valve. Turn key to ON; pump should prime for 2 seconds and build rated pressure (40-60 psi). If zero pressure, test 12V power at pump relay and pump connector. If pump has 12V but does not run, drop tank and replace pump module.",
            "preventive_maintenance": "Avoid habitually driving with less than 1/4 tank of gas; in-tank fuel pumps rely on submersion in gasoline for motor cooling.",
            "replacement_criteria": "Replace pump if pressure is below factory spec, pump whines loudly, or internal check valve bleeds off pressure immediately upon shutdown.",
            "do_not_replace_warning": "Always inspect the fuel pump relay and inertia safety fuel cutoff switch before pulling the fuel pump from the fuel tank."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ENG_PUMP_PRIME_HUM",
                "question": "When you turn the ignition key to the ON position (without cranking), do you hear a 2-second electric humming sound from beneath the rear seats?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "No",
                "contradictory_answer": "Yes",
                "context": "Normal fuel pumps hum for 2 seconds at key-on to prime fuel rail pressure; complete silence indicates lack of electrical power or a burned pump motor."
            }
        ],
        "contradictory_evidence": [
            "Fuel pump primes with healthy 2-second hum and fuel rail holds 50+ psi pressure steadily"
        ]
    },
    "Fuel Tank": {
        "affected_component": "Polyethylene / Stamped Steel Fuel Storage Tank & Filler Neck",
        "subsystem": "Fuel Storage & Containment",
        "safety_level": "Critical",
        "required_expertise": "Professional Automotive Technician / ASE Specialist",
        "required_tools": [
            "Transmission Jack (to support tank)",
            "Fuel Evacuation Syringe / Caddy",
            "Fire Extinguisher"
        ],
        "maintenance_actions": {
            "corrective_action": "Inspect fuel tank straps, seams, and filler neck for rust perforation or road impact punctures. If external fuel dripping or wetness is found, drain fuel completely and install replacement fuel tank assembly.",
            "preventive_maintenance": "Rinse road de-icing salt from underbody fuel tank straps and filler neck shield after winter.",
            "replacement_criteria": "Replace fuel tank immediately if any crack, puncture, or seam weld leak allows fuel leakage.",
            "do_not_replace_warning": "EXTREME FIRE HAZARD: Never attempt to weld or solder a fuel tank; explosive fuel vapors remain inside empty tanks indefinitely."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ENG_TANK_DRIP",
                "question": "Can you see liquid gasoline dripping from the underside of the fuel tank or pooling under the rear of the vehicle?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "A leaking fuel tank presents an extreme catastrophic fire and explosion risk that requires immediate repair."
            }
        ],
        "contradictory_evidence": [
            "Fuel tank body, seams, and filler neck are dry, clean, and free of any rust perforation or fuel odor"
        ]
    },
    "Throttle Position Sensor": {
        "affected_component": "Throttle Position Sensor (TPS) Dual Potentiometer",
        "subsystem": "Engine Air Intake & Load Sensing",
        "safety_level": "Medium",
        "required_expertise": "General Mechanic or Intermediate DIYer",
        "required_tools": [
            "Digital Multimeter (Analog needle or Min/Max recording)",
            "Scan Tool Live Data Graph"
        ],
        "maintenance_actions": {
            "corrective_action": "Connect analog multimeter or scanner graph to TPS signal wire. Slowly depress accelerator pedal from idle to wide-open throttle with key on engine off. Output voltage must rise smoothly from ~0.5V to ~4.5V with zero dead spots. Replace defective TPS sensor.",
            "preventive_maintenance": "Keep throttle shaft bushings clean and lubricated to prevent mechanical sticking.",
            "replacement_criteria": "Replace sensor if voltage output has glitches/dropouts or scan tool reports correlation code between track 1 and track 2.",
            "do_not_replace_warning": "Ensure sensor throttle blade linkage is not binding mechanically before assuming an internal electrical sensor flaw."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_ENG_TPS_DEAD_SPOT",
                "question": "Does the vehicle engine suddenly jerk, cutout, or stumble at one specific pedal position when you press the gas pedal?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Worn potentiometer tracks develop localized dead spots that drop the throttle signal to zero volts, causing instantaneous fuel cutout."
            }
        ],
        "contradictory_evidence": [
            "TPS output voltage sweeps with complete linear smoothness from 0.5V to 4.5V on graph without glitches"
        ]
    },
    "Bevel Gears": {
        "affected_component": "Spiral Bevel Differential Ring and Pinion Final Drive Gears",
        "subsystem": "Final Drive Differential Assembly",
        "safety_level": "High",
        "required_expertise": "Professional Automotive Technician / ASE Specialist",
        "required_tools": [
            "Gear Marking Compound",
            "Dial Indicator with Magnetic Base (Backlash gauge)",
            "Inch-Pound Beam Torque Wrench"
        ],
        "maintenance_actions": {
            "corrective_action": "Drain differential fluid and inspect magnetic drain plug for metal shards. Inspect gear tooth mesh pattern with yellow gear marking compound. Check ring-and-pinion backlash (spec typically 0.006-0.010 in). Re-shim or replace worn bevel gear set.",
            "preventive_maintenance": "Replace hypoid gear oil every 50,000-80,000 km with recommended GL-5 gear lubricant.",
            "replacement_criteria": "Replace gears if tooth faces show metal spalling/pitting or gear backlash exceeds factory tolerance.",
            "do_not_replace_warning": "Setting up bevel final drive gears requires precision pinion bearing preload and gear backlash shimming; improper setup whines loudly."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_TRANS_BEVEL_WHINE_LOAD",
                "question": "Does a distinct high-pitched gear whine sound from beneath the car specifically when pressing the accelerator, which silences when you coast?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Hypoid bevel gears whine under drive load when ring-and-pinion tooth contact patterns are misaligned or worn."
            }
        ],
        "contradictory_evidence": [
            "Differential runs silently under drive and coast, and gear marking compound shows centered oval tooth contact"
        ]
    },
    "Center Differential": {
        "affected_component": "AWD / 4WD Center Differential Planetary Gearset & Viscous Lock",
        "subsystem": "All-Wheel Drive Transfer & Torque Distribution",
        "safety_level": "High",
        "required_expertise": "Professional Automotive Technician / ASE Specialist",
        "required_tools": [
            "Wheel Speed Tachometer",
            "Drivetrain Lift",
            "Fluid Catch Pan"
        ],
        "maintenance_actions": {
            "corrective_action": "Inspect transfer case / center differential fluid for burnt metallic sheen. Test for torque binding by performing full-lock slow circles on dry asphalt. Replace seized center differential unit or repair worn planetary carrier.",
            "preventive_maintenance": "Ensure all 4 tires are identical brand, model, and tread depth (within 2/32 in) to prevent center differential overheating.",
            "replacement_criteria": "Replace differential if vehicle crow-hops / binds on tight parking turns or differential housing overheats.",
            "do_not_replace_warning": "Mismatched tire diameters between front and rear axles will destroy a center differential within a few hundred kilometers."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_TRANS_CENTER_BIND",
                "question": "Does the vehicle shudder, bind, or chirp its tires when making tight, slow-speed steering turns in a parking lot?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "A locked or seized center differential prevents required front-to-rear axle speed differentiation, causing severe drivetrain binding."
            }
        ],
        "contradictory_evidence": [
            "AWD vehicle turns tight slow-speed circles smoothly with zero tire scrubbing or drivetrain binding"
        ]
    },
    "Clutch Cable": {
        "affected_component": "Multi-Strand Steel Clutch Release Cable & Auto-Adjuster Mechanism",
        "subsystem": "Manual Transmission Clutch Actuation",
        "safety_level": "High",
        "required_expertise": "General Mechanic or Intermediate DIYer",
        "required_tools": [
            "Pliers / Pry Bar",
            "Clutch Cable Lubricant",
            "Wrench Set"
        ],
        "maintenance_actions": {
            "corrective_action": "Inspect cable sheath for melted nylon casing from exhaust heat and cable strands for fraying near pedal quadrant. Check pedal free play. Adjust cable tension or replace snapped/binding clutch cable.",
            "preventive_maintenance": "Inspect cable ends and pedal pivot bushings for wear and apply graphite cable lube every 40,000 km.",
            "replacement_criteria": "Replace if individual steel strands are broken, cable binds inside casing, or cable has stretched past adjustment limit.",
            "do_not_replace_warning": "Ensure clutch release fork on transmission is pivoting freely before assuming a heavy pedal is caused by the cable."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_TRANS_CABLE_SNAP",
                "question": "Did the clutch pedal suddenly snap directly to the floorboard and stay there, leaving the transmission unable to enter gear?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "A snapped clutch cable immediately eliminates all mechanical connection between pedal and clutch release fork."
            }
        ],
        "contradictory_evidence": [
            "Clutch pedal has smooth linear resistance throughout travel with 1/2 in free-play at top"
        ]
    },
    "Clutch Slave Cylinder": {
        "affected_component": "Hydraulic Clutch Release Slave Cylinder & Pushrod",
        "subsystem": "Manual Transmission Clutch Hydraulics",
        "safety_level": "High",
        "required_expertise": "Experienced Technician or Well-Equipped DIYer",
        "required_tools": [
            "Brake / Clutch Pressure Bleeder",
            "Flare Nut Wrench",
            "Catch Pan"
        ],
        "maintenance_actions": {
            "corrective_action": "Pull back rubber dust boot on slave cylinder; check for fluid leakage. Test hydraulic pressure. Bleed air bubbles from hydraulic clutch line. If cylinder leaks fluid or internal piston is seized, replace clutch slave cylinder.",
            "preventive_maintenance": "Flush clutch hydraulic fluid every 2 years alongside brake fluid maintenance.",
            "replacement_criteria": "Replace if fluid leaks into bellhousing or past dust boot, or pushrod does not extend fully when clutch pedal is pressed.",
            "do_not_replace_warning": "If the slave cylinder is a concentric slave cylinder (CSC) located inside the transmission bellhousing, the transmission must be dropped."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_TRANS_SLAVE_LEAK",
                "question": "Is the clutch fluid reservoir empty, or is brake fluid leaking from the bottom seam of the transmission bellhousing?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "A leaking clutch slave cylinder drops hydraulic pressure, leaving the clutch pedal limp and unable to disengage the clutch disc."
            }
        ],
        "contradictory_evidence": [
            "Clutch slave cylinder dust boot is bone-dry and pushrod strokes full 15-20 mm travel upon pedal application"
        ]
    },
    "Differential": {
        "affected_component": "Differential Carrier Case, Spider Pinion Gears & Side Carrier Bearings",
        "subsystem": "Axle Power Distribution",
        "safety_level": "High",
        "required_expertise": "Professional Automotive Technician / ASE Specialist",
        "required_tools": [
            "Dial Indicator with Magnetic Base",
            "Bearing Puller & Press",
            "Differential Case Spreader"
        ],
        "maintenance_actions": {
            "corrective_action": "Inspect differential housing for oil leaks at pinion seal and side axle seals. Check spider gear cross-pin for galling and carrier bearings for spalling. Replace worn carrier bearings or rebuild differential assembly.",
            "preventive_maintenance": "Change differential gear oil according to factory severe-service schedule; add limited-slip friction modifier if equipped with LSD.",
            "replacement_criteria": "Replace carrier assembly if spider gear teeth are chipped or bearing races show severe flaking.",
            "do_not_replace_warning": "Do not mistake tire noise for differential bearing whine; tire noise changes pitch with road surface, differential noise changes with vehicle load."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_TRANS_DIFF_GROWL",
                "question": "Does a continuous deep metallic growl or rumble come from the drive axle that gets louder the faster you drive?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Pitted differential side carrier or pinion bearings emit a continuous rumbling growl directly proportional to road speed."
            }
        ],
        "contradictory_evidence": [
            "Differential operates with whisper silence and gear oil is clean with zero metallic glitter on magnetic plug"
        ]
    },
    "Live Axle": {
        "affected_component": "Solid Drive Axle Tube, Shafts & Wheel End Roller Bearings",
        "subsystem": "Rear Axle & Drivetrain",
        "safety_level": "High",
        "required_expertise": "Experienced Technician or Well-Equipped DIYer",
        "required_tools": [
            "Slide Hammer Axle Puller",
            "Bearing and Seal Driver Set",
            "Drain Pan"
        ],
        "maintenance_actions": {
            "corrective_action": "Inspect rear axle ends near brake backing plates for gear oil leakage past outer axle shaft seals. Use slide hammer to pull axle shaft; inspect bearing surface on axle journal for grooving. Install fresh axle bearing and oil seal.",
            "preventive_maintenance": "Inspect axle vent breather tube to ensure it is clear; a plugged vent builds pressure that forces oil past axle seals.",
            "replacement_criteria": "Replace axle shaft if bearing journal surface is grooved or shaft flange runout exceeds 0.005 in.",
            "do_not_replace_warning": "A plugged axle breather valve on top of the axle tube causes oil seals to leak; clear the breather before installing new seals."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_TRANS_AXLE_SEAL_OIL",
                "question": "Is gear oil leaking out onto the inside of your rear wheel rim or soaking the rear brake shoes/caliper?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Failure of the outer live axle oil seal allows heavy hypoid gear oil to leak directly into the wheel hub and brake assembly."
            }
        ],
        "contradictory_evidence": [
            "Rear axle tubes and wheel backing plates are clean, dry, and axle shafts have zero radial play"
        ]
    },
    "Rigid Axle": {
        "affected_component": "Non-Drive Solid Beam Axle & Suspension Locating Bushings",
        "subsystem": "Suspension & Axle Geometry",
        "safety_level": "High",
        "required_expertise": "Experienced Technician or Well-Equipped DIYer",
        "required_tools": [
            "Computerized 4-Wheel Alignment Machine",
            "Tape Measure / Trammel Bar",
            "Hydraulic Bushing Press"
        ],
        "maintenance_actions": {
            "corrective_action": "Perform 4-wheel alignment to measure rear thrust angle and individual rear toe/camber. Inspect beam axle for collision bends or cracked locating control arm bushings. Replace damaged beam axle or press in new rubber suspension bushings.",
            "preventive_maintenance": "Inspect axle locating bushings for rubber tearing during regular suspension inspections.",
            "replacement_criteria": "Replace rigid axle if alignment reveals bent camber/toe exceeding non-adjustable factory limits.",
            "do_not_replace_warning": "A rigid beam axle is structural; never attempt to heat and bend an axle beam back into shape as heat destroys metallurgy."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_TRANS_RIGID_DOGTRACK",
                "question": "Does the vehicle appear to 'dog-track' (rear of the vehicle travels slightly sideways to the front) when driving straight down the road?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "A shifted or bent rigid rear axle creates an abnormal thrust angle, forcing the vehicle to travel at an angle down the road."
            }
        ],
        "contradictory_evidence": [
            "Rear thrust angle is 0.00 degrees on alignment rack and axle beam is perfectly straight"
        ]
    },
    "Slushbox": {
        "affected_component": "Hydraulic Automatic Planetary Transmission Assembly & Valve Body",
        "subsystem": "Automatic Transmission & Hydraulic Controls",
        "safety_level": "High",
        "required_expertise": "Professional Automotive Technician / ASE Specialist",
        "required_tools": [
            "Transmission Pressure Test Gauge Set (0-300 psi)",
            "OBD-II Transmission Live Data Scanner",
            "Fluid Catch Pan"
        ],
        "maintenance_actions": {
            "corrective_action": "Check ATF fluid level and color. Read transmission DTCs and line pressure. If friction clutches slip, gears drop out, or transmission fluid is black with burnt odor, perform transmission rebuild or install remanufactured assembly.",
            "preventive_maintenance": "Perform transmission fluid and filter drain-and-fill every 60,000-80,000 km.",
            "replacement_criteria": "Replace/rebuild transmission if clutch pack material is in the pan, gear slippage exceeds 200 RPM on scanner, or pump pressure is lost.",
            "do_not_replace_warning": "Verify shift linkages, range selector switch, and transmission solenoid wiring before condemning internal mechanical transmission failure."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_TRANS_SLIP_REV",
                "question": "When you step on the gas pedal to accelerate, does the engine rev up high like it is in Neutral while the car barely accelerates?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Engine revving without vehicle acceleration is the classic symptom of worn automatic transmission friction clutches slipping in the drum."
            }
        ],
        "contradictory_evidence": [
            "Transmission shifts gears firmly, decisively, and on-time without slipping or flare between shifts"
        ]
    },
    "Universal Joint": {
        "affected_component": "Cardan Universal Joint (U-Joint) Cross & Needle Bearing Caps",
        "subsystem": "Driveshaft Driveline Coupling",
        "safety_level": "High",
        "required_expertise": "Experienced Technician or Well-Equipped DIYer",
        "required_tools": [
            "U-Joint Press Tool / C-Clamp Press",
            "Needle Nose Pliers (for C-clips)",
            "Pry Bar"
        ],
        "maintenance_actions": {
            "corrective_action": "Inspect U-joint bearing seals for red rust powder ('rust bleed') indicating dry needle bearings. Grasp driveshaft and check for rotational free-play. Replace worn U-joint crosses and grease greaseable fittings.",
            "preventive_maintenance": "Grease greaseable U-joint Zerk fittings with chassis grease at every oil change interval.",
            "replacement_criteria": "Replace U-joint immediately if any rotational play, binding, or rust staining is present at bearing caps.",
            "do_not_replace_warning": "DRIVELINE SAFETY: A failing U-joint that snaps at highway speeds can drop the driveshaft onto the road, risking vehicle rollover."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_TRANS_UJOINT_CLINK",
                "question": "Do you hear a loud metallic 'CLINK' or 'PING' sound from under the floorboards when shifting from Drive to Reverse?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Rotational slack in worn U-joint needle bearings produces a distinct hollow metallic ringing clink when drivetrain torque reverses."
            }
        ],
        "contradictory_evidence": [
            "Driveshaft universal joints have zero rotational play and pivot smoothly with sealed, intact bearing boots"
        ]
    },
    "Viscous Coupling": {
        "affected_component": "AWD Viscous Coupling Multi-Plate Silicone Fluid Pack",
        "subsystem": "All-Wheel Drive Transfer & Torque Limiting",
        "safety_level": "High",
        "required_expertise": "Professional Automotive Technician / ASE Specialist",
        "required_tools": [
            "Torque Wrench",
            "Jack & Axle Stands",
            "Driveline Wrench Set"
        ],
        "maintenance_actions": {
            "corrective_action": "Elevate vehicle on stands. Turn one wheel by hand while measuring resistance required to slip viscous unit. If coupling is locked solid (causing severe tire scrubbing on turns) or slips freely with zero torque transfer, replace viscous coupling.",
            "preventive_maintenance": "Maintain identical tire rolling radius on all 4 wheels; mismatched tire circumference continuously overheats viscous fluid.",
            "replacement_criteria": "Replace coupling if internal dilatant silicone fluid has overheated and permanently locked the friction plates together.",
            "do_not_replace_warning": "A locked viscous coupling mimics a bad rear differential; test the coupling isolated from the differential carrier before replacing."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_TRANS_VISCOUS_LOCK",
                "question": "Does the car feel heavily resisted or jerky when maneuvering into a tight parking stall, as if the brakes are dragging?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Overheated viscous couplings lock solid, forcing the front and rear axles to turn at identical speeds and resisting parking maneuvers."
            }
        ],
        "contradictory_evidence": [
            "Viscous coupling allows smooth progressive torque transfer with zero driveline bind on tight dry pavement turns"
        ]
    },
    "Clutch Master Cylinder": {
        "affected_component": "Foot-Operated Hydraulic Clutch Master Cylinder & Pushrod",
        "subsystem": "Manual Transmission Clutch Hydraulics",
        "safety_level": "High",
        "required_expertise": "Experienced Technician or Well-Equipped DIYer",
        "required_tools": [
            "Flare Nut Wrench (10mm/11mm)",
            "Clutch Hydraulic Bleeding Hose",
            "Catch Container"
        ],
        "maintenance_actions": {
            "corrective_action": "Inspect driver floorboard carpet above clutch pedal arm for leaking brake fluid running down pedal pushrod. If fluid leaks or pedal sinks to floor without disengaging clutch, replace clutch master cylinder and bleed hydraulic circuit.",
            "preventive_maintenance": "Flush clutch hydraulic fluid every 2 years to prevent moisture scoring on master cylinder aluminum piston bore.",
            "replacement_criteria": "Replace if piston seal leaks fluid internally or externally, causing clutch drag or incomplete clutch disengagement.",
            "do_not_replace_warning": "Always bench-bleed new clutch master cylinder before installation on vehicle to purge trapped air from upper cylinder bore."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_TRANS_CMC_LEAK_PEDAL",
                "question": "Is the clutch pedal arm damp with oily fluid under the driver dashboard, or does the pedal stay stuck down on the carpet?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Master cylinder primary cup failure leaks fluid past the pushrod boot down into the cabin footwell, leaving the pedal stuck down."
            }
        ],
        "contradictory_evidence": [
            "Clutch master cylinder pushrod is completely dry and pedal disengages clutch cleanly at mid-stroke"
        ]
    },
    "Torque Converter": {
        "affected_component": "Hydrodynamic Fluid Torque Converter & Internal Lockup Clutch",
        "subsystem": "Automatic Transmission Torque Coupling",
        "safety_level": "High",
        "required_expertise": "Professional Automotive Technician / ASE Specialist",
        "required_tools": [
            "Transmission Pressure Test Gauge",
            "Scan Tool TCC Slip RPM Live Graph",
            "Engine Support Fixture"
        ],
        "maintenance_actions": {
            "corrective_action": "Graph Torque Converter Clutch (TCC) slip RPM on scanner while driving at 80 km/h (slip should be 0-20 RPM when locked). If TCC shudders like driving over rumble strips, perform transmission fluid flush with friction modifier. If internal stator clutch or lockup disc is burnt, replace torque converter.",
            "preventive_maintenance": "Change automatic transmission fluid on schedule; degraded ATF causes torque converter lockup clutch shudder.",
            "replacement_criteria": "Replace converter if lockup clutch slips continuously (code P0741), stator one-way clutch is seized, or stall test RPM is out of specification.",
            "do_not_replace_warning": "A shudder that feels like driving over highway rumble strips at 60-80 km/h is often cured with fresh OEM fluid and anti-shudder additive."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_TRANS_TCC_SHUDDER",
                "question": "Do you feel a brief, violent vehicle shudder (like driving over rumble strips on the highway edge) when shifting into top overdrive gear?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Glazed torque converter lockup friction lining chatters as the hydraulic lockup piston applies, transmitting severe drivetrain vibration."
            }
        ],
        "contradictory_evidence": [
            "Torque converter lockup engages smoothly with zero shudder and slip RPM drops to 0 RPM on highway cruise"
        ]
    },
    "Transmission Fluid": {
        "affected_component": "Automatic / Manual Transmission Lubrication & Hydraulic Operating Fluid",
        "subsystem": "Transmission Hydraulic & Lubrication Circuit",
        "safety_level": "High",
        "required_expertise": "General Mechanic or Intermediate DIYer",
        "required_tools": [
            "Transmission Dipstick / Level Check Plug Tool",
            "Drain Pan",
            "Fluid Transfer Pump & Spec ATF"
        ],
        "maintenance_actions": {
            "corrective_action": "Check transmission fluid level at operating temperature with engine idling (or via side overflow plug on sealed units). Check fluid color: should be bright translucent red. If dark brown or smelling like burnt toast, drain pan, clean magnets, and refill with fresh OEM-spec fluid.",
            "preventive_maintenance": "Check transmission fluid level every 10,000 km; drain and refill every 60,000-80,000 km.",
            "replacement_criteria": "Drain and refill immediately if fluid is dark brown, opaque black, smells burnt, or contains friction particulate sheen.",
            "do_not_replace_warning": "Low fluid level causes delayed gear engagement and harsh slamming shifts; always verify fluid level before condemning transmission internals."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_TRANS_FLUID_BURNT_SMELL",
                "question": "Is the transmission fluid on the dipstick dark brown or black, with a sharp, acrid burnt toast odor?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "Burnt transmission fluid indicates severe clutch overheating and thermal breakdown of hydraulic friction modifiers."
            }
        ],
        "contradictory_evidence": [
            "Transmission fluid is bright pink/red, translucent, smells clean, and sits precisely at the HOT level mark"
        ]
    },
    "Transmission Filter": {
        "affected_component": "Automatic Transmission Fluid Suction Filter & Pan Neodymium Magnets",
        "subsystem": "Transmission Hydraulic Filtration",
        "safety_level": "Medium",
        "required_expertise": "General Mechanic or Intermediate DIYer",
        "required_tools": [
            "Transmission Pan Socket Set (10mm/12mm)",
            "Torque Wrench",
            "Replacement Pan Gasket",
            "Drain Pan"
        ],
        "maintenance_actions": {
            "corrective_action": "Drop transmission oil pan. Clean metallic sludge from pan bottom and wipe collection magnets clean. Unbolt old filter pickup and install fresh filter with new rubber O-ring seal. Reinstall pan with new gasket and torque bolts to 8-10 Nm.",
            "preventive_maintenance": "Replace transmission filter whenever performing an automatic transmission fluid service.",
            "replacement_criteria": "Replace filter whenever transmission pan is removed; replace immediately if filter media is clogged with clutch friction material.",
            "do_not_replace_warning": "Ensure the rubber neck O-ring of the old filter came out of the transmission pump bore; leaving two O-rings causes pump cavitation and no drive."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_TRANS_FILTER_WHINE_COLD",
                "question": "Does the transmission emit a loud buzzing or whining noise upon cold startup that fades as the car warms up?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "A clogged suction filter restricts oil flow to the transmission front pump, causing severe hydraulic cavitation whine on cold viscous fluid."
            }
        ],
        "contradictory_evidence": [
            "Transmission oil pan is clean, magnets have only normal fine gray fuzz, and pump draws fluid with zero cavitation whine"
        ]
    },
    "Transmission Solenoid": {
        "affected_component": "Electronic Transmission Shift / Line Pressure Pulse-Width Solenoid Pack",
        "subsystem": "Transmission Electro-Hydraulic Valve Body",
        "safety_level": "High",
        "required_expertise": "Experienced Technician or Well-Equipped DIYer",
        "required_tools": [
            "Digital Multimeter (Ohms test)",
            "OBD-II Scan Tool (Transmission PID data)",
            "Valve Body Torx Bit Set"
        ],
        "maintenance_actions": {
            "corrective_action": "Read transmission diagnostic fault codes (e.g. P0750, P0755 shift solenoid codes). Measure solenoid electrical resistance through transmission case connector (typically 10-25 ohms). Drop pan, unbolt defective solenoid, and install fresh solenoid.",
            "preventive_maintenance": "Keep transmission fluid clean; fine metallic debris in old fluid jams electromagnetic solenoid pintles.",
            "replacement_criteria": "Replace solenoid if internal resistance is out of spec or scan tool confirms electrical open/short in circuit.",
            "do_not_replace_warning": "Test the transmission wiring harness and case pass-through connector pins for corrosion before dropping the transmission pan."
        },
        "diagnostic_questions": [
            {
                "question_id": "Q_TRANS_LIMP_MODE",
                "question": "Is the automatic transmission locked in 'Limp-In' mode (locked in 3rd gear only, refusing to shift up or down)?",
                "options": [
                    "Yes",
                    "No",
                    "Not Sure"
                ],
                "supporting_answer": "Yes",
                "contradictory_answer": "No",
                "context": "When the transmission control module detects a shift solenoid circuit electrical failure, it commands limp mode (3rd gear) to prevent internal damage."
            }
        ],
        "contradictory_evidence": [
            "All shift solenoids click sharply on scan tool active test and transmission cycles through all gears seamlessly"
        ]
    }
}
