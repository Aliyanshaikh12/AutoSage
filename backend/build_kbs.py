"""Build the structured Auto Sage Knowledge Base from new_kbs_dataset.

Source dataset:
  - D:\\CARFAULTDIA\\new_kbs_dataset\\automotive_faults_aktc_obike_et_al.json
  - D:\\CARFAULTDIA\\new_kbs_dataset\\brake_faults_flowchart.png
  - D:\\CARFAULTDIA\\new_kbs_dataset\\electrical_faults_flowchart.png
  - D:\\CARFAULTDIA\\new_kbs_dataset\\engine_overheating_flowchart.png
  - D:\\CARFAULTDIA\\new_kbs_dataset\\transmission_faults_flowchart.png

Dataset citation & license:
  Obike, Peter, and Okure Obot (2025). "Automotive Faults Dataset for Diagnostic
  and Maintenance Systems." Zenodo. DOI: 10.5281/zenodo.15626055. Licensed under
  Creative Commons Attribution 4.0 International (CC BY 4.0).
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from rule_enrichment import RULE_ENRICHMENT_BY_SUBCATEGORY

PROJECT_ROOT = BACKEND_DIR.parent
RAW_DATASET_DIR = PROJECT_ROOT / "new_kbs_dataset"
RAW_JSON_PATH = RAW_DATASET_DIR / "automotive_faults_aktc_obike_et_al.json"
OUTPUT_KB_PATH = BACKEND_DIR / "data" / "kbs_knowledge_base.json"

DATASET_PROVENANCE = {
    "title": "Automotive Faults Dataset for Diagnostic and Maintenance Systems",
    "authors": ["Peter Obike (Data Collector)", "Okure Obot (Data Curator)"],
    "organization": "AKTC / University Research Dataset",
    "doi": "10.5281/zenodo.15626055",
    "url": "https://doi.org/10.5281/zenodo.15626055",
    "related_publication": (
        "Obot, Okure, and Peter Obike (2024). 'An Integrated Fuzzy-Rule and "
        "Case-Based Reasoning System for Enhanced Automobile Maintenance and "
        "Repair.' Journal of Engineering Research and Reports, 26(8), 433-445. "
        "DOI: 10.9734/jerr/2024/v26i81256"
    ),
    "license": "Creative Commons Attribution 4.0 International (CC BY 4.0)",
    "license_url": "https://creativecommons.org/licenses/by/4.0/",
}

CATEGORY_DEFINITIONS: list[dict[str, Any]] = [
    {
        "category_id": "CAT_ENGINE",
        "name": "Engine & Fuel System",
        "short_name": "Engine & Fuel",
        "icon": "engineering",
        "description": (
            "Engine misfires, rough or stalling idle, loss of power, poor acceleration, "
            "exhaust smoke, oil leaks or oil pressure warnings, engine belts, and fuel delivery faults."
        ),
        "source_categories": ["Engine Components", "Engine Compartment", "Fuel System"],
        "safety_note": (
            "Stop driving immediately if the low oil pressure warning light illuminates, "
            "if you smell raw fuel or see a fuel leak, or if severe engine knocking occurs."
        ),
    },
    {
        "category_id": "CAT_ELECTRICAL",
        "name": "Starting, Battery & Electrical",
        "short_name": "Electrical & Starting",
        "icon": "bolt",
        "description": (
            "No-crank or slow cranking on startup, clicking sounds when turning the key, "
            "battery warning light, dim or failed headlights, ignition wires, wipers, washer spray, windows, locks, and horn."
        ),
        "source_categories": ["Electrical System", "Liquid Systems (Windshield Washer Fluid)"],
        "safety_note": (
            "Turn off the ignition and disconnect the negative battery terminal before probing "
            "high-current starter or charging cables, and wear eye protection around lead-acid batteries."
        ),
    },
    {
        "category_id": "CAT_BRAKES",
        "name": "Braking & ABS System",
        "short_name": "Braking & ABS",
        "icon": "disc_full",
        "description": (
            "Soft, spongy, or hard brake pedal, squealing brakes, pedal pulsation, steering vibration under braking, "
            "pulling or dragging brakes, brake fluid leaks, and ABS or brake warning lights."
        ),
        "source_categories": ["ABS System", "Liquid Systems (Brake Fluid)"],
        "safety_note": (
            "CRITICAL SAFETY WARNING: Do not drive the vehicle if the brake pedal feels soft/spongy, "
            "sinks toward the floor, or if active brake fluid leakage is visible."
        ),
    },
    {
        "category_id": "CAT_COOLING",
        "name": "Cooling & Cabin Heating",
        "short_name": "Cooling System",
        "icon": "thermostat",
        "description": (
            "Engine overheating, temperature gauge in the red zone, coolant leaks under the vehicle, "
            "sweet coolant smell in the cabin, no cabin heat, radiator, cooling fan, hoses, and water pump."
        ),
        "source_categories": ["Cooling System", "Liquid Systems (Coolant Reservoir, Radiator)"],
        "safety_note": (
            "THERMAL BURN HAZARD: Never open a radiator or pressurized coolant reservoir cap while "
            "the engine is hot. Shut off an overheating engine safely and allow it to cool completely."
        ),
    },
    {
        "category_id": "CAT_TRANSMISSION",
        "name": "Transmission, Clutch & Drivetrain",
        "short_name": "Transmission",
        "icon": "settings",
        "description": (
            "Slipping gears, delayed or erratic shifting, transmission overheating, shuddering, "
            "soft or loose clutch pedal, driveline vibration, clunking, differential whine, and binding on turns."
        ),
        "source_categories": ["Transmission", "Drivetrain"],
        "safety_note": (
            "Secure the vehicle on level ground with wheel chocks before inspecting underbody "
            "transmission, clutch hydraulic, differential, or axle components."
        ),
    },
    {
        "category_id": "CAT_EMISSIONS",
        "name": "Exhaust & Emissions System",
        "short_name": "Emissions & Exhaust",
        "icon": "air",
        "description": (
            "Check engine light paired with rough idle, rotten-egg exhaust smell, fuel vapor odor, "
            "gas cap warning light, engine knocking/pinging, or loud exhaust manifold leaks."
        ),
        "source_categories": ["Emissions System"],
        "safety_note": (
            "CARBON MONOXIDE HAZARD: Never run an engine in an enclosed garage, and have cabin "
            "exhaust odors inspected immediately before driving with windows closed."
        ),
    },
    {
        "category_id": "CAT_HVAC",
        "name": "Air Conditioning & Ventilation",
        "short_name": "AC & Ventilation",
        "icon": "ac_unit",
        "description": (
            "No cold air or warm air from AC vents, weak or absent cabin airflow, musty vent odors, "
            "loud AC compressor or blower noises, and erratic HVAC fan speeds."
        ),
        "source_categories": ["Air Conditioning System"],
        "safety_note": (
            "AC refrigerant circuits are pressurized; leak repairs and refrigerant handling "
            "should be performed with proper recovery equipment."
        ),
    },
    {
        "category_id": "CAT_STEERING_TIRES",
        "name": "Steering, Wheels & Tires",
        "short_name": "Steering & Tires",
        "icon": "tire_repair",
        "description": (
            "Noise or stiff effort when turning the steering wheel, grinding or clicking noises from wheels, "
            "wheel wobbling, highway vibration with uneven tire wear, and TPMS tire-pressure warnings."
        ),
        "source_categories": ["Steering", "Wheels & Tires", "Liquid Systems (Power Steering Fluid)", "Drivetrain (Shaft and Tires)"],
        "safety_note": (
            "Do not drive at highway speeds if wheel wobbling, severe wheel grinding, or sudden "
            "steering stiffness is present; inspect lug nuts, wheel hubs, and tire inflation safely."
        ),
    },
]

# Raw 0-based indices excluded from fault rules because they represent maintenance services,
# generic diagnostic intake placeholders, circular gauge measurements, or exact duplicates.
EXCLUDED_RAW_RECORDS: dict[int, str] = {
    12: (
        "Excluded: 'AC Recharge' is a maintenance service rather than a component fault, and its "
        "input symptom ('Low AC system pressure') requires AC manifold gauges rather than user observation."
    ),
    13: (
        "Excluded: 'Air Conditioning Diagnosis' is a generic diagnostic scan placeholder "
        "('Check AC system components for proper operation') rather than a specific fault candidate."
    ),
    18: (
        "Excluded: 'Coolant Leak Diagnosis' is a generic leak-testing procedure redundant with specific "
        "Cooling System component rules (Radiator, Radiator Hose, Heater Hose, Water Pump, Coolant Reservoir)."
    ),
    37: (
        "Excluded: 'Check Engine Light Diagnosis' is a generic OBD-II code-scan intake entry rather than "
        "a specific fault; concrete Check Engine Light component rules are modeled under Emissions System."
    ),
    71: (
        "Excluded: 'Battery Charging' uses a voltmeter measurement ('Low voltage') as an input symptom "
        "and duplicates 'Charging System' (record #37) and 'Battery Replacement' (record #36)."
    ),
}

# Raw index 81 ('Fuel System -> Fuel Injector') is an exact duplicate of raw index 62
# ('Engine Components -> Fuel Injector') with identical symptoms and diagnosis steps.
MERGED_DUPLICATE_MAP: dict[int, int] = {
    81: 62,
}

# Canonical symptom normalization map (lowercased raw text -> canonical readable text).
SYMPTOM_NORMALIZATION: dict[str, str] = {
    "abs warning light on": "ABS warning light is on",
    "abs light stays on": "ABS warning light is on",
    "brake fluid leak": "Brake fluid leak",
    "brake fluid leaks": "Brake fluid leak",
    "soft brake pedal": "Soft or spongy brake pedal",
    "spongy brake pedal": "Soft or spongy brake pedal",
    "coolant leaks under the vehicle": "Coolant leak under vehicle",
    "visible coolant leak under vehicle": "Coolant leak under vehicle",
    "coolant leak under vehicle": "Coolant leak under vehicle",
    "coolant leak": "Coolant leak under vehicle",
    "coolant odor in cabin": "Sweet or coolant odor inside cabin",
    "sweet smell in cabin": "Sweet or coolant odor inside cabin",
    "clicking sound when starting": "Clicking sound when turning key to start",
    "clicking sound when key is turned": "Clicking sound when turning key to start",
    "weak airflow from vents": "Weak or reduced airflow from vents",
    "reduced airflow from vents": "Weak or reduced airflow from vents",
    "transmission slipping": "Transmission or gears slipping",
    "slipping gears": "Transmission or gears slipping",
    "gears slipping": "Transmission or gears slipping",
    "delay in gear engagement": "Delayed gear engagement or shifting",
    "delayed shifting": "Delayed gear engagement or shifting",
    "vehicle binding on turns": "Vehicle binding during turns",
    "vehicle binding during turns": "Vehicle binding during turns",
    "clutch pedal feels spongy": "Soft or spongy clutch pedal",
    "soft clutch pedal": "Soft or spongy clutch pedal",
    "loss of power": "Loss of engine power",
    "loss of engine power": "Loss of engine power",
    "decreased engine performance": "Decreased overall engine performance",
    "engine performance issues": "Decreased overall engine performance",
}

# Broad secondary warning/performance indicators that appear across many distinct faults
# and require at least one corroborating physical symptom to isolate a candidate rule.
BROAD_INDICATOR_LABELS: set[str] = {
    "Check engine light on",
    "Poor fuel economy",
}

# Subcategories whose two listed symptoms represent alternative severity levels of the same
# component malfunction (OR logic: either symptom satisfies the fault rule directly).
ANY_LOGIC_RAW_INDICES: set[int] = {
    16,  # Heater Blower Motor Resistor: erratic fan speed OR fan only works on certain settings
    38,  # Door Window Motor: window does not move OR moves intermittently
    40,  # Headlamp Bulb: headlight not working OR dim headlight
    45,  # Windshield Washer Pump: no washer fluid spray OR weak washer fluid spray
    46,  # Wiper Motor: wipers not working OR operate intermittently
    90,  # Windshield Washer Fluid: no washer fluid spray OR weak washer fluid spray
    95,  # Transmission Solenoid: erratic shifting OR won't shift gears
}

# Clarified fault titles where raw subcategory names use service labels or colloquialisms,
# while strictly preserving raw_subcategory in source provenance.
FAULT_TITLE_OVERRIDES: dict[int, str] = {
    17: "Low or Degraded Coolant / Antifreeze",
    19: "Thermostat or Radiator Blockage (Engine Cooling System)",
    32: "Automatic Transmission Assembly (Slushbox)",
    35: "Weak 12V Battery or Corroded Terminals (Battery Replacement)",
    36: "Alternator or Charging Belt Issue (Charging System)",
    57: "Turbocharger Boost / Intercooler Leak (Boost Pressure)",
    69: "Worn or Loose Cooling Fan Belt (Fan Belt)",
    72: "Worn or Misaligned Accessory Drive Belt (Engine Belt)",
    73: "Power Steering Pump or Fluid Leak (Steering Noise)",
    74: "Driveshaft Imbalance or Tire Condition (Shaft and Tires)",
    77: "Low or Degraded Engine Oil / Oil Leak (Engine Oil)",
    86: "Low or Contaminated Brake Fluid / Line Leak (Brake Fluid)",
    88: "Low Power Steering Fluid or Hose Leak (Power Steering Fluid)",
    90: "Low Windshield Washer Fluid or Pump Issue",
    93: "Low or Degraded Transmission Fluid / Pan Leak",
}

FLOWCHART_DEFINITIONS: list[dict[str, Any]] = [
    {
        "flowchart_id": "FC_BRAKES",
        "file_name": "brake_faults_flowchart.png",
        "title": "Brake Faults Diagnostic Flowchart",
        "category_id": "CAT_BRAKES",
        "root_node": "Brake Faults",
        "top_level_branches": [
            "Brake Pedal Soft",
            "Brake Noise",
            "Brake Fluid Leak",
            "ABS Light On",
        ],
        "detailed_branch": "Brake Pedal Soft",
        "trigger_symptom_labels": [
            "Soft or spongy brake pedal",
            "Brake fluid leak",
            "Squealing brakes",
            "ABS warning light is on",
        ],
        "coverage_note": (
            "In brake_faults_flowchart.png, four brake fault branches are listed under 'Brake Faults', "
            "and a complete 4-stage sequential decision tree is expanded under 'Brake Pedal Soft'."
        ),
        "decision_steps": [
            {
                "order": 1,
                "check": "Check Brake Fluid Level",
                "if_abnormal": "Low -> Refill brake fluid (and inspect why fluid dropped)",
                "if_normal": "Normal -> Proceed to Check for Brake Fluid Leaks",
            },
            {
                "order": 2,
                "check": "Check for Brake Fluid Leaks",
                "if_abnormal": "Leak found -> Repair leaks",
                "if_normal": "No leaks -> Proceed to Check Brake Pads and Rotors",
            },
            {
                "order": 3,
                "check": "Check Brake Pads and Rotors",
                "if_abnormal": "Worn -> Replace brake pads or rotors",
                "if_normal": "Good -> Proceed to Check Brake Master Cylinder",
            },
            {
                "order": 4,
                "check": "Check Brake Master Cylinder",
                "if_abnormal": "Faulty -> Replace master cylinder",
                "if_normal": "Working -> No further action required",
            },
        ],
    },
    {
        "flowchart_id": "FC_ELECTRICAL",
        "file_name": "electrical_faults_flowchart.png",
        "title": "Electrical & Starting Faults Flowchart",
        "category_id": "CAT_ELECTRICAL",
        "root_node": "Electrical Faults",
        "top_level_branches": [
            "Battery Dead",
            "Alternator Failure",
            "Starter Motor Issues",
            "Fuse Issues",
        ],
        "detailed_branch": "Battery Dead",
        "trigger_symptom_labels": [
            "Engine cranks slowly",
            "Clicking sound when turning key to start",
            "Engine does not crank",
            "Battery warning light on",
            "Dim headlights",
        ],
        "coverage_note": (
            "In electrical_faults_flowchart.png, four electrical branches are shown under 'Electrical Faults', "
            "and a 3-stage sequential decision tree is expanded under 'Battery Dead'."
        ),
        "decision_steps": [
            {
                "order": 1,
                "check": "Check Battery Terminals",
                "if_abnormal": "Corroded -> Clean terminals",
                "if_normal": "Clean -> Proceed to Check Battery Voltage",
            },
            {
                "order": 2,
                "check": "Check Battery Voltage",
                "if_abnormal": "Low voltage -> Charge or replace battery",
                "if_normal": "Normal voltage -> Proceed to Check Alternator Output",
            },
            {
                "order": 3,
                "check": "Check Alternator Output",
                "if_abnormal": "Low output -> Replace alternator",
                "if_normal": "Normal output -> No further action required",
            },
        ],
    },
    {
        "flowchart_id": "FC_OVERHEATING",
        "file_name": "engine_overheating_flowchart.png",
        "title": "Engine Overheating Diagnostic Flowchart",
        "category_id": "CAT_COOLING",
        "root_node": "Engine Overheating",
        "top_level_branches": ["Engine Overheating"],
        "detailed_branch": "Engine Overheating",
        "trigger_symptom_labels": [
            "Engine overheating",
            "Temperature gauge in red zone",
            "Coolant leak under vehicle",
            "Low coolant warning light",
        ],
        "coverage_note": (
            "In engine_overheating_flowchart.png, a complete 5-stage sequential decision pathway "
            "traces Coolant Level -> Radiator Fan -> Thermostat -> Radiator -> Head Gasket."
        ),
        "decision_steps": [
            {
                "order": 1,
                "check": "Check Coolant Level",
                "if_abnormal": "Low -> Refill coolant and check for leaks",
                "if_normal": "Normal -> Proceed to Check Radiator Fan Operation",
            },
            {
                "order": 2,
                "check": "Check Radiator Fan Operation",
                "if_abnormal": "Not working -> Check fan motor, relay, and fuse",
                "if_normal": "Working -> Proceed to Check Thermostat",
            },
            {
                "order": 3,
                "check": "Check Thermostat",
                "if_abnormal": "Stuck closed -> Replace thermostat",
                "if_normal": "Functioning normally -> Proceed to Inspect Radiator",
            },
            {
                "order": 4,
                "check": "Inspect Radiator",
                "if_abnormal": "Blocked or damaged -> Clean or replace radiator",
                "if_normal": "Clear -> Proceed to Check for Head Gasket Failure",
            },
            {
                "order": 5,
                "check": "Check for Head Gasket Failure",
                "if_abnormal": "Symptoms of failure -> Replace head gasket",
                "if_normal": "No symptoms -> No further action required",
            },
        ],
    },
    {
        "flowchart_id": "FC_TRANSMISSION",
        "file_name": "transmission_faults_flowchart.png",
        "title": "Transmission Faults Diagnostic Flowchart",
        "category_id": "CAT_TRANSMISSION",
        "root_node": "Transmission Faults",
        "top_level_branches": [
            "Slipping",
            "Noisy Operation",
            "Fluid Leaks",
            "Shifting Issues",
        ],
        "detailed_branch": "Slipping",
        "trigger_symptom_labels": [
            "Transmission or gears slipping",
            "Delayed gear engagement or shifting",
            "Erratic shifting",
            "Transmission won't shift gears",
            "Transmission overheating",
            "Shuddering during acceleration",
        ],
        "coverage_note": (
            "In transmission_faults_flowchart.png, four transmission fault branches are shown, "
            "and a 3-stage sequential decision pathway is expanded under 'Slipping'."
        ),
        "decision_steps": [
            {
                "order": 1,
                "check": "Check Transmission Fluid Level",
                "if_abnormal": "Low -> Refill fluid",
                "if_normal": "Normal -> Proceed to Check Transmission Fluid Condition",
            },
            {
                "order": 2,
                "check": "Check Transmission Fluid Condition",
                "if_abnormal": "Contaminated -> Replace fluid and filter",
                "if_normal": "Clean -> Proceed to Check for Internal Wear",
            },
            {
                "order": 3,
                "check": "Check for Internal Wear",
                "if_abnormal": "Signs of wear -> Repair or replace transmission",
                "if_normal": "No wear -> No further action required",
            },
        ],
    },
]


def _slugify(text: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", text.strip()).strip("_").upper()
    return cleaned


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _map_record_to_category_id(raw_category: str, raw_subcategory: str) -> str:
    if raw_category == "ABS System" or raw_subcategory == "Brake Fluid":
        return "CAT_BRAKES"
    if raw_category == "Cooling System" or raw_subcategory in {"Coolant Reservoir", "Radiator"}:
        return "CAT_COOLING"
    if raw_category == "Electrical System" or raw_subcategory == "Windshield Washer Fluid":
        return "CAT_ELECTRICAL"
    if raw_category in {"Transmission", "Drivetrain"} and raw_subcategory != "Shaft and Tires":
        return "CAT_TRANSMISSION"
    if raw_category == "Air Conditioning System":
        return "CAT_HVAC"
    if (
        raw_category in {"Steering", "Wheels & Tires"}
        or raw_subcategory in {"Power Steering Fluid", "Shaft and Tires"}
    ):
        return "CAT_STEERING_TIRES"
    if raw_category == "Emissions System":
        return "CAT_EMISSIONS"
    return "CAT_ENGINE"


def _canonical_symptom_label(raw_symptom: str) -> str:
    trimmed = raw_symptom.strip()
    return SYMPTOM_NORMALIZATION.get(trimmed.lower(), trimmed)


def build_knowledge_base() -> dict[str, Any]:
    if not RAW_JSON_PATH.exists():
        raise FileNotFoundError(f"Missing primary dataset file: {RAW_JSON_PATH}")

    raw_records: list[dict[str, Any]] = json.loads(RAW_JSON_PATH.read_text(encoding="utf-8"))
    json_sha256 = _sha256_file(RAW_JSON_PATH)

    # Verify all 4 flowcharts exist and hash them
    flowchart_files_meta: list[dict[str, Any]] = []
    for fc in FLOWCHART_DEFINITIONS:
        fc_path = RAW_DATASET_DIR / fc["file_name"]
        if not fc_path.exists():
            raise FileNotFoundError(f"Missing dataset flowchart image: {fc_path}")
        flowchart_files_meta.append(
            {
                "flowchart_id": fc["flowchart_id"],
                "file_name": fc["file_name"],
                "size_bytes": fc_path.stat().st_size,
                "sha256": _sha256_file(fc_path),
            }
        )

    # Track merged provenance for duplicate records
    extra_sources_by_primary: dict[int, list[dict[str, Any]]] = {}
    for dup_idx, primary_idx in MERGED_DUPLICATE_MAP.items():
        dup_rec = raw_records[dup_idx]
        extra_sources_by_primary.setdefault(primary_idx, []).append(
            {
                "raw_index_0based": dup_idx,
                "source_record_id": f"SRC_JSON_{dup_idx + 1:03d}",
                "raw_category": dup_rec["category"],
                "raw_subcategory": dup_rec["subcategory"],
            }
        )

    excluded_entries: list[dict[str, Any]] = []
    for ex_idx, reason in sorted(EXCLUDED_RAW_RECORDS.items()):
        rec = raw_records[ex_idx]
        excluded_entries.append(
            {
                "raw_index_0based": ex_idx,
                "source_record_id": f"SRC_JSON_{ex_idx + 1:03d}",
                "raw_category": rec["category"],
                "raw_subcategory": rec["subcategory"],
                "raw_symptoms": rec["symptoms"],
                "disposition": "excluded",
                "reason": reason,
            }
        )
    for dup_idx, primary_idx in sorted(MERGED_DUPLICATE_MAP.items()):
        rec = raw_records[dup_idx]
        excluded_entries.append(
            {
                "raw_index_0based": dup_idx,
                "source_record_id": f"SRC_JSON_{dup_idx + 1:03d}",
                "raw_category": rec["category"],
                "raw_subcategory": rec["subcategory"],
                "raw_symptoms": rec["symptoms"],
                "disposition": f"merged_into_SRC_JSON_{primary_idx + 1:03d}",
                "reason": (
                    f"Exact duplicate of record #{primary_idx + 1} "
                    f"({raw_records[primary_idx]['category']} -> {raw_records[primary_idx]['subcategory']}) "
                    "with identical symptoms and diagnostic steps."
                ),
            }
        )

    # First pass: collect canonical symptoms
    symptom_registry: dict[str, dict[str, Any]] = {}
    for idx, rec in enumerate(raw_records):
        if idx in EXCLUDED_RAW_RECORDS or idx in MERGED_DUPLICATE_MAP:
            continue
        cat_id = _map_record_to_category_id(rec["category"], rec["subcategory"])
        for raw_sym in rec["symptoms"]:
            canon_label = _canonical_symptom_label(raw_sym)
            sym_id = f"SYM_{_slugify(canon_label)}"
            entry = symptom_registry.setdefault(
                sym_id,
                {
                    "symptom_id": sym_id,
                    "label": canon_label,
                    "text": canon_label,
                    "source_variants": [],
                    "category_ids": [],
                    "related_subcategories": [],
                    "broad_indicator": canon_label in BROAD_INDICATOR_LABELS,
                },
            )
            if raw_sym.strip() not in entry["source_variants"]:
                entry["source_variants"].append(raw_sym.strip())
            if cat_id not in entry["category_ids"]:
                entry["category_ids"].append(cat_id)
            if rec["subcategory"] not in entry["related_subcategories"]:
                entry["related_subcategories"].append(rec["subcategory"])

    # Enrich symptoms with non-invented helper descriptions summarizing which subsystem checks reference them
    for sym_entry in symptom_registry.values():
        subs = sym_entry["related_subcategories"]
        if len(subs) == 1:
            sym_entry["description"] = (
                f"Associated in the knowledge base with {subs[0]} inspection."
            )
        elif len(subs) <= 3:
            sym_entry["description"] = (
                f"Associated in the knowledge base with {', '.join(subs)} checks."
            )
        else:
            preview = ", ".join(subs[:3])
            sym_entry["description"] = (
                f"Shared symptom across {len(subs)} fault rules (including {preview}). "
                + (
                    "Select any additional symptoms you notice to narrow down candidates."
                    if sym_entry["broad_indicator"]
                    else "Combine with any other observed symptoms for stronger isolation."
                )
            )
        sym_entry["rule_count"] = len(subs)

    # Map flowcharts with resolved symptom IDs
    label_to_sym_id = {v["label"].lower(): k for k, v in symptom_registry.items()}
    flowcharts_out: list[dict[str, Any]] = []
    flowchart_by_hash = {m["flowchart_id"]: m for m in flowchart_files_meta}
    for fc in FLOWCHART_DEFINITIONS:
        trigger_ids = [
            label_to_sym_id[lbl.lower()]
            for lbl in fc["trigger_symptom_labels"]
            if lbl.lower() in label_to_sym_id
        ]
        meta = flowchart_by_hash[fc["flowchart_id"]]
        flowcharts_out.append(
            {
                "flowchart_id": fc["flowchart_id"],
                "title": fc["title"],
                "file_name": fc["file_name"],
                "category_id": fc["category_id"],
                "source_type": "flowchart",
                "sha256": meta["sha256"],
                "size_bytes": meta["size_bytes"],
                "root_node": fc["root_node"],
                "top_level_branches": fc["top_level_branches"],
                "detailed_branch": fc["detailed_branch"],
                "trigger_symptom_ids": trigger_ids,
                "coverage_note": fc["coverage_note"],
                "decision_steps": fc["decision_steps"],
            }
        )

    cat_by_id = {c["category_id"]: c for c in CATEGORY_DEFINITIONS}
    fc_by_cat = {fc["category_id"]: fc for fc in flowcharts_out}

    # Second pass: build explicit IF-THEN fault rules
    rules_out: list[dict[str, Any]] = []
    per_cat_counter: dict[str, int] = {}

    cat_prefix_map = {
        "CAT_ENGINE": "ENG",
        "CAT_ELECTRICAL": "ELEC",
        "CAT_BRAKES": "BRK",
        "CAT_COOLING": "COOL",
        "CAT_TRANSMISSION": "TRANS",
        "CAT_EMISSIONS": "EMIS",
        "CAT_HVAC": "HVAC",
        "CAT_STEERING_TIRES": "STR",
    }

    for idx, rec in enumerate(raw_records):
        if idx in EXCLUDED_RAW_RECORDS or idx in MERGED_DUPLICATE_MAP:
            continue

        cat_id = _map_record_to_category_id(rec["category"], rec["subcategory"])
        cat_meta = cat_by_id[cat_id]
        per_cat_counter[cat_id] = per_cat_counter.get(cat_id, 0) + 1
        seq = per_cat_counter[cat_id]
        prefix = cat_prefix_map[cat_id]
        rule_id = f"RULE_{prefix}_{seq:03d}"
        fault_id = f"FAULT_{_slugify(rec['subcategory'])}"

        canon_sym_ids: list[str] = []
        canon_sym_labels: list[str] = []
        for raw_sym in rec["symptoms"]:
            lbl = _canonical_symptom_label(raw_sym)
            sid = f"SYM_{_slugify(lbl)}"
            if sid not in canon_sym_ids:
                canon_sym_ids.append(sid)
                canon_sym_labels.append(lbl)

        # Determine explicit rule logic mode
        if idx == 2:
            # Brake Booster lists 'Spongy brake pedal' and 'Hard brake pedal', which are
            # physically alternative pedal states; 'Hard brake pedal' directly satisfies it,
            # while 'Soft or spongy brake pedal' alone evaluates it as a partial candidate.
            logic_mode = "PRIMARY_OR_PARTIAL"
            primary_direct_ids = [label_to_sym_id["hard brake pedal"]]
        elif idx in ANY_LOGIC_RAW_INDICES or len(canon_sym_ids) == 1:
            logic_mode = "ANY"
            primary_direct_ids = list(canon_sym_ids)
        else:
            logic_mode = "ALL"
            primary_direct_ids = []

        if len(canon_sym_labels) == 1:
            rule_expression = (
                f'IF "{canon_sym_labels[0]}" THEN Possible Fault Candidate = "{FAULT_TITLE_OVERRIDES.get(idx, rec["subcategory"])}"'
            )
        elif logic_mode == "ANY":
            joined = '" OR "'.join(canon_sym_labels)
            rule_expression = (
                f'IF "{joined}" THEN Possible Fault Candidate = "{FAULT_TITLE_OVERRIDES.get(idx, rec["subcategory"])}"'
            )
        elif logic_mode == "PRIMARY_OR_PARTIAL":
            rule_expression = (
                f'IF "Hard brake pedal" (or partial pedal-assist check on "Soft or spongy brake pedal") '
                f'THEN Possible Fault Candidate = "{FAULT_TITLE_OVERRIDES.get(idx, rec["subcategory"])}"'
            )
        else:
            joined = '" AND "'.join(canon_sym_labels)
            rule_expression = (
                f'IF "{joined}" THEN Possible Fault Candidate = "{FAULT_TITLE_OVERRIDES.get(idx, rec["subcategory"])}"'
            )

        structured_steps: list[dict[str, Any]] = []
        abnormal_findings: list[str] = []
        recommended_checks: list[str] = []
        for step_idx, raw_step in enumerate(rec["diagnosis_steps"], start=1):
            step_text = raw_step["step"].strip()
            results_list = raw_step.get("result") or []
            abnormal = results_list[0].strip() if len(results_list) >= 1 else "Fault detected"
            normal = results_list[1].strip() if len(results_list) >= 2 else "Within normal condition"
            structured_steps.append(
                {
                    "step_number": step_idx,
                    "step": step_text,
                    "abnormal_result": abnormal,
                    "normal_result": normal,
                }
            )
            abnormal_findings.append(f"{abnormal} ({step_text.lower()})")
            recommended_checks.append(
                f"Step {step_idx}: {step_text} — check whether finding is '{abnormal}' vs. '{normal}'."
            )

        title = FAULT_TITLE_OVERRIDES.get(idx, rec["subcategory"])
        possible_fault = f"Possible {title} issue" if "issue" not in title.lower() else f"Possible {title}"

        suggested_next_steps = (
            f"Perform the {len(structured_steps)} diagnostic verification checks in order "
            f"({'; '.join(s['step'] for s in structured_steps)}). "
            f"Only service or replace {rec['subcategory']} components if physical inspection confirms "
            f"{' or '.join(repr(s['abnormal_result']) for s in structured_steps)}."
        )

        # Link complementary flowchart if this rule's category and symptoms intersect a flowchart
        linked_fc_id = None
        cat_fc = fc_by_cat.get(cat_id)
        if cat_fc and any(sid in cat_fc["trigger_symptom_ids"] for sid in canon_sym_ids):
            linked_fc_id = cat_fc["flowchart_id"]

        source_record_ids = [f"SRC_JSON_{idx + 1:03d}"]
        raw_categories = [rec["category"]]
        raw_indices = [idx]
        for extra in extra_sources_by_primary.get(idx, []):
            source_record_ids.append(extra["source_record_id"])
            if extra["raw_category"] not in raw_categories:
                raw_categories.append(extra["raw_category"])
            raw_indices.append(extra["raw_index_0based"])

        enrichment = RULE_ENRICHMENT_BY_SUBCATEGORY.get(rec["subcategory"], {})
        affected_component = enrichment.get("affected_component", title)
        subsystem = enrichment.get("subsystem", cat_meta["name"])
        safety_level = enrichment.get("safety_level", "Medium")
        required_expertise = enrichment.get("required_expertise", "Experienced Technician or Well-Equipped DIYer")
        required_tools = enrichment.get("required_tools", ["Digital Multimeter", "Basic Hand Tools"])
        maintenance_actions = enrichment.get(
            "maintenance_actions",
            {
                "corrective_action": suggested_next_steps,
                "preventive_maintenance": "Follow regular service schedule.",
                "replacement_criteria": "Replace if component fails physical bench inspection.",
                "do_not_replace_warning": "Do not replace without confirmed physical findings.",
            },
        )
        diagnostic_questions = enrichment.get("diagnostic_questions", [])
        contradictory_evidence = enrichment.get("contradictory_evidence", [])

        rules_out.append(
            {
                "rule_id": rule_id,
                "fault_id": fault_id,
                "category_id": cat_id,
                "category_name": cat_meta["name"],
                "title": title,
                "possible_fault": possible_fault,
                "subcategory": rec["subcategory"],
                "affected_component": affected_component,
                "subsystem": subsystem,
                "safety_level": safety_level,
                "required_expertise": required_expertise,
                "required_tools": required_tools,
                "maintenance_actions": maintenance_actions,
                "diagnostic_questions": diagnostic_questions,
                "contradictory_evidence": contradictory_evidence,
                "system_hierarchy": {
                    "system": cat_meta["name"],
                    "subsystem": subsystem,
                    "component": affected_component,
                    "fault": possible_fault,
                },
                "logic_mode": logic_mode,
                "symptom_ids": canon_sym_ids,
                "symptom_labels": canon_sym_labels,
                "primary_direct_symptom_ids": primary_direct_ids,
                "raw_symptoms": rec["symptoms"],
                "rule_expression": rule_expression,
                "diagnosis_steps": structured_steps,
                "possible_causes": abnormal_findings,
                "recommended_checks": recommended_checks,
                "suggested_next_steps": suggested_next_steps,
                "safety_warning": cat_meta["safety_note"],
                "related_flowchart_id": linked_fc_id,
                "source_type": "json_dataset",
                "source_reference": {
                    "dataset_title": DATASET_PROVENANCE["title"],
                    "doi": DATASET_PROVENANCE["doi"],
                    "url": DATASET_PROVENANCE["url"],
                    "license": DATASET_PROVENANCE["license"],
                    "source_file": "automotive_faults_aktc_obike_et_al.json",
                    "source_record_ids": source_record_ids,
                    "raw_indices_0based": raw_indices,
                    "raw_categories": raw_categories,
                    "raw_subcategory": rec["subcategory"],
                },
            }
        )

    # Finalize category metadata with exact rule and symptom counts
    categories_out: list[dict[str, Any]] = []
    for cat_def in CATEGORY_DEFINITIONS:
        cid = cat_def["category_id"]
        cat_rules = [r for r in rules_out if r["category_id"] == cid]
        cat_sym_ids = sorted(
            {sid for r in cat_rules for sid in r["symptom_ids"]},
            key=lambda s: symptom_registry[s]["label"].lower(),
        )
        cat_fc = fc_by_cat.get(cid)
        categories_out.append(
            {
                "category_id": cid,
                "name": cat_def["name"],
                "short_name": cat_def["short_name"],
                "icon": cat_def["icon"],
                "description": cat_def["description"],
                "source_categories": cat_def["source_categories"],
                "safety_note": cat_def["safety_note"],
                "rule_count": len(cat_rules),
                "symptom_count": len(cat_sym_ids),
                "symptom_ids": cat_sym_ids,
                "flowchart_id": cat_fc["flowchart_id"] if cat_fc else None,
            }
        )

    symptoms_sorted = sorted(
        symptom_registry.values(),
        key=lambda item: item["label"].lower(),
    )

    kb_payload = {
        "schema_version": 2,
        "system_type": "symptom_rule_kbs",
        "dataset": {
            **DATASET_PROVENANCE,
            "raw_json_file": "new_kbs_dataset/automotive_faults_aktc_obike_et_al.json",
            "raw_json_sha256": json_sha256,
            "raw_record_count": len(raw_records),
            "integrated_rule_count": len(rules_out),
            "merged_duplicate_count": len(MERGED_DUPLICATE_MAP),
            "excluded_record_count": len(EXCLUDED_RAW_RECORDS),
            "category_count": len(categories_out),
            "canonical_symptom_count": len(symptoms_sorted),
            "flowchart_count": len(flowcharts_out),
        },
        "categories": categories_out,
        "symptoms": symptoms_sorted,
        "rules": rules_out,
        "flowcharts": flowcharts_out,
        "excluded_source_records": excluded_entries,
    }

    OUTPUT_KB_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_KB_PATH.write_text(
        json.dumps(kb_payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return kb_payload


if __name__ == "__main__":
    kb = build_knowledge_base()
    ds = kb["dataset"]
    print(
        f"Built kbs_knowledge_base.json successfully: "
        f"{ds['category_count']} categories, "
        f"{ds['integrated_rule_count']} fault rules, "
        f"{ds['canonical_symptom_count']} canonical symptoms, "
        f"{ds['flowchart_count']} flowcharts "
        f"(from {ds['raw_record_count']} raw records; "
        f"{ds['merged_duplicate_count']} merged duplicate, "
        f"{ds['excluded_record_count']} excluded)."
    )
