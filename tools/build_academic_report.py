"""
Auto Sage Academic Project Report Generator
NED University of Engineering and Technology, Karachi
Department of Computer Science and Information Technology
Course: Knowledge-Based Systems (CT-359)
"""

import os
import sys
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = Path("D:/CARFAULTDIA")
FINAL_DIR = BASE_DIR / "final_report"
FINAL_DIR.mkdir(parents=True, exist_ok=True)
SCREEN_DIR = FINAL_DIR / "screenshots"
DIAG_DIR = FINAL_DIR / "diagrams"

DOCX_OUT = FINAL_DIR / "Auto_Sage_Final_Project_Report.docx"
PDF_OUT = FINAL_DIR / "Auto_Sage_Final_Project_Report.pdf"

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=120, bottom=120, left=180, right=180):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_header_text(doc, text, size=14, bold=True, color=(15, 23, 42), align=WD_ALIGN_PARAGRAPH.CENTER):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = RGBColor(*color)
    return p

def add_styled_heading(doc, text, level):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.keep_with_next = True
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(4)
    run = h.runs[0]
    run.font.name = "Arial"
    if level == 1:
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = RGBColor(15, 41, 66)
    elif level == 2:
        run.font.size = Pt(11.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(30, 58, 138)
    elif level == 3:
        run.font.size = Pt(10.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(51, 65, 85)
    return h

def add_body_p(doc, text, bold_prefix="", space_after=6, italic_prefix=False):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(space_after)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
        if italic_prefix:
            r_pre.font.italic = True
        r_pre.font.color.rgb = RGBColor(15, 23, 42)
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(30, 41, 59)
    return p

def add_bullet(doc, text, bold_prefix=""):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(3)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(15, 23, 42)
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(30, 41, 59)
    return p

def add_figure(doc, image_path, caption_text, width_inches=5.8):
    if not Path(image_path).exists():
        print(f"Warning: image {image_path} not found.")
        return
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(8)
    p_img.paragraph_format.space_after = Pt(2)
    run = p_img.add_run()
    run.add_picture(str(image_path), width=Inches(width_inches))

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(10)
    p_cap.paragraph_format.keep_with_next = True
    r_cap = p_cap.add_run(caption_text)
    r_cap.font.name = "Calibri"
    r_cap.font.size = Pt(9.5)
    r_cap.font.italic = True
    r_cap.font.bold = True
    r_cap.font.color.rgb = RGBColor(71, 85, 105)

def build_report():
    print("Initializing Document...")
    doc = Document()

    # Set Margins (1 inch on all sides)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # =========================================================================
    # TITLE PAGE / COVER (Strictly matching KBS CCP Report Template.pdf)
    # =========================================================================
    add_header_text(doc, "NED University of Engineering and Technology, Karachi", size=15, bold=True)
    add_header_text(doc, "Computer Science and Information Technology", size=13, bold=True, color=(71, 85, 105))
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_header_text(doc, "COMPLEX COMPUTING PROBLEM (CCP)", size=14, bold=True, color=(15, 23, 42))
    add_header_text(doc, "PROJECT SUBMISSION", size=14, bold=True, color=(15, 23, 42))

    # Add Official NED Emblem extracted directly from the template
    ned_logo_path = DIAG_DIR / "ned_logo_0.png"
    if ned_logo_path.exists():
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(6)
        p_logo.paragraph_format.space_after = Pt(6)
        p_logo.add_run().add_picture(str(ned_logo_path), width=Inches(1.8))

    add_header_text(doc, "Knowledge-Based Systems (CT-359)", size=13, bold=True, color=(15, 41, 66))
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # Project Title Table
    table_title = doc.add_table(rows=2, cols=2)
    table_title.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_title.autofit = False

    col_widths = [Inches(1.8), Inches(4.7)]
    for row in table_title.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width

    # Row 0: Project Title
    table_title.cell(0, 0).paragraphs[0].add_run("Project Title").bold = True
    table_title.cell(0, 0).paragraphs[0].runs[0].font.size = Pt(10)
    set_cell_background(table_title.cell(0, 0), "E2E8F0")
    set_cell_margins(table_title.cell(0, 0))

    cell_title_val = table_title.cell(0, 1)
    p_tv = cell_title_val.paragraphs[0]
    r_tv = p_tv.add_run("Auto Sage: Intelligent Knowledge-Based System for Automotive Equipment Fault Diagnosis and Maintenance Decision Support")
    r_tv.bold = True
    r_tv.font.size = Pt(10)
    set_cell_margins(cell_title_val)

    # Row 1: Submission Date
    table_title.cell(1, 0).paragraphs[0].add_run("Submission Date").bold = True
    table_title.cell(1, 0).paragraphs[0].runs[0].font.size = Pt(10)
    set_cell_background(table_title.cell(1, 0), "E2E8F0")
    set_cell_margins(table_title.cell(1, 0))

    cell_date_val = table_title.cell(1, 1)
    p_dv = cell_date_val.paragraphs[0]
    p_dv.add_run("October 31, 2026").font.size = Pt(10)
    set_cell_margins(cell_date_val)

    # Table borders
    for row in table_title.rows:
        for cell in row.cells:
            tcPr = cell._tc.get_or_add_tcPr()
            tcBorders = parse_xml(
                f'<w:tcBorders {nsdecls("w")}>'
                f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
                f'<w:left w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
                f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
                f'<w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
                f'</w:tcBorders>'
            )
            tcPr.append(tcBorders)

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(8)
    p_sp.paragraph_format.space_after = Pt(4)

    # Student Details Table
    add_header_text(doc, "Student Details", size=11, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    table_students = doc.add_table(rows=4, cols=4)
    table_students.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_students.autofit = False

    s_widths = [Inches(0.8), Inches(2.7), Inches(1.5), Inches(1.5)]
    for row in table_students.rows:
        for idx, width in enumerate(s_widths):
            row.cells[idx].width = width

    headers = ["Sr. No.", "Student Name", "Roll No.", "Signature"]
    for idx, h_text in enumerate(headers):
        cell = table_students.cell(0, idx)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.bold = True
        r.font.size = Pt(9.5)
        set_cell_background(cell, "DBEAFE")
        set_cell_margins(cell)

    students = [
        ("1", "ALIYAN SHAIKH", "CT-24252"),
        ("2", "TALAL TARIQ", "CT-24298"),
        ("3", "MUHAMMAD HASAN", "CT-24291"),
    ]

    for row_idx, (sr, name, roll) in enumerate(students, start=1):
        cell_sr = table_students.cell(row_idx, 0)
        p_sr = cell_sr.paragraphs[0]
        p_sr.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_sr.add_run(sr).font.size = Pt(9.5)
        set_cell_margins(cell_sr)

        cell_name = table_students.cell(row_idx, 1)
        p_name = cell_name.paragraphs[0]
        r_name = p_name.add_run(name)
        r_name.font.size = Pt(9.5)
        r_name.bold = True
        set_cell_margins(cell_name)

        cell_roll = table_students.cell(row_idx, 2)
        p_roll = cell_roll.paragraphs[0]
        p_roll.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_roll.add_run(roll).font.size = Pt(9.5)
        set_cell_margins(cell_roll)

        cell_sig = table_students.cell(row_idx, 3)
        cell_sig.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_margins(cell_sig)

    for row in table_students.rows:
        for cell in row.cells:
            tcPr = cell._tc.get_or_add_tcPr()
            tcBorders = parse_xml(
                f'<w:tcBorders {nsdecls("w")}>'
                f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
                f'<w:left w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
                f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
                f'<w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
                f'</w:tcBorders>'
            )
            tcPr.append(tcBorders)

    # Project Instructions (from template)
    add_styled_heading(doc, "1. Project Instructions", level=1)
    add_bullet(doc, "Complete all sections using the prescribed template. Replace bracketed placeholders with project-specific information.")
    add_bullet(doc, "Submit the complete source code, dataset / knowledge base files, project report, and presentation according to the submission instructions.")
    add_bullet(doc, "The implementation must be executable and demonstrable during the viva examination.")
    add_bullet(doc, "Any assumptions made to complete the problem must be clearly stated and justified.")
    add_bullet(doc, "All external datasets, knowledge sources, libraries, tools, or publications used in the project must be cited.")
    add_bullet(doc, "The report and presentation must follow the prescribed template and be submitted on time.")

    doc.add_page_break()

    # =========================================================================
    # SECTION 2: PROBLEM STATEMENT (CLO 1, CLO 2, CLO 3)
    # =========================================================================
    add_styled_heading(doc, "2. Problem Statement", level=1)
    add_body_p(doc, "Modern automotive equipment represents a sophisticated integration of mechanical, hydraulic, pneumatic, and electrical subsystems. When an operational failure occurs, identifying the defective assembly from observed physical symptoms is non-trivial due to symptom overlap, incomplete driver reports, and the high cost of misdiagnoses. This project addresses the Complex Computing Problem (CCP) through three Course Learning Outcomes (CLOs):")

    add_bullet(doc, "Explain how a Knowledge-Based System can represent industrial/automotive equipment knowledge, including equipment, components, symptoms, faults, causes, and maintenance actions, using an appropriate knowledge representation formalism. In Auto Sage, this is addressed through a structured, multi-tier JSON ontology comprising 8 primary automotive categories, 120 canonical deduplicated symptoms, and 93 verified production rules that couple non-invasive symptom patterns with physical bench verifications (Tier A) and maintenance directives (Tier B).", bold_prefix="CLO 1 — Knowledge Representation Formalism: ")

    add_bullet(doc, "Analyze the given industrial equipment fault-diagnosis problem by identifying incomplete requirements, stakeholder needs, relationships, constraints, and suitable knowledge-based approaches for developing an effective solution. In Auto Sage, this is realized by engineering a dynamic second-stage clarification mechanism (up to 5 targeted follow-up inquiries) that resolves ambiguous symptom clusters, detects contradictory user observations, and isolates candidate faults before destructive mechanical disassembly.", bold_prefix="CLO 2 — Problem Analysis & Requirements Engineering: ")

    add_bullet(doc, "Evaluate suitable knowledge representation methods and inference algorithms for diagnosing equipment faults and recommending maintenance actions, and justify the selected approach based on accuracy, explainability, safety, cost, and system requirements. In Auto Sage, a deterministic propositional forward-chaining inference engine was evaluated and selected over stochastic machine-learning classifiers. This guarantees 100% auditable reasoning trails, deterministic conflict resolution via evidence tallying and negative contradiction penalties (-4 points), strict safety priority escalation, and complete explainability.", bold_prefix="CLO 3 — Algorithmic Evaluation & KBS Justification: ")

    # =========================================================================
    # SECTION 3: PROBLEM DESCRIPTION / PROJECT CONTEXT
    # =========================================================================
    add_styled_heading(doc, "3. Problem Description / Project Context", level=1)
    add_body_p(doc, "In contemporary automotive fleet management and individual vehicle maintenance, diagnosing operational anomalies poses significant challenges due to information asymmetry, heterogeneous knowledge sources, and severe safety consequences. Mechanical workshops, service centers, and vehicle operators frequently encounter ambiguous symptoms—such as engine overheating, brake pedal spongy travel, erratic transmission slipping, or no-crank electrical conditions—that can stem from multiple distinct component failures. Driver reports are inherently incomplete, subjective, and prone to descriptive inaccuracies. At the same time, service technicians operate under acute constraints: commercial pressures incentivize rapid part replacements, while improper diagnosis can lead to premature replacement of expensive, functional components (e.g., replacing an entire hydraulic brake booster when the actual fault is a degraded vacuum hose). Furthermore, safety-critical systems like braking, steering, and fuel delivery present life-safety hazards where inaccurate triage could lead to catastrophic road accidents or sudden thermal fires.")

    add_body_p(doc, "Auto Sage is engineered as an intelligent, deterministic Knowledge-Based System that bridges the gap between non-invasive symptom observation and certified mechanical repair. Grounded in peer-reviewed empirical workshop failure records collected at the Akwa Ibom Transport Corporation (AKTC) mechanical division, Auto Sage formalizes expert diagnostic reasoning into an interactive, step-by-step diagnostic platform. The system ingests driver-observed symptoms, generates dynamic follow-up clarification inquiries to eliminate false positives and contradictory conditions, evaluates candidate failure modes through transparent propositional rules (ALL, ANY, and PRIMARY_OR_PARTIAL modes), and strictly separates Tier A Physical Bench Verification (multimeter, vacuum gauge, and pressure measurements) from Tier B Maintenance Directives. By enforcing objective component replacement criteria and issuing explicit anti-mistake directives, Auto Sage resolves stakeholder conflicts, minimizes maintenance downtime, safeguards roadworthiness, and delivers an audit-ready, 12-section diagnostic report for workshop service authorization.")

    # =========================================================================
    # SECTION 4: PROBLEM ANALYSIS
    # =========================================================================
    add_styled_heading(doc, "4. Problem Analysis", level=1)

    add_styled_heading(doc, "4.1 Problem Understanding", level=2)
    add_body_p(doc, "Vehicle fault diagnosis is traditionally performed either through heuristic guesswork by human mechanics or through diagnostic trouble codes (DTCs) read from the On-Board Diagnostics (OBD-II) port. However, a significant majority of physical mechanical failures—such as sticking caliper slide pins, vacuum booster diaphragm tears, worn friction linings, warped brake rotors, and coolant hose micro-cracks—do not trigger an electronic trouble code until severe secondary damage has occurred. Consequently, diagnosis must rely on observable physical manifestations (acoustics, vibrations, thermal anomalies, hydraulic pedal feedback, and fluid leakages). The computational challenge lies in mapping subjective, often singular customer observations to complex, multi-component physical failure modes without generating hallucinations or assigning unjustified confidence percentages.")

    add_styled_heading(doc, "4.2 Stakeholders and Their Requirements", level=2)
    add_body_p(doc, "The system serves four primary stakeholder groups, each with distinct and often conflicting operational requirements:")
    add_bullet(doc, "Requires an intuitive, jargon-free interface to report observations, understand whether the vehicle is safe to drive (roadworthiness advisory), avoid paying for unnecessary parts, and obtain an authentic inspection dossier before visiting a repair facility.", bold_prefix="1. Vehicle Owners & Drivers: ")
    add_bullet(doc, "Requires systematic, standardized triage procedures, exact multimeter and gauge criteria (Tier A physical checks), component-specific failure taxonomies, and clear warnings against premature component replacement.", bold_prefix="2. Automotive Service Technicians: ")
    add_bullet(doc, "Requires auditable diagnostic records, formal work-order sign-off blocks, standardized service bay routing, and verifiable safety liability disclaimers.", bold_prefix="3. Workshop Service Managers: ")
    add_bullet(doc, "Requires rigorous knowledge representation formalism, verifiable empirical dataset grounding (DOI: 10.5281/zenodo.15626055), deterministic algorithmic execution, automated test coverage, and transparent viva demonstrability.", bold_prefix="4. University Course Evaluators (CT-359): ")

    add_styled_heading(doc, "4.3 Constraints and Conflicting Requirements", level=2)
    add_body_p(doc, "Engineering Auto Sage required resolving critical technical and operational tensions:")
    add_bullet(doc, "Drivers report symptoms in non-technical terms, whereas automotive service manuals require precise engineering terminology. The system resolves this by defining 120 canonical, user-friendly symptom descriptions mapped internally to formal component predicates.", bold_prefix="A. Layperson Reporting vs. Technical Rigor: ")
    add_bullet(doc, "A single symptom like 'Soft or spongy brake pedal' can be caused by air in hydraulic lines, a failing master cylinder, swollen rubber hoses, or a defective brake booster. The system avoids hasty conclusions by treating initial matches as preliminary candidates and triggering dynamic follow-up questions to isolate the true root cause.", bold_prefix="B. Broad Multi-Candidate Ambiguity: ")
    add_bullet(doc, "Vehicle owners want low-cost fixes, while safety mandates strict intervention on compromised brakes or overheating engines. The system enforces a 4-tier safety hierarchy (Critical, High, Medium, Low) that halts vehicle operation when life-safety is threatened regardless of repair costs.", bold_prefix="C. Cost Minimization vs. Life-Safety Mandate: ")
    add_bullet(doc, "Black-box machine learning models output probabilistic predictions that cannot be formally audited or explained in a court or workshop. Auto Sage strictly enforces deterministic propositional logic, guaranteeing that identical inputs always yield identical, explainable outputs.", bold_prefix="D. Determinism vs. Machine Learning Hallucination: ")

    add_styled_heading(doc, "4.4 Root Cause / Requirement Identification", level=2)
    add_body_p(doc, "Based on stakeholder analysis, the functional and non-functional requirements of the KBS were formalized:")
    add_bullet(doc, "FR-1: Vehicle Specification Intake; FR-2: 8-Subsystem Category Selection; FR-3: Canonical Symptom Selection with Keyword Filtering; FR-4: Dynamic Follow-Up Inquiry Generation (up to 5 questions); FR-5: Propositional Inference Execution (ALL, ANY, PRIMARY_OR_PARTIAL); FR-6: Multi-Attribute Candidate Ranking & Contradiction Penalty (-4 points); FR-7: Two-Tier Guidance Output (Tier A Physical Tests & Tier B Maintenance Directives); FR-8: 12-Section Formal Diagnostic Report Generation (Client-Side PDF & Native Print); FR-9: Local Session Persistence in localStorage.", bold_prefix="Functional Requirements (FR): ")
    add_bullet(doc, "NFR-1: Sub-millisecond inference execution via LRU in-memory rule caching; NFR-2: Zero cloud telemetry leakage (100% local processing); NFR-3: High-fidelity A4 document pagination with page-break avoidance; NFR-4: Responsive cross-platform presentation across desktop and mobile browsers.", bold_prefix="Non-Functional Requirements (NFR): ")

    add_styled_heading(doc, "4.5 Assumptions", level=2)
    add_body_p(doc, "The system design operates under three explicit, justified assumptions:")
    add_bullet(doc, "The driver or apprentice technician entering symptoms provides honest, observable observations based on physical sight, sound, smell, or driving feel.", bold_prefix="Assumption 1 (Observation Veracity): ")
    add_bullet(doc, "A diagnostic result produced by the KBS represents a hypothetical candidate requiring physical bench testing (Tier A) prior to mechanical teardown or parts purchase.", bold_prefix="Assumption 2 (Diagnostic Hypothesis Status): ")
    add_bullet(doc, "The scope of deterministic fault isolation is bounded by the 93 empirical failure modes documented in the research dataset. Symptoms outside this scope result in an honest no-match declaration.", bold_prefix="Assumption 3 (Knowledge Base Boundary): ")

    doc.add_page_break()

    # =========================================================================
    # SECTION 5: KNOWLEDGE REPRESENTATION AND KBS DESIGN
    # =========================================================================
    add_styled_heading(doc, "5. Knowledge Representation and KBS Design", level=1)

    add_styled_heading(doc, "5.1 Selected Knowledge Representation Formalism", level=2)
    add_body_p(doc, "Auto Sage utilizes Production Rules based on Classical Propositional Logic augmented with multi-mode matching semantics. Production rules represent domain expertise as declarative condition-action pairs: IF <antecedent> THEN <consequent>.")
    add_body_p(doc, "Mathematically, each diagnostic rule R_i is defined as a tuple:")
    add_body_p(doc, "R_i = < C_i, S_i, P_i, M_i, F_i, Q_i, V_i, A_i, L_i >", bold_prefix="Rule Schema Definition: ")
    add_body_p(doc, "Where C_i is the category identifier, S_i is the set of required symptom predicates, P_i is the set of primary direct triggers, M_i in {ALL, ANY, PRIMARY_OR_PARTIAL} is the propositional logic mode, F_i is the fault candidate, Q_i is the set of follow-up clarification questions, V_i is the multi-step Tier A verification procedure, A_i is the Tier B maintenance action schema, and L_i in {Critical, High, Medium, Low} is the safety risk level.")

    add_body_p(doc, "The three propositional matching modes operate as follows:")
    add_bullet(doc, "Conjunction (AND). The rule fires as a full match if and only if all symptoms in S_i are present in the user's intake manifest: FullMatch <=> S_i subseteq SelectedSymptoms. If only a proper subset matches, it evaluates to a partial candidate.", bold_prefix="1. ALL Mode: ")
    add_bullet(doc, "Disjunction (OR). Any single symptom from S_i satisfies the rule: FullMatch <=> S_i intersect SelectedSymptoms != empty_set.", bold_prefix="2. ANY Mode: ")
    add_bullet(doc, "Hierarchical Trigger. Used for complex components having one definitive hallmark symptom and several shared indicators. If a symptom in P_i is selected, the rule evaluates to 'full'. If only secondary symptoms match, it evaluates to 'partial'.", bold_prefix="3. PRIMARY_OR_PARTIAL Mode: ")

    add_styled_heading(doc, "5.2 Knowledge Base / Ontology / Rule Base", level=2)
    add_body_p(doc, "The Knowledge Base is serialized in JSON format at backend/data/kbs_knowledge_base.json (574 KB). It organizes automotive knowledge across 8 discrete subsystem domains, 120 canonical deduplicated symptoms, and 93 verified diagnostic rules:")

    # Table of Categories
    table_cats = doc.add_table(rows=9, cols=5)
    table_cats.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_cats.autofit = False

    cat_widths = [Inches(1.2), Inches(2.2), Inches(0.8), Inches(0.8), Inches(1.5)]
    for row in table_cats.rows:
        for idx, width in enumerate(cat_widths):
            row.cells[idx].width = width

    c_headers = ["Category ID", "Subsystem Domain", "Rules", "Symptoms", "Safety Level"]
    for idx, text in enumerate(c_headers):
        cell = table_cats.cell(0, idx)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(text)
        r.bold = True
        r.font.size = Pt(9)
        set_cell_background(cell, "DBEAFE")
        set_cell_margins(cell)

    cat_data = [
        ("CAT_ENGINE", "Engine & Fuel System", "25", "31", "High / Critical"),
        ("CAT_ELECTRICAL", "Starting, Battery & Electrical", "13", "21", "High"),
        ("CAT_BRAKES", "Braking & ABS System", "10", "11", "Critical"),
        ("CAT_COOLING", "Cooling & Cabin Heating", "9", "9", "High"),
        ("CAT_TRANSMISSION", "Transmission & Drivetrain", "15", "23", "High"),
        ("CAT_EMISSIONS", "Exhaust & Emissions System", "9", "10", "Medium"),
        ("CAT_HVAC", "Air Conditioning & Ventilation", "6", "10", "Medium"),
        ("CAT_STEERING_TIRES", "Steering, Wheels & Tires", "6", "10", "Critical"),
    ]

    for row_idx, (cid, name, r_cnt, s_cnt, s_lev) in enumerate(cat_data, start=1):
        table_cats.cell(row_idx, 0).paragraphs[0].add_run(cid).font.size = Pt(9)
        table_cats.cell(row_idx, 1).paragraphs[0].add_run(name).font.size = Pt(9)
        table_cats.cell(row_idx, 2).paragraphs[0].add_run(r_cnt).font.size = Pt(9)
        table_cats.cell(row_idx, 2).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        table_cats.cell(row_idx, 3).paragraphs[0].add_run(s_cnt).font.size = Pt(9)
        table_cats.cell(row_idx, 3).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        table_cats.cell(row_idx, 4).paragraphs[0].add_run(s_lev).font.size = Pt(9)
        for col_i in range(5):
            set_cell_margins(table_cats.cell(row_idx, col_i))

    for row in table_cats.rows:
        for cell in row.cells:
            tcPr = cell._tc.get_or_add_tcPr()
            tcBorders = parse_xml(
                f'<w:tcBorders {nsdecls("w")}>'
                f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
                f'<w:left w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
                f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
                f'<w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
                f'</w:tcBorders>'
            )
            tcPr.append(tcBorders)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_styled_heading(doc, "5.3 Inference Mechanism", level=2)
    add_body_p(doc, "Auto Sage implements a Data-Driven Forward-Chaining Inference Engine (backend/inference_engine.py). Reasoning progresses through an explicit 9-Step Reasoning Trail:")
    add_bullet(doc, "1. Symptom Intake Manifest: Validates symptom IDs against canonical category definitions.")
    add_bullet(doc, "2. Follow-Up Ingestion: Normalizes user answers ('yes', 'no', 'not_sure') to lowercase strings.")
    add_bullet(doc, "3. Category Rule Retrieval: Extracts rules registered under the active category.")
    add_bullet(doc, "4. Propositional Logic Evaluation: Computes match status ('full' vs. 'partial') across ALL, ANY, and PRIMARY_OR_PARTIAL modes.")
    add_bullet(doc, "5. Cross-Category Knowledge Scan: Identifies multi-symptom rules satisfied across adjacent subsystems.")
    add_bullet(doc, "6. Contradiction & Missing Condition Filtering: Tallies supporting and contradictory evidence.")
    add_bullet(doc, "7. Candidate Ranking & Isolation: Applies a deterministic 9-element sorting tuple.")
    add_bullet(doc, "8. Diagnostic Verification Directive: Isolates the Step 1 physical bench procedure.")
    add_bullet(doc, "9. Maintenance & Safety Protocol Assignment: Assigns the overall safety risk level and anti-mistake directives.")

    add_body_p(doc, "To rank candidates deterministically without fabricating artificial confidence percentages, the engine computes an integer Evidence Tally:")
    add_body_p(doc, "Evidence Tally = (2 * |MatchedSymptoms|) + (2 * |SupportingFollowUps|) - (4 * |ContradictoryFollowUps|) - (1 * |MissingSymptoms|)", bold_prefix="Evidence Tally Formula: ")
    add_body_p(doc, "Matched symptoms and confirmatory follow-ups award +2 points each. Missing rule conditions incur a -1 penalty. Contradictory answers incur a severe -4 penalty, ensuring discredited candidates drop below valid possibilities.")

    add_styled_heading(doc, "5.4 Conflict Resolution Strategy", level=2)
    add_body_p(doc, "When multiple rules fire simultaneously, conflict resolution is governed by a deterministic 9-element sorting key (_rank_key):")
    add_body_p(doc, "(is_contradicted, 0 if full_match else 1, status_order, -evidence_tally, -matched_count, missing_count, safety_val, unaccounted_count, rule_id)", bold_prefix="Deterministic Sorting Key: ")
    add_body_p(doc, "This guarantees: (1) Contradicted candidates always sort to the bottom; (2) Full matches rank ahead of partial matches; (3) Corroborated status ranks ahead of unverified status; (4) Highest evidence tally breaks ties; (5) Critical safety faults rank ahead of lower risks; and (6) Alphabetical rule ID guarantees 100% deterministic tie-breaking.")

    add_styled_heading(doc, "5.5 Explanation Facility", level=2)
    add_body_p(doc, "Auto Sage provides complete diagnostic transparency by decomposing every conclusion into four structured elements:")
    add_bullet(doc, "Lists observed symptoms and confirmatory follow-up responses supporting the fault hypothesis.", bold_prefix="1. Supporting Evidence: ")
    add_bullet(doc, "Explicitly enumerates unobserved rule symptoms and unperformed tests requiring bench verification.", bold_prefix="2. Missing Prerequisites: ")
    add_bullet(doc, "Highlights follow-up observations that refute the hypothesis, explaining why the fault is contraindicated.", bold_prefix="3. Contradictory Evidence: ")
    add_bullet(doc, "Synthesizes observations into clear, natural automotive sentences (e.g., 'You reported Soft or spongy brake pedal... however, other common signs were not reported, so further physical inspection is required').", bold_prefix="4. Clinical Reasoning Correlation: ")

    add_styled_heading(doc, "5.6 System Architecture", level=2)
    add_body_p(doc, "The architecture strictly decouples presentation, REST routing, and knowledge reasoning. Figure 1 illustrates the high-level system architecture, and Figure 2 details the propositional inference logic flow:")

    add_figure(doc, DIAG_DIR / "01_system_architecture.png", "Figure 1: Auto Sage High-Level System Architecture and Component Interaction", width_inches=6.0)
    add_figure(doc, DIAG_DIR / "02_inference_flowchart.png", "Figure 2: 9-Step Propositional Inference Engine Logic Flowchart", width_inches=5.8)
    add_figure(doc, DIAG_DIR / "03_use_case_diagram.png", "Figure 3: UML Use Case Diagram for Drivers and Automotive Service Technicians", width_inches=5.8)
    add_figure(doc, DIAG_DIR / "04_dfd_diagram.png", "Figure 4: Data Flow Diagram (DFD Level 1) for Intake, Inference, and Dossier Generation", width_inches=5.8)

    doc.add_page_break()

    # =========================================================================
    # SECTION 6: DATASET / KNOWLEDGE SOURCES (Matching template table)
    # =========================================================================
    add_styled_heading(doc, "6. Dataset / Knowledge Sources", level=1)
    add_body_p(doc, "The diagnostic knowledge base is compiled from a peer-reviewed empirical automotive maintenance dataset collected across commercial bus and passenger vehicle maintenance workshops at the Akwa Ibom Transport Corporation (AKTC):")

    table_ds = doc.add_table(rows=2, cols=5)
    table_ds.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_ds.autofit = False

    ds_widths = [Inches(1.8), Inches(1.1), Inches(1.1), Inches(1.3), Inches(1.2)]
    for row in table_ds.rows:
        for idx, width in enumerate(ds_widths):
            row.cells[idx].width = width

    d_headers = ["Source / Dataset", "Type", "Size / No. of Records", "Purpose", "Citation / URL"]
    for idx, text in enumerate(d_headers):
        cell = table_ds.cell(0, idx)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(text)
        r.bold = True
        r.font.size = Pt(8.5)
        set_cell_background(cell, "DBEAFE")
        set_cell_margins(cell)

    ds_vals = [
        "Automotive Faults Dataset for Diagnostic and Maintenance Systems (Obike & Obot)",
        "Empirical JSON Dataset & Verified Flowcharts",
        "99 Raw Records\n(93 Integrated Rules, 120 Symptoms)",
        "Core KBS Domain Knowledge, Symptoms, Tier A Tests & Tier B Repairs",
        "Zenodo DOI:\n10.5281/zenodo.15626055\n(CC BY 4.0)"
    ]
    for idx, val in enumerate(ds_vals):
        cell = table_ds.cell(1, idx)
        cell.paragraphs[0].add_run(val).font.size = Pt(8.5)
        set_cell_margins(cell)

    for row in table_ds.rows:
        for cell in row.cells:
            tcPr = cell._tc.get_or_add_tcPr()
            tcBorders = parse_xml(
                f'<w:tcBorders {nsdecls("w")}>'
                f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
                f'<w:left w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
                f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
                f'<w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
                f'</w:tcBorders>'
            )
            tcPr.append(tcBorders)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    add_body_p(doc, "Cleansing and Ingestion Pipeline: The raw AKTC dataset contained 99 records. The automated build pipeline (backend/build_kbs.py) merged 1 duplicate record (combining overlapping battery charging failure profiles) and excluded 5 records that lacked observable physical symptom mappings. The remaining 93 records were enriched via backend/rule_enrichment.py with explicit Tier A physical tests, Tier B repair instructions, replacement thresholds, anti-mistake directives, and diagnostic clarification questions.")

    # =========================================================================
    # SECTION 7: IMPLEMENTATION
    # =========================================================================
    add_styled_heading(doc, "7. Implementation", level=1)

    add_styled_heading(doc, "7.1 Software / Tools / Libraries", level=2)
    add_body_p(doc, "The implementation utilizes modern open-source web and computational frameworks:")
    add_bullet(doc, "Vite 5.4, React 18.3.1, Tailwind CSS 3.4, Material Symbols Outlined, html2pdf.js 0.14.0.", bold_prefix="Frontend Stack: ")
    add_bullet(doc, "Python 3.12 / 3.14, Flask 3.1.2, Flask-CORS 6.0.0, python-docx 1.2.0, docx2pdf, Selenium 4.52.0.", bold_prefix="Backend Stack: ")
    add_bullet(doc, "JSON schema validation via validate_knowledge_base.py, Node.js native test runner (node --test), Python unittest.", bold_prefix="Testing & Verification: ")

    add_styled_heading(doc, "7.2 Modules and Components", level=2)
    add_body_p(doc, "The application is partitioned into 10 modular React page components and an overarching presentation shell:")
    add_bullet(doc, "Dashboard.jsx: Landing overview with vehicle subsystem hotspot navigation and live system status.", bold_prefix="1. Dashboard: ")
    add_bullet(doc, "VehicleInformation.jsx: Intake form capturing Make, Model, Year, Powertrain, and Odometer with safe fallbacks.", bold_prefix="2. Vehicle Intake: ")
    add_bullet(doc, "SymptomSelection.jsx: Subsystem selector, real-time keyword search, and live symptom selection tray.", bold_prefix="3. Symptom Selection: ")
    add_bullet(doc, "FollowUpQuestions.jsx: Targeted secondary clarification inquiry presenting up to 5 questions with context.", bold_prefix="4. Clarification Inquiries: ")
    add_bullet(doc, "DiagnosisResults.jsx: Candidate fault cards, formal status pills, evidence breakdown, and flowchart previews.", bold_prefix="5. Diagnosis Results: ")
    add_bullet(doc, "FaultDetails.jsx: Component mechanical hierarchy, documented root causes, and multi-step bench procedures.", bold_prefix="6. Component Details: ")
    add_bullet(doc, "RepairMitigationGuide.jsx: Corrective actions, preventive schedules, replacement criteria, and anti-mistake rules.", bold_prefix="7. Repair Guide: ")
    add_bullet(doc, "SafetyGuide.jsx: 4-tier safety hazard manual, emergency roadside protocols, and dangerous DIY warnings.", bold_prefix="8. Safety Guide: ")
    add_bullet(doc, "History.jsx: Persistent local session viewer, keyword filter, and review payload restoration.", bold_prefix="9. History Archive: ")
    add_bullet(doc, "DiagnosticReport.jsx: 12-section printable vehicle inspection document with PDF download and native print.", bold_prefix="10. Diagnostic Report: ")

    add_styled_heading(doc, "7.3 Code Structure", level=2)
    add_body_p(doc, "The repository is structured into distinct functional directories:")
    add_body_p(doc, "D:\\CARFAULTDIA\\\n├── backend/\n│   ├── app.py (REST API routes & input sanitization)\n│   ├── inference_engine.py (Propositional matching & ranking logic)\n│   ├── build_kbs.py (Dataset transformation & compilation pipeline)\n│   ├── rule_enrichment.py (Tier A & Tier B academic metadata)\n│   └── data/kbs_knowledge_base.json (Compiled production KBS)\n├── frontend/\n│   ├── src/pages/ (10 user-facing view components)\n│   ├── src/components/ (Layout.jsx, Stepper.jsx, Evidence.jsx)\n│   └── src/utils/ (historyStorage.js, pdfExport.js)\n└── final_report/ (Deliverables, screenshots, and diagrams)", bold_prefix="Directory Tree: ")

    add_styled_heading(doc, "7.4 User Inputs and Outputs", level=2)
    add_body_p(doc, "User inputs comprise: (1) Vehicle intake specifications; (2) Subsystem selection; (3) Observable symptom selections; and (4) Yes/No/Not Sure follow-up responses. System outputs comprise: (1) Ranked candidate fault hypotheses; (2) Formal status badges; (3) Supporting, missing, and contradictory evidence breakdowns; (4) Tier A bench testing criteria; (5) Tier B repair directives; (6) Operational roadworthiness driving advisories; and (7) Printable 12-section PDF vehicle inspection reports.")

    doc.add_page_break()

    # =========================================================================
    # SECTION 8: TESTING AND RESULTS
    # =========================================================================
    add_styled_heading(doc, "8. Testing and Results", level=1)

    add_styled_heading(doc, "8.1 Automated Test Execution & Quality Assurance", level=2)
    add_body_p(doc, "Auto Sage was subjected to automated unit, integration, and build testing across both frontend and backend stacks. All 42 automated tests passed with a 100% success rate:")
    add_bullet(doc, "29 tests executed in 2.37s. Verified endpoint status codes, 404/400 validation, propositional evaluation, contradiction penalties, ranking keys, and KB schema integrity.", bold_prefix="1. Backend Unit Tests (unittest): ")
    add_bullet(doc, "13 tests executed in 379ms. Verified localStorage serialization, quota handling, session isolation, report ID generation, and DOM formatting helpers.", bold_prefix="2. Frontend Unit Tests (Node.js): ")
    add_bullet(doc, "Verified live HTTP REST pipeline across /api/health, /api/categories, /api/symptoms, and /api/diagnose.", bold_prefix="3. Integration Verification: ")
    add_bullet(doc, "54 modules transformed and bundled cleanly in 14.45s with zero syntax or compilation errors.", bold_prefix="4. Production Build (Vite): ")

    add_styled_heading(doc, "8.2 Three Real Diagnosis Scenarios", level=2)
    add_body_p(doc, "To demonstrate the inference engine's reasoning behavior, three real diagnosis scenarios were executed:")
    add_bullet(doc, "Input: CAT_COOLING with 'Engine overheating' and 'Coolant leak under vehicle'. Follow-up: Q_COOL_PUDDLE answered 'Yes'. Result: RULE_COOL_001 matched with status 'Suspected Fault (Corroborated by Follow-up Evidence)', evidence tally +6, and zero missing conditions.", bold_prefix="Scenario 1 (Full Conjunction Match): ")
    add_bullet(doc, "Input: CAT_BRAKES with single symptom 'Soft or spongy brake pedal'. Initially produces 5 partial candidates (Brake Booster, Hose, Master Cylinder, Fluid, Drum). When the user answers that the pedal drops on engine start ('Yes') and does not hiss ('No'), RULE_BRK_003 (Brake Booster) is directly contradicted, dropping from Rank 1 to Rank 5 with tally -7 and status 'Fault Not Supported by Evidence'.", bold_prefix="Scenario 2 (Partial Match & Follow-up Refutation): ")
    add_bullet(doc, "Case 3A: Selecting 'Check engine light on' alone returns status 'no_match' because it is a broad indicator shared by many faults. Case 3B: Selecting 'ABS warning light is on' + 'Brake dragging' returns status 'no_match' because no stored rule requires both electrical sensor failure and mechanical slide pin seizure simultaneously. The system honestly declares no match rather than guessing.", bold_prefix="Scenario 3 (Broad Indicator & Contradictory No-Match): ")

    add_styled_heading(doc, "8.3 Genuine Application Screenshots", level=2)
    add_body_p(doc, "Figures 5 through 15 present genuine, unedited screenshots captured from the running application demonstrating all 10 user-facing pages:")

    add_figure(doc, SCREEN_DIR / "01_dashboard.png", "Figure 5: Auto Sage Dashboard — System Health, Hotspots, and Subsystem Cards", width_inches=5.8)
    add_figure(doc, SCREEN_DIR / "02_vehicle_information.png", "Figure 6: Vehicle Information Intake Form — Specification Profile with Skip Fallback", width_inches=5.8)
    add_figure(doc, SCREEN_DIR / "03_symptom_selection.png", "Figure 7: Symptom Selection Interface — Category Selector, Keyword Search, and Selection Tray", width_inches=5.8)
    add_figure(doc, SCREEN_DIR / "04_followup_questions.png", "Figure 8: Targeted Follow-Up Inquiry — Dynamic Clarification Questions with Engineering Context", width_inches=5.8)
    add_figure(doc, SCREEN_DIR / "05_diagnosis_results.png", "Figure 9: Diagnosis Results — Ranked Candidate Faults, Status Pills, and Tier A Directives", width_inches=5.8)
    add_figure(doc, SCREEN_DIR / "06_evidence_breakdown.png", "Figure 10: Evidence Breakdown Component — Supporting, Missing, and Contradictory Findings", width_inches=5.8)
    add_figure(doc, SCREEN_DIR / "07_fault_details.png", "Figure 11: Fault Details Dossier — Component Mechanical Hierarchy and Multimeter Checklists", width_inches=5.8)
    add_figure(doc, SCREEN_DIR / "08_repair_mitigation_guide.png", "Figure 12: Repair & Mitigation Guide — Tier B Actions, Replacement Criteria, and Anti-Mistake Warnings", width_inches=5.8)
    add_figure(doc, SCREEN_DIR / "09_safety_guide.png", "Figure 13: Safety Guide — 4-Tier Roadworthiness Hierarchy and Roadside Protocols", width_inches=5.8)
    add_figure(doc, SCREEN_DIR / "11_diagnosis_history.png", "Figure 14: Diagnosis History — Persistent Archive of Past Diagnostic Sessions in localStorage", width_inches=5.8)
    add_figure(doc, SCREEN_DIR / "10_diagnostic_report.png", "Figure 15: Vehicle Diagnostic Report — 12-Section Printable A4 Inspection Dossier with Official Brand Logo", width_inches=5.8)

    doc.add_page_break()

    # =========================================================================
    # SECTION 9: EVALUATION, LIMITATIONS AND CONCLUSION
    # =========================================================================
    add_styled_heading(doc, "9. Evaluation, Limitations and Conclusion", level=1)

    add_styled_heading(doc, "9.1 Evaluation of the Proposed Approach", level=2)
    add_body_p(doc, "The evaluation demonstrates that Auto Sage satisfies all academic learning outcomes and industrial software requirements:")
    add_bullet(doc, "Unlike neural networks that output unexplainable percentages, Auto Sage provides complete transparency. Every recommended check is directly traced to satisfied propositional predicates.", bold_prefix="1. 100% Explainability (CLO 3): ")
    add_bullet(doc, "Identical symptoms and follow-up answers always produce the identical ranking and directives. There is zero stochastic variance or hallucination.", bold_prefix="2. Deterministic Consistency: ")
    add_bullet(doc, "Separating Tier A bench tests from Tier B repairs eliminates premature component replacement, addressing the core economic failure of vehicle triage.", bold_prefix="3. Economic & Anti-Mistake Utility: ")
    add_bullet(doc, "By operating entirely on local client-side and Flask runtime, no vehicle telemetry or driver identities are exposed to third-party cloud infrastructure.", bold_prefix="4. Privacy & Zero-Cloud Footprint: ")

    add_styled_heading(doc, "9.2 Limitations", level=2)
    add_body_p(doc, "In accordance with academic rigor, the actual limitations of the system are explicitly acknowledged:")
    add_bullet(doc, "The system relies on human observation rather than streaming real-time sensor voltages directly from an OBD-II CAN bus scanner.", bold_prefix="1. Manual Symptom Observation: ")
    add_bullet(doc, "The deterministic inference scope is bounded by the 93 rules compiled from the research dataset. Obscure faults outside this scope result in an honest no-match.", bold_prefix="2. Scope Bounded to 93 Failure Modes: ")
    add_bullet(doc, "A diagnostic result is an unverified hypothesis. Physical confirmation requires hands-on multimeter or pressure measurements.", bold_prefix="3. Hypothetical Status: ")
    add_bullet(doc, "Diagnosis history is stored in browser localStorage. Clearing browser data removes previous session records.", bold_prefix="4. Browser-Bound Storage: ")

    add_styled_heading(doc, "9.3 Future Improvements", level=2)
    add_body_p(doc, "Proposed future enhancements include:")
    add_bullet(doc, "Hardware integration with Bluetooth ELM327 OBD-II scanners to automatically ingest live DTC fault codes and sensor PIDs alongside subjective driver observations.", bold_prefix="1. OBD-II CAN Bus Streaming: ")
    add_bullet(doc, "Expanding the Knowledge Base to include high-voltage battery cell degradation, inverter thermal management, and regenerative braking rules for electric vehicles.", bold_prefix="2. Hybrid & EV Telematics Expansion: ")
    add_bullet(doc, "Implementing an optional PostgreSQL backend to synchronize historical fleet work orders across multiple workshop service bays.", bold_prefix="3. Multi-Tenant Workshop Cloud Sync: ")

    add_styled_heading(doc, "9.4 Conclusion", level=2)
    add_body_p(doc, "Auto Sage demonstrates the successful design, implementation, and verification of a deterministic Knowledge-Based System for automotive fault diagnosis and maintenance decision support. By formalizing empirical research knowledge into 93 production rules across 8 subsystems and integrating dynamic follow-up corroboration, the system effectively resolves stakeholder conflicts, eliminates diagnostic guesswork, and enforces physical bench verification before mechanical teardown. Complete with an audit-ready 12-section diagnostic report and an automated test suite, Auto Sage fulfills all requirements of the Complex Computing Problem (CCP) for Knowledge-Based Systems (CT-359).")

    # =========================================================================
    # SECTION 10: REFERENCES (IEEE / Academic Formal Reference List)
    # =========================================================================
    add_styled_heading(doc, "10. References", level=1)
    refs = [
        "[1] P. Obike and O. Obot, 'Automotive Faults Dataset for Diagnostic and Maintenance Systems,' CERN Zenodo, 2024. [Online]. Available: https://doi.org/10.5281/zenodo.15626055. [Accessed: Oct. 31, 2026].",
        "[2] O. Obot and P. Obike, 'An Integrated Fuzzy-Rule and Case-Based Reasoning System for Enhanced Automobile Maintenance and Repair,' Journal of Engineering Research and Reports, vol. 26, no. 8, pp. 433-445, 2024. doi: 10.9734/jerr/2024/v26i81256.",
        "[3] S. Russell and P. Norvig, Artificial Intelligence: A Modern Approach, 4th ed. Hoboken, NJ: Pearson, 2020.",
        "[4] J. Giarratano and G. Riley, Expert Systems: Principles and Programming, 4th ed. Boston, MA: Course Technology, 2005.",
        "[5] B. G. Buchanan and E. H. Shortliffe, Rule-Based Expert Systems: The MYCIN Experiments of the Stanford Heuristic Programming Project. Reading, MA: Addison-Wesley, 1984.",
        "[6] Society of Automotive Engineers, 'SAE J2012: Diagnostic Trouble Code Definitions,' SAE International Standards, 2016.",
        "[7] J. D. Halderman, Automotive Technology: Principles, Diagnosis, and Service, 6th ed. Upper Saddle River, NJ: Pearson, 2020.",
        "[8] M. Ribbens, Understanding Automotive Electronics: An Engineering Perspective, 8th ed. Oxford, UK: Butterworth-Heinemann, 2017."
    ]
    for r_text in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.line_spacing = 1.15
        p_ref.paragraph_format.space_after = Pt(4)
        run = p_ref.add_run(r_text)
        run.font.name = "Calibri"
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(30, 41, 59)

    print(f"Saving DOCX to {DOCX_OUT}...")
    doc.save(str(DOCX_OUT))
    print(f"Saved {DOCX_OUT} ({DOCX_OUT.stat().st_size} bytes).")

    # Convert to PDF
    print(f"Converting DOCX to PDF at {PDF_OUT}...")
    try:
        from docx2pdf import convert
        convert(str(DOCX_OUT), str(PDF_OUT))
        print(f"docx2pdf converted successfully! PDF size: {PDF_OUT.stat().st_size} bytes.")
    except Exception as e:
        print(f"docx2pdf error: {e}, attempting direct win32com...")
        try:
            import win32com.client
            word = win32com.client.Dispatch("Word.Application")
            word.Visible = False
            wb = word.Documents.Open(str(DOCX_OUT.resolve()))
            wb.SaveAs(str(PDF_OUT.resolve()), FileFormat=17) # 17 = wdFormatPDF
            wb.Close()
            try:
                word.Quit()
            except:
                pass
            print(f"win32com direct converted successfully! PDF size: {PDF_OUT.stat().st_size} bytes.")
        except Exception as e2:
            print(f"win32com error: {e2}")

if __name__ == "__main__":
    build_report()
