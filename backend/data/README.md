# Auto Sage Knowledge Base Data

Active knowledge base file loaded by the inference engine:

- `kbs_knowledge_base.json` — Consolidated symptom-based Knowledge-Based System JSON.
  - **Schema Version**: 2
  - **8 Problem Categories**: Engine & Fuel, Starting/Electrical, Braking & ABS, Cooling System, Transmission/Clutch, Emissions & Exhaust, AC & Ventilation, Steering/Tires.
  - **93 Fault Rules**: Deterministic IF–THEN rules grounded directly in dataset records (`RULE_ENG_001` through `RULE_STR_006`).
  - **120 Canonical Symptoms**: Standardized symptom labels with rule counts and subsystem associations.
  - **4 Expert Diagnostic Flowcharts**: Sequential decision pathways linking to flowcharts in `new_kbs_dataset/`:
    - `FC_BRAKES` (`brake_faults_flowchart.png`)
    - `FC_ELECTRICAL` (`electrical_faults_flowchart.png`)
    - `FC_OVERHEATING` (`engine_overheating_flowchart.png`)
    - `FC_TRANSMISSION` (`transmission_faults_flowchart.png`)

## Primary Dataset Source & Citation

- **Title**: *Automotive Faults Dataset for Diagnostic and Maintenance Systems*
- **Authors**: Peter Obike (Data Collector), Okure Obot (Data Curator)
- **Zenodo DOI**: `10.5281/zenodo.15626055` ([https://doi.org/10.5281/zenodo.15626055](https://doi.org/10.5281/zenodo.15626055))
- **Related Paper**: Obot, O., & Obike, P. (2024), *Journal of Engineering Research and Reports*, 26(8), 433–445 (`10.9734/jerr/2024/v26i81256`).
- **License**: Creative Commons Attribution 4.0 International (CC BY 4.0).

## Rebuilding the Knowledge Base

To rebuild `kbs_knowledge_base.json` deterministically from `new_kbs_dataset/automotive_faults_aktc_obike_et_al.json`:

```bash
.\.venv\Scripts\python.exe backend\build_kbs.py
```

## Validating Integrity

To run the automated referential integrity check:

```bash
.\.venv\Scripts\python.exe backend\validate_knowledge_base.py
```
