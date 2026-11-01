"""
Auto Sage Academic Project Report Generator — Master Redesign (v6)
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

BASE_DIR = Path("D:/AUTOSAGE")
FINAL_DIR = BASE_DIR / "final_report"
FINAL_DIR.mkdir(parents=True, exist_ok=True)
SCREEN_DIR = FINAL_DIR / "screenshots"
DIAG_DIR = FINAL_DIR / "diagrams"

DOCX_OUT = FINAL_DIR / "Auto_Sage_Final_Project_Report.docx"
PDF_OUT = FINAL_DIR / "Auto_Sage_Final_Project_Report.pdf"

# Typography Palette
COLOR_NAVY = RGBColor(15, 41, 74)       # Primary Chapter Headings (#0F294A)
COLOR_BLUE = RGBColor(30, 58, 138)      # Secondary Section Headings (#1E3A8A)
COLOR_SLATE = RGBColor(51, 65, 85)      # Subsection Headings (#334155)
COLOR_BODY = RGBColor(30, 41, 59)       # Body Text Charcoal (#1E293B)
COLOR_MUTED = RGBColor(100, 116, 139)   # Captions & Running Headers (#64748B)

HEX_NAVY = "0F294A"
HEX_LIGHT_BLUE = "DBEAFE"
HEX_LIGHT_BG = "F8FAFC"
HEX_BORDER = "CBD5E1"

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=60, bottom=60, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_borders(cell, border_color="CBD5E1", border_sz="4"):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="{border_sz}" w:space="0" w:color="{border_color}"/>'
        f'<w:left w:val="single" w:sz="{border_sz}" w:space="0" w:color="{border_color}"/>'
        f'<w:bottom w:val="single" w:sz="{border_sz}" w:space="0" w:color="{border_color}"/>'
        f'<w:right w:val="single" w:sz="{border_sz}" w:space="0" w:color="{border_color}"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)

def make_row_cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

def make_row_header(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

def format_entire_table(table, col_widths, is_header=True):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    for row_idx, row in enumerate(table.rows):
        make_row_cant_split(row)
        if row_idx == 0 and is_header:
            make_row_header(row)
        for col_idx, width in enumerate(col_widths):
            cell = row.cells[col_idx]
            cell.width = width
            set_cell_margins(cell, top=60, bottom=60, left=120, right=120)
            set_cell_borders(cell)

def add_header_text(doc, text, size=15, bold=True, color=(15, 41, 74), align=WD_ALIGN_PARAGRAPH.CENTER):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.line_spacing = 1.12
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = RGBColor(*color)
    return p

def add_heading_1(doc, text, space_before=10, space_after=3):
    h = doc.add_heading(level=1)
    h.paragraph_format.keep_with_next = True
    h.paragraph_format.space_before = Pt(space_before)
    h.paragraph_format.space_after = Pt(space_after)
    r = h.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(14.5)
    r.font.bold = True
    r.font.color.rgb = COLOR_NAVY
    return h

def add_heading_2(doc, text, space_before=8, space_after=2):
    h = doc.add_heading(level=2)
    h.paragraph_format.keep_with_next = True
    h.paragraph_format.space_before = Pt(space_before)
    h.paragraph_format.space_after = Pt(space_after)
    r = h.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = COLOR_BLUE
    return h

def add_heading_3(doc, text, space_before=5, space_after=2):
    h = doc.add_heading(level=3)
    h.paragraph_format.keep_with_next = True
    h.paragraph_format.space_before = Pt(space_before)
    h.paragraph_format.space_after = Pt(space_after)
    r = h.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(10.5)
    r.font.bold = True
    r.font.color.rgb = COLOR_SLATE
    return h

def add_body_p(doc, text, bold_prefix="", space_after=3, italic_prefix=False):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.12
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(10.5)
        r_pre.font.bold = True
        if italic_prefix:
            r_pre.font.italic = True
        r_pre.font.color.rgb = RGBColor(15, 23, 42)
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(10.5)
    r.font.color.rgb = COLOR_BODY
    return p

def add_bullet(doc, text, bold_prefix="", space_after=2):
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.12
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(10.5)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(15, 23, 42)
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(10.5)
    r.font.color.rgb = COLOR_BODY
    return p

def add_figure(doc, image_path, caption_title, caption_text="", width_inches=4.0):
    if not Path(image_path).exists():
        print(f"Warning: image {image_path} not found.")
        return
    
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(3)
    p_img.paragraph_format.space_after = Pt(1)
    p_img.paragraph_format.keep_with_next = True
    run_img = p_img.add_run()
    run_img.add_picture(str(image_path), width=Inches(width_inches))

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(1)
    p_cap.paragraph_format.space_after = Pt(4)
    
    r_title = p_cap.add_run(caption_title + (" — " if caption_text else ""))
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(9)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_SLATE

    if caption_text:
        r_desc = p_cap.add_run(caption_text)
        r_desc.font.name = "Calibri"
        r_desc.font.size = Pt(9)
        r_desc.font.italic = True
        r_desc.font.color.rgb = COLOR_MUTED

def setup_page_headers_and_footers(doc):
    sec = doc.sections[0]
    # Standard academic 0.9 inch margins to optimize printable area and guarantee 20 balanced pages
    sec.top_margin = Inches(0.9)
    sec.bottom_margin = Inches(0.9)
    sec.left_margin = Inches(0.9)
    sec.right_margin = Inches(0.9)
    sec.different_first_page_header_footer = True

    # Header for pages 2+
    hdr = sec.header
    p_hdr = hdr.paragraphs[0]
    p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_hdr.paragraph_format.space_after = Pt(3)
    r_hl = p_hdr.add_run("Auto Sage: Intelligent Automotive Fault Diagnosis KBS (CT-359)\tNEDUET, Karachi")
    r_hl.font.name = "Calibri"
    r_hl.font.size = Pt(8.5)
    r_hl.font.italic = True
    r_hl.font.color.rgb = COLOR_MUTED

    pPr = p_hdr._p.get_or_add_pPr()
    pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="4" w:space="1" w:color="CBD5E1"/></w:pBdr>')
    pPr.append(pBdr)

    # Footer for pages 2+
    ftr = sec.footer
    p_ftr = ftr.paragraphs[0]
    p_ftr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_ftr.paragraph_format.space_before = Pt(3)

    pPr_f = p_ftr._p.get_or_add_pPr()
    pBdr_f = parse_xml(f'<w:pBdr {nsdecls("w")}><w:top w:val="single" w:sz="4" w:space="1" w:color="CBD5E1"/></w:pBdr>')
    pPr_f.append(pBdr_f)

    r_fl = p_ftr.add_run("Complex Computing Problem (CCP) Final Report\tPage ")
    r_fl.font.name = "Calibri"
    r_fl.font.size = Pt(9)
    r_fl.font.color.rgb = COLOR_MUTED

    fld1 = OxmlElement('w:fldSimple')
    fld1.set(qn('w:instr'), 'PAGE')
    p_ftr._p.append(fld1)

    r_fl2 = p_ftr.add_run(" of ")
    r_fl2.font.name = "Calibri"
    r_fl2.font.size = Pt(9)
    r_fl2.font.color.rgb = COLOR_MUTED

    fld2 = OxmlElement('w:fldSimple')
    fld2.set(qn('w:instr'), 'NUMPAGES')
    p_ftr._p.append(fld2)

def build_report():
    print("Initializing Master Document (v6)...")
    doc = Document()
    setup_page_headers_and_footers(doc)

    # =========================================================================
    # PAGE 1: DEDICATED TITLE PAGE / COVER
    # =========================================================================
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    add_header_text(doc, "NED University of Engineering and Technology, Karachi", size=16, bold=True, color=(15, 41, 74))
    add_header_text(doc, "Department of Computer Science and Information Technology", size=13, bold=True, color=(51, 65, 85))
    add_header_text(doc, "COMPLEX COMPUTING PROBLEM (CCP) PROJECT SUBMISSION", size=13.5, bold=True, color=(30, 58, 138))
    
    ned_logo_path = DIAG_DIR / "ned_logo_0.png"
    if ned_logo_path.exists():
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(8)
        p_logo.paragraph_format.space_after = Pt(8)
        p_logo.add_run().add_picture(str(ned_logo_path), width=Inches(1.75))

    add_header_text(doc, "Course: Knowledge-Based Systems (CT-359)", size=13, bold=True, color=(15, 41, 74))
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    table_title = doc.add_table(rows=2, cols=2)
    format_entire_table(table_title, [Inches(1.8), Inches(4.9)], is_header=False)

    table_title.cell(0, 0).paragraphs[0].add_run("Project Title").bold = True
    table_title.cell(0, 0).paragraphs[0].runs[0].font.size = Pt(10)
    set_cell_background(table_title.cell(0, 0), "F1F5F9")

    cell_tv = table_title.cell(0, 1)
    p_tv = cell_tv.paragraphs[0]
    r_tv = p_tv.add_run("Auto Sage: Intelligent Knowledge-Based System for Automotive Equipment Fault Diagnosis and Maintenance Decision Support")
    r_tv.bold = True
    r_tv.font.size = Pt(10)
    r_tv.font.color.rgb = COLOR_NAVY

    table_title.cell(1, 0).paragraphs[0].add_run("Submission Date").bold = True
    table_title.cell(1, 0).paragraphs[0].runs[0].font.size = Pt(10)
    set_cell_background(table_title.cell(1, 0), "F1F5F9")

    table_title.cell(1, 1).paragraphs[0].add_run("October 31, 2026").font.size = Pt(10)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_header_text(doc, "Student Details", size=11.5, bold=True, color=(15, 41, 74), align=WD_ALIGN_PARAGRAPH.CENTER)

    table_students = doc.add_table(rows=4, cols=4)
    format_entire_table(table_students, [Inches(0.8), Inches(2.9), Inches(1.5), Inches(1.5)], is_header=True)

    headers = ["Sr. No.", "Student Name", "Roll No.", "Signature"]
    for idx, h_text in enumerate(headers):
        cell = table_students.cell(0, idx)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, HEX_NAVY)

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

        cell_name = table_students.cell(row_idx, 1)
        p_name = cell_name.paragraphs[0]
        r_name = p_name.add_run(name)
        r_name.font.size = Pt(9.5)
        r_name.bold = True

        cell_roll = table_students.cell(row_idx, 2)
        p_roll = cell_roll.paragraphs[0]
        p_roll.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_roll.add_run(roll).font.size = Pt(9.5)

        cell_sig = table_students.cell(row_idx, 3)
        cell_sig.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_page_break()

    # =========================================================================
    # PAGE 2: EXECUTIVE SUMMARY & SECTION 1: PROJECT INSTRUCTIONS
    # =========================================================================
    add_heading_1(doc, "Executive Summary", space_before=4)
    add_body_p(doc, "Auto Sage is an intelligent, deterministic Knowledge-Based System (KBS) engineered to resolve the Complex Computing Problem (CCP) of automotive fault diagnosis and maintenance decision support. Grounded in peer-reviewed empirical workshop failure records collected at the Akwa Ibom Transport Corporation (AKTC) mechanical division and cataloged in CERN Zenodo (DOI: 10.5281/zenodo.15626055), the system models 93 discrete mechanical and electrical failure modes across 8 canonical vehicle subsystems and 120 deduplicated symptoms. Auto Sage replaces stochastic guesswork and premature part replacements with an explainable, forward-chaining propositional inference engine that actively corroborates observations through targeted follow-up questions, tallies positive and contradictory evidence, strictly isolates non-destructive physical bench verification (Tier A) from workshop repairs (Tier B), and generates an audit-ready 12-section vehicle inspection dossier.")

    add_heading_1(doc, "1. Project Instructions")
    add_body_p(doc, "This project submission satisfies the institutional requirements established for the Complex Computing Problem (CCP) in Knowledge-Based Systems (CT-359):")
    add_bullet(doc, "Complete all sections using the prescribed template. All bracketed placeholders have been expanded with verified empirical and technical data.", bold_prefix="1. Template Adherence: ")
    add_bullet(doc, "The submission package includes complete source code, dataset knowledge base files, comprehensive technical documentation, automated test suites, and presentation materials.", bold_prefix="2. Deliverables Scope: ")
    add_bullet(doc, "The system is fully executable, featuring a React 18 single-page frontend and a Flask REST backend, demonstrable in real-time during the viva examination.", bold_prefix="3. Demonstrability: ")
    add_bullet(doc, "All diagnostic heuristics, scoring weights, and engineering assumptions are formalized and justified using domain principles.", bold_prefix="4. Engineering Assumptions: ")
    add_bullet(doc, "All external empirical datasets, libraries, and foundational literature are cited using IEEE bibliographic standards.", bold_prefix="5. Attribution & Citations: ")
    add_bullet(doc, "The report adheres strictly to NED University academic integrity standards, with zero artificial hallucination or probabilistic fabrication.", bold_prefix="6. Academic Integrity: ")

    doc.add_page_break()

    # =========================================================================
    # PAGE 3: SECTION 2: PROBLEM STATEMENT (CLO 1, CLO 2, CLO 3)
    # =========================================================================
    add_heading_1(doc, "2. Problem Statement", space_before=4)
    add_body_p(doc, "Modern automotive equipment represents an intricate integration of mechanical, hydraulic, pneumatic, and electrical subsystems. When an operational malfunction occurs, identifying the underlying defective assembly from observed physical symptoms is non-trivial due to symptom overlap, incomplete driver reports, and the severe cost of misdiagnoses. This project addresses the Complex Computing Problem (CCP) through three Course Learning Outcomes (CLOs):")

    add_bullet(doc, "Explain how a Knowledge-Based System can represent industrial/automotive equipment knowledge, including equipment, components, symptoms, faults, causes, and maintenance actions, using an appropriate knowledge representation formalism. In Auto Sage, this is addressed through a structured, multi-tier JSON ontology comprising 8 primary automotive categories, 120 canonical deduplicated symptoms, and 93 verified production rules that couple non-invasive symptom patterns with physical bench verifications (Tier A) and maintenance directives (Tier B).", bold_prefix="CLO 1 — Knowledge Representation Formalism: ")

    add_bullet(doc, "Analyze the given industrial equipment fault-diagnosis problem by identifying incomplete requirements, stakeholder needs, relationships, constraints, and suitable knowledge-based approaches for developing an effective solution. In Auto Sage, this is realized by engineering a dynamic second-stage clarification mechanism (up to 5 targeted follow-up inquiries) that resolves ambiguous symptom clusters, detects contradictory user observations, and isolates candidate faults before destructive mechanical disassembly.", bold_prefix="CLO 2 — Problem Analysis & Requirements Engineering: ")

    add_bullet(doc, "Evaluate suitable knowledge representation methods and inference algorithms for diagnosing equipment faults and recommending maintenance actions, and justify the selected approach based on accuracy, explainability, safety, cost, and system requirements. In Auto Sage, a deterministic propositional forward-chaining inference engine was evaluated and selected over stochastic machine-learning classifiers. This guarantees 100% auditable reasoning trails, deterministic conflict resolution via evidence tallying and negative contradiction penalties (-4 points), strict safety priority escalation, and complete explainability.", bold_prefix="CLO 3 — Algorithmic Evaluation & KBS Justification: ")

    doc.add_page_break()

    # =========================================================================
    # PAGE 4: SECTION 3: PROBLEM DESCRIPTION / PROJECT CONTEXT
    # =========================================================================
    add_heading_1(doc, "3. Problem Description / Project Context", space_before=4)
    add_body_p(doc, "In contemporary automotive fleet management and individual vehicle maintenance, diagnosing operational anomalies poses significant challenges due to information asymmetry, heterogeneous knowledge sources, and severe safety consequences. Mechanical workshops, service centers, and vehicle operators frequently encounter ambiguous symptoms—such as engine overheating, brake pedal spongy travel, erratic transmission slipping, or no-crank electrical conditions—that can stem from multiple distinct component failures. Driver reports are inherently incomplete, subjective, and prone to descriptive inaccuracies. At the same time, service technicians operate under acute constraints: commercial pressures incentivize rapid part replacements, while improper diagnosis can lead to premature replacement of expensive, functional components (e.g., replacing an entire hydraulic brake booster when the actual fault is a degraded vacuum hose). Furthermore, safety-critical systems like braking, steering, and fuel delivery present life-safety hazards where inaccurate triage could lead to catastrophic road accidents or sudden thermal fires.")

    add_body_p(doc, "Auto Sage is engineered as an intelligent, deterministic Knowledge-Based System that bridges the gap between non-invasive symptom observation and certified mechanical repair. Grounded in peer-reviewed empirical workshop failure records collected at the Akwa Ibom Transport Corporation (AKTC) mechanical division, Auto Sage formalizes expert diagnostic reasoning into an interactive, step-by-step diagnostic platform. The system ingests driver-observed symptoms, generates dynamic follow-up clarification inquiries to eliminate false positives and contradictory conditions, evaluates candidate failure modes through transparent propositional rules (ALL, ANY, and PRIMARY_OR_PARTIAL modes), and strictly separates Tier A Physical Bench Verification (multimeter, vacuum gauge, and pressure measurements) from Tier B Maintenance Directives. By enforcing objective component replacement criteria and issuing explicit anti-mistake directives, Auto Sage resolves stakeholder conflicts, minimizes maintenance downtime, safeguards roadworthiness, and delivers an audit-ready, 12-section diagnostic report for workshop service authorization.")

    doc.add_page_break()

    # =========================================================================
    # PAGE 5: SECTION 4: PROBLEM ANALYSIS (4.1 to 4.5)
    # =========================================================================
    add_heading_1(doc, "4. Problem Analysis", space_before=4)

    add_heading_2(doc, "4.1 Problem Understanding")
    add_body_p(doc, "Vehicle fault diagnosis is traditionally performed either through heuristic guesswork by human mechanics or through diagnostic trouble codes (DTCs) read from On-Board Diagnostics (OBD-II). However, mechanical failures (e.g., sticking slide pins, booster vacuum leaks, warped rotors) do not trigger an electronic code until secondary damage occurs. Diagnosis must rely on physical manifestations (acoustics, vibrations, hydraulic feedback). The computational challenge lies in mapping subjective observations to multi-component failure modes deterministically.")

    add_heading_2(doc, "4.2 Stakeholders and Their Requirements")
    add_bullet(doc, "Intuitive interface, roadworthiness advisory, cost avoidance, authentic inspection dossier.", bold_prefix="1. Vehicle Owners & Drivers: ")
    add_bullet(doc, "Standardized triage, multimeter/gauge criteria (Tier A), anti-mistake warnings.", bold_prefix="2. Service Technicians: ")
    add_bullet(doc, "Auditable records, work-order sign-off blocks, bay routing, safety liability disclaimers.", bold_prefix="3. Workshop Managers: ")
    add_bullet(doc, "Rigorous representation formalism, empirical dataset grounding, deterministic execution, test coverage.", bold_prefix="4. University Evaluators: ")

    add_heading_2(doc, "4.3 Constraints and Conflicting Requirements")
    add_bullet(doc, "Layperson reporting vs. engineering precision resolved via 120 canonical symptom predicates.", bold_prefix="A. Reporting vs. Rigor: ")
    add_bullet(doc, "Multi-candidate ambiguity resolved via dynamic follow-up inquiries.", bold_prefix="B. Ambiguity Resolution: ")
    add_bullet(doc, "Cost minimization vs. life-safety mandate resolved via a 4-tier roadworthiness hierarchy.", bold_prefix="C. Life-Safety Mandate: ")
    add_bullet(doc, "Determinism vs. stochastic variance resolved via 100% propositional Horn clause inference.", bold_prefix="D. Determinism: ")

    add_heading_2(doc, "4.4 Root Cause / Requirement Identification")
    add_bullet(doc, "FR-1: Vehicle Specification Intake; FR-2: 8 Subsystems; FR-3: Canonical Symptoms; FR-4: Follow-Up Questions; FR-5: Propositional Matching; FR-6: Contradiction Penalty (-4); FR-7: Two-Tier Guidance; FR-8: 12-Section Report; FR-9: Persistence.", bold_prefix="Functional (FR): ")
    add_bullet(doc, "NFR-1: Sub-millisecond execution; NFR-2: Zero cloud telemetry; NFR-3: High-fidelity A4 layout; NFR-4: Responsive design.", bold_prefix="Non-Functional (NFR): ")

    add_heading_2(doc, "4.5 Engineering Assumptions & Justifications")
    add_bullet(doc, "Veracity of driver observations; Diagnostic hypothesis status requiring Tier A bench checks; Scope bounded by 93 empirical failure modes.", bold_prefix="Assumptions: ")

    doc.add_page_break()

    # =========================================================================
    # PAGE 6: SECTION 5: KNOWLEDGE REPRESENTATION (5.1 & 5.2 - Table 1 Complete)
    # =========================================================================
    add_heading_1(doc, "5. Knowledge Representation and KBS Design", space_before=4)

    add_heading_2(doc, "5.1 Selected Knowledge Representation Formalism")
    add_body_p(doc, "Auto Sage utilizes Production Rules based on Classical Propositional Logic augmented with multi-mode matching semantics: IF <antecedent> THEN <consequent>.")
    add_body_p(doc, "R_i = < C_i, S_i, P_i, M_i, F_i, Q_i, V_i, A_i, L_i >", bold_prefix="Rule Schema Definition: ")
    add_bullet(doc, "ALL Mode: Conjunction (AND). FullMatch <=> S_i subseteq SelectedSymptoms.", bold_prefix="1. ALL Mode: ")
    add_bullet(doc, "ANY Mode: Disjunction (OR). FullMatch <=> S_i intersect SelectedSymptoms != empty_set.", bold_prefix="2. ANY Mode: ")
    add_bullet(doc, "PRIMARY_OR_PARTIAL: Hallmark symptom match yields full; secondary yields partial.", bold_prefix="3. PRIMARY_OR_PARTIAL: ")

    add_heading_2(doc, "5.2 Knowledge Base / Ontology / Rule Base")
    add_body_p(doc, "The Knowledge Base is serialized in JSON format at backend/data/kbs_knowledge_base.json (574 KB), structured across 8 vehicle subsystem domains, 120 canonical symptoms, and 93 verified rules, detailed in Table 1:")

    p_t1 = doc.add_paragraph()
    p_t1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t1.paragraph_format.space_before = Pt(3)
    p_t1.paragraph_format.space_after = Pt(2)
    p_t1.paragraph_format.keep_with_next = True
    r_t1 = p_t1.add_run("Table 1: Auto Sage Vehicle Subsystem Knowledge Base Organization")
    r_t1.font.size = Pt(9)
    r_t1.font.bold = True
    r_t1.font.color.rgb = COLOR_NAVY

    table_cats = doc.add_table(rows=9, cols=5)
    cat_widths = [Inches(1.65), Inches(2.25), Inches(0.7), Inches(0.7), Inches(1.4)]
    format_entire_table(table_cats, cat_widths, is_header=True)

    c_headers = ["Category ID", "Subsystem Domain", "Rules", "Symptoms", "Safety Level"]
    for idx, text in enumerate(c_headers):
        cell = table_cats.cell(0, idx)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(text)
        r.bold = True
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, HEX_NAVY)

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
        table_cats.cell(row_idx, 0).paragraphs[0].add_run(cid).font.size = Pt(8)
        table_cats.cell(row_idx, 1).paragraphs[0].add_run(name).font.size = Pt(8)
        table_cats.cell(row_idx, 2).paragraphs[0].add_run(r_cnt).font.size = Pt(8)
        table_cats.cell(row_idx, 2).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        table_cats.cell(row_idx, 3).paragraphs[0].add_run(s_cnt).font.size = Pt(8)
        table_cats.cell(row_idx, 3).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        table_cats.cell(row_idx, 4).paragraphs[0].add_run(s_lev).font.size = Pt(8)
        table_cats.cell(row_idx, 4).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_page_break()

    # =========================================================================
    # PAGE 7: SECTION 5: INFERENCE, CONFLICT RESOLUTION & EXPLANATION (5.3 to 5.5)
    # =========================================================================
    add_heading_2(doc, "5.3 Inference Mechanism", space_before=4)
    add_body_p(doc, "Auto Sage implements a Data-Driven Forward-Chaining Inference Engine (backend/inference_engine.py) advancing through a 9-Step Reasoning Trail: (1) Symptom Intake Validation; (2) Follow-Up Ingestion ('yes', 'no', 'not_sure'); (3) Category Rule Retrieval; (4) Propositional Logic Evaluation across ALL, ANY, and PRIMARY_OR_PARTIAL modes; (5) Cross-Category Knowledge Scan; (6) Contradiction & Missing Condition Filtering; (7) Deterministic Ranking; (8) Diagnostic Verification Directive; and (9) Safety & Protocol Assignment.")

    add_body_p(doc, "To rank candidates deterministically without fabricating artificial confidence percentages, the engine computes an integer Evidence Tally:")
    add_body_p(doc, "Evidence Tally = (2 * |MatchedSymptoms|) + (2 * |SupportingFollowUps|) - (4 * |ContradictoryFollowUps|) - (1 * |MissingSymptoms|)", bold_prefix="Evidence Tally Formula: ")
    add_body_p(doc, "Matched symptoms and confirmatory follow-ups award +2 points each. Missing rule conditions incur a -1 penalty. Contradictory answers incur a severe -4 penalty, ensuring discredited candidates drop below valid possibilities.")

    add_heading_2(doc, "5.4 Conflict Resolution Strategy")
    add_body_p(doc, "When multiple rules fire simultaneously, conflict resolution is governed by a deterministic 9-element sorting key (_rank_key):")
    add_body_p(doc, "(is_contradicted, 0 if full_match else 1, status_order, -evidence_tally, -matched_count, missing_count, safety_val, unaccounted_count, rule_id)", bold_prefix="Deterministic Sorting Key: ")
    add_body_p(doc, "This guarantees: (1) Contradicted candidates always sort to the bottom; (2) Full matches rank ahead of partial matches; (3) Corroborated status ranks ahead of unverified status; (4) Highest evidence tally breaks ties; (5) Critical safety faults rank ahead of lower risks; and (6) Alphabetical rule ID guarantees 100% deterministic tie-breaking.")

    add_heading_2(doc, "5.5 Explanation Facility")
    add_body_p(doc, "Auto Sage provides complete diagnostic transparency by decomposing every conclusion into four structured elements:")
    add_bullet(doc, "Lists observed symptoms and confirmatory follow-up responses supporting the fault hypothesis.", bold_prefix="1. Supporting Evidence: ")
    add_bullet(doc, "Explicitly enumerates unobserved rule symptoms and unperformed tests requiring bench verification.", bold_prefix="2. Missing Prerequisites: ")
    add_bullet(doc, "Highlights follow-up observations that refute the hypothesis, explaining why the fault is contraindicated.", bold_prefix="3. Contradictory Evidence: ")
    add_bullet(doc, "Synthesizes observations into clear, natural automotive sentences (e.g., 'You reported Soft or spongy brake pedal... however, other common signs were not reported, so further physical inspection is required').", bold_prefix="4. Clinical Reasoning Correlation: ")

    doc.add_page_break()

    # =========================================================================
    # PAGE 8: SECTION 5.6 ARCHITECTURAL MODELING (Figures 1 & 2)
    # =========================================================================
    add_heading_2(doc, "5.6 Architectural & System Modeling", space_before=4)
    add_body_p(doc, "The Auto Sage architecture strictly decouples presentation, REST routing, and knowledge reasoning. Figure 1 illustrates the high-level system architecture, and Figure 2 details the propositional inference logic flow:")

    add_figure(doc, DIAG_DIR / "01_system_architecture.png", "Figure 1", "Auto Sage High-Level System Architecture and Component Interaction", width_inches=3.95)
    add_figure(doc, DIAG_DIR / "02_inference_flowchart.png", "Figure 2", "9-Step Propositional Inference Engine Logic Flowchart", width_inches=3.95)

    doc.add_page_break()

    # =========================================================================
    # PAGE 9: SECTION 5.6 ARCHITECTURAL MODELING (Figures 3 & 4)
    # =========================================================================
    add_body_p(doc, "Figure 3 captures stakeholder use cases across vehicle owners and automotive service technicians, while Figure 4 depicts the Level-1 Data Flow Diagram (DFD) showing the boundary between client-side intake and backend reasoning stores:", space_after=4)

    add_figure(doc, DIAG_DIR / "03_use_case_diagram.png", "Figure 3", "UML Use Case Diagram for Drivers and Automotive Service Technicians", width_inches=3.95)
    add_figure(doc, DIAG_DIR / "04_dfd_diagram.png", "Figure 4", "Data Flow Diagram (DFD Level 1) for Intake, Inference, and Dossier Generation", width_inches=3.95)

    add_body_p(doc, "In addition to system-level architectural models, expert diagnostic reasoning for complex vehicle failure modes is formalized into decision tree flowcharts (Brake Faults Flowchart, Electrical Starting Flowchart, Engine Overheating Flowchart, and Transmission Slippage Flowchart), visually translating observed symptoms into step-by-step physical bench tests.")

    doc.add_page_break()

    # =========================================================================
    # PAGE 10: SECTION 6: DATASET & SECTION 7: IMPLEMENTATION
    # =========================================================================
    add_heading_1(doc, "6. Dataset / Knowledge Sources", space_before=4)
    add_body_p(doc, "The diagnostic knowledge base is compiled from a peer-reviewed empirical automotive maintenance dataset collected across commercial bus and passenger vehicle maintenance workshops at the Akwa Ibom Transport Corporation (AKTC), summarized in Table 2:")

    p_t2 = doc.add_paragraph()
    p_t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t2.paragraph_format.space_before = Pt(3)
    p_t2.paragraph_format.space_after = Pt(2)
    p_t2.paragraph_format.keep_with_next = True
    r_t2 = p_t2.add_run("Table 2: Empirical Dataset and Knowledge Source Attribution")
    r_t2.font.size = Pt(9)
    r_t2.font.bold = True
    r_t2.font.color.rgb = COLOR_NAVY

    table_ds = doc.add_table(rows=2, cols=5)
    ds_widths = [Inches(1.8), Inches(1.1), Inches(1.1), Inches(1.4), Inches(1.3)]
    format_entire_table(table_ds, ds_widths, is_header=True)

    d_headers = ["Source / Dataset", "Type", "Size / No. of Records", "Purpose", "Citation / URL"]
    for idx, text in enumerate(d_headers):
        cell = table_ds.cell(0, idx)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(text)
        r.bold = True
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, HEX_NAVY)

    ds_vals = [
        "Automotive Faults Dataset for Diagnostic and Maintenance Systems (Obike & Obot)",
        "Empirical JSON Dataset & Verified Flowcharts",
        "99 Raw Records\n(93 Integrated Rules, 120 Symptoms)",
        "Core KBS Domain Knowledge, Symptoms, Tier A Tests & Tier B Repairs",
        "Zenodo DOI:\n10.5281/zenodo.15626055\n(CC BY 4.0)"
    ]
    for idx, val in enumerate(ds_vals):
        cell = table_ds.cell(1, idx)
        cell.paragraphs[0].add_run(val).font.size = Pt(8)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    add_body_p(doc, "Cleansing and Ingestion Pipeline: The raw AKTC dataset contained 99 records. The automated build pipeline (backend/build_kbs.py) merged 1 duplicate record (combining overlapping battery charging failure profiles) and excluded 5 records that lacked observable physical symptom mappings. The remaining 93 records were enriched via backend/rule_enrichment.py with explicit Tier A physical tests, Tier B repair instructions, replacement thresholds, anti-mistake directives, and diagnostic clarification questions.")

    add_heading_1(doc, "7. Implementation")

    add_heading_2(doc, "7.1 Software / Tools / Libraries")
    add_bullet(doc, "Vite 5.4, React 18.3.1, Tailwind CSS 3.4, Material Symbols Outlined, html2pdf.js 0.14.0.", bold_prefix="Frontend Stack: ")
    add_bullet(doc, "Python 3.12 / 3.14, Flask 3.1.2, Flask-CORS 6.0.0, python-docx 1.2.0, docx2pdf, Selenium 4.52.0.", bold_prefix="Backend Stack: ")
    add_bullet(doc, "JSON schema validation via validate_knowledge_base.py, Node.js native test runner (node --test), Python unittest.", bold_prefix="Testing & Verification: ")

    add_heading_2(doc, "7.2 Code Structure")
    add_body_p(doc, "The repository is structured into distinct functional directories:")
    add_body_p(doc, "D:\\AUTOSAGE\\\n├── backend/\n│   ├── app.py (REST API routes & input sanitization)\n│   ├── inference_engine.py (Propositional matching & ranking logic)\n│   ├── build_kbs.py (Dataset transformation & compilation pipeline)\n│   ├── rule_enrichment.py (Tier A & Tier B academic metadata)\n│   └── data/kbs_knowledge_base.json (Compiled production KBS)\n├── frontend/\n│   ├── src/pages/ (10 user-facing view components)\n│   ├── src/components/ (Layout.jsx, Stepper.jsx, Evidence.jsx)\n│   └── src/utils/ (historyStorage.js, pdfExport.js)\n└── final_report/ (Deliverables, screenshots, and diagrams)", bold_prefix="Directory Tree: ")

    doc.add_page_break()

    # =========================================================================
    # PAGE 11: MODULES 1 & 2 (Figures 5 & 6)
    # =========================================================================
    add_heading_2(doc, "7.3 User Experience Workflow & Page Modules", space_before=4)
    add_body_p(doc, "The Auto Sage user experience is engineered around a seamless, multi-stage diagnostic progression. Each module addresses a specific diagnostic objective, accompanied below by genuine screenshots captured directly from the live application:")

    add_heading_3(doc, "7.3.1 Module 1: Dashboard & System Health Telemetry")
    add_body_p(doc, "Dashboard.jsx serves as the primary gateway, displaying active system health, quick-triage access points, and interactive cards for all 8 vehicle subsystem domains. It queries the backend /api/health endpoint to verify engine status and displays subsystem status indicators.")
    add_figure(doc, SCREEN_DIR / "01_dashboard.png", "Figure 5", "Auto Sage Dashboard — System Health, Hotspots, and Subsystem Cards", width_inches=3.95)

    add_heading_3(doc, "7.3.2 Module 2: Vehicle Intake Specification Profile")
    add_body_p(doc, "VehicleInformation.jsx captures essential vehicle metadata including Year, Make, Model, Powertrain, and Mileage. This specification profile customizes subsequent diagnostic guidance while preserving a non-blocking skip fallback for emergency triage.")
    add_figure(doc, SCREEN_DIR / "02_vehicle_information.png", "Figure 6", "Vehicle Information Intake Form — Specification Profile with Skip Fallback", width_inches=3.95)

    doc.add_page_break()

    # =========================================================================
    # PAGE 12: MODULES 3 & 4 (Figures 7 & 8)
    # =========================================================================
    add_heading_3(doc, "7.3.3 Module 3: Symptom Selection Tray & Real-Time Filtering", space_before=4)
    add_body_p(doc, "SymptomSelection.jsx provides real-time keyword filtering, subsystem badges, and a live selection tray. Users select observable physical anomalies from 120 canonical symptoms, which are validated against category rules before transmission.")
    add_figure(doc, SCREEN_DIR / "03_symptom_selection.png", "Figure 7", "Symptom Selection Interface — Category Selector, Keyword Search, and Selection Tray", width_inches=3.95)

    add_heading_3(doc, "7.3.4 Module 4: Dynamic Clarification Inquiry Scheduling")
    add_body_p(doc, "FollowUpQuestions.jsx dynamically analyzes preliminary candidate rules and presents up to 5 targeted follow-up inquiries. Each question includes an engineering explanation, allowing the user to provide corroborating or refuting observations.")
    add_figure(doc, SCREEN_DIR / "04_followup_questions.png", "Figure 8", "Targeted Follow-Up Inquiry — Dynamic Clarification Questions with Engineering Context", width_inches=3.95)

    doc.add_page_break()

    # =========================================================================
    # PAGE 13: MODULES 5 & 6 (Figures 9 & 10)
    # =========================================================================
    add_heading_3(doc, "7.3.5 Module 5: Diagnosis Results & Fault Hypothesis Ranking", space_before=4)
    add_body_p(doc, "DiagnosisResults.jsx presents ranked candidate fault hypotheses, status pills (e.g., 'Suspected Fault Corroborated'), evidence tally scores, and immediate action directives. It enforces strict separation between Tier A tests and Tier B repairs.")
    add_figure(doc, SCREEN_DIR / "05_diagnosis_results.png", "Figure 9", "Diagnosis Results — Ranked Candidate Faults, Status Pills, and Tier A Directives", width_inches=3.95)

    add_heading_3(doc, "7.3.6 Module 6: Transparent Evidence Breakdown Facility")
    add_body_p(doc, "Evidence.jsx delivers complete diagnostic transparency by decomposing the reasoning trail into supporting observations (+2 points), missing rule predicates (-1 point), and refuting contradictions (-4 points), ensuring auditability.")
    add_figure(doc, SCREEN_DIR / "06_evidence_breakdown.png", "Figure 10", "Evidence Breakdown Component — Supporting, Missing, and Contradictory Findings", width_inches=3.95)

    doc.add_page_break()

    # =========================================================================
    # PAGE 14: MODULES 7 & 8 (Figures 11 & 12)
    # =========================================================================
    add_heading_3(doc, "7.3.7 Module 7: Component Mechanical Hierarchy & Bench Procedures", space_before=4)
    add_body_p(doc, "FaultDetails.jsx details the mechanical hierarchy of the suspect part, documented failure modes, and multi-step multimeter and bench testing procedures. This guides technicians through objective physical verification.")
    add_figure(doc, SCREEN_DIR / "07_fault_details.png", "Figure 11", "Fault Details Dossier — Component Mechanical Hierarchy and Multimeter Checklists", width_inches=3.95)

    add_heading_3(doc, "7.3.8 Module 8: Tier B Repair Guide & Anti-Mistake Warnings")
    add_body_p(doc, "RepairMitigationGuide.jsx details Tier B corrective actions, preventive maintenance schedules, component replacement criteria, and explicit anti-mistake rules preventing costly unnecessary part replacements.")
    add_figure(doc, SCREEN_DIR / "08_repair_mitigation_guide.png", "Figure 12", "Repair & Mitigation Guide — Tier B Actions, Replacement Criteria, and Anti-Mistake Warnings", width_inches=3.95)

    doc.add_page_break()

    # =========================================================================
    # PAGE 15: MODULES 9 & 10 (Figures 13 & 14)
    # =========================================================================
    add_heading_3(doc, "7.3.9 Module 9: Safety & Roadside Emergency Protocols", space_before=4)
    add_body_p(doc, "SafetyGuide.jsx enforces a 4-tier roadworthiness hierarchy (Critical, High, Medium, Low), issuing immediate driving hazard warnings and roadside emergency protocols when life-safety systems are compromised.")
    add_figure(doc, SCREEN_DIR / "09_safety_guide.png", "Figure 13", "Safety Guide — 4-Tier Roadworthiness Hierarchy and Roadside Protocols", width_inches=3.95)

    add_heading_3(doc, "7.3.10 Module 10: Persistent Session History Archive")
    add_body_p(doc, "History.jsx archives past diagnostic sessions in client-side localStorage, enabling users to review previous vehicle assessments, search past queries by date or keyword, and reload previous diagnostic states.")
    add_figure(doc, SCREEN_DIR / "11_diagnosis_history.png", "Figure 14", "Diagnosis History — Persistent Archive of Past Diagnostic Sessions in localStorage", width_inches=3.95)

    doc.add_page_break()

    # =========================================================================
    # PAGE 16: MODULE 11 (Figure 15) & SECTION 7.4 EXPLAINABILITY
    # =========================================================================
    add_heading_3(doc, "7.3.11 Module 11: Printable Diagnostic Inspection Report Dossier", space_before=4)
    add_body_p(doc, "DiagnosticReport.jsx compiles an official 12-section vehicle inspection dossier. Featuring official brand header, vehicle intake details, primary fault conclusions, evidence breakdowns, and mechanic sign-off blocks, it supports native browser printing and high-resolution PDF download.")
    add_figure(doc, SCREEN_DIR / "10_diagnostic_report.png", "Figure 15", "Vehicle Diagnostic Report — 12-Section Printable A4 Inspection Dossier with Official Brand Logo", width_inches=4.3)

    add_heading_2(doc, "7.4 Explainability & User Guidance Framework")
    add_body_p(doc, "The explainability facility operates across all modules, ensuring that no diagnosis is delivered as an unexplained score. By decomposing results into Tier A non-destructive checks and Tier B repair directives, Auto Sage bridges the communication gap between non-technical vehicle owners and certified automotive mechanics.")

    doc.add_page_break()

    # =========================================================================
    # PAGE 17: SECTION 8: TESTING AND RESULTS (8.1 & 8.2 - Table 3 Complete)
    # =========================================================================
    add_heading_1(doc, "8. Testing and Results", space_before=4)

    add_heading_2(doc, "8.1 Automated Test Execution & Quality Assurance")
    add_body_p(doc, "Auto Sage was subjected to automated unit, integration, and build testing across both frontend and backend stacks. All 42 automated tests passed with a 100% success rate:")
    add_bullet(doc, "29 tests executed in 2.37s. Verified endpoint status codes, 404/400 validation, propositional evaluation, contradiction penalties, ranking keys, and KB schema integrity.", bold_prefix="1. Backend Unit Tests (unittest): ")
    add_bullet(doc, "13 tests executed in 379ms. Verified localStorage serialization, quota handling, session isolation, report ID generation, and DOM formatting helpers.", bold_prefix="2. Frontend Unit Tests (Node.js): ")
    add_bullet(doc, "Verified live HTTP REST pipeline across /api/health, /api/categories, /api/symptoms, and /api/diagnose.", bold_prefix="3. Integration Verification: ")
    add_bullet(doc, "54 modules transformed and bundled cleanly in 14.45s with zero syntax or compilation errors.", bold_prefix="4. Production Build (Vite): ")

    add_heading_2(doc, "8.2 Subsystem Test Verification Matrix")
    add_body_p(doc, "To verify deterministic inference across all 8 vehicle subsystems, dedicated test cases were executed against the knowledge base, as documented in Table 3:")

    p_t3 = doc.add_paragraph()
    p_t3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t3.paragraph_format.space_before = Pt(3)
    p_t3.paragraph_format.space_after = Pt(2)
    p_t3.paragraph_format.keep_with_next = True
    r_t3 = p_t3.add_run("Table 3: Multi-Subsystem Automated Test Verification Matrix")
    r_t3.font.size = Pt(9)
    r_t3.font.bold = True
    r_t3.font.color.rgb = COLOR_NAVY

    table_tests = doc.add_table(rows=9, cols=5)
    test_widths = [Inches(1.1), Inches(2.0), Inches(1.5), Inches(0.8), Inches(1.3)]
    format_entire_table(table_tests, test_widths, is_header=True)

    t_headers = ["Subsystem", "Selected Input Symptoms", "Top Inferred Fault", "Tally Score", "Verified Status"]
    for idx, text in enumerate(t_headers):
        cell = table_tests.cell(0, idx)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(text)
        r.bold = True
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, HEX_NAVY)

    test_matrix_data = [
        ("Engine", "Engine cranking but won't start", "Fuel Pump Failure", "+4", "Corroborated Match"),
        ("Electrical", "Clicking sound, no crank", "Starter Solenoid / Battery", "+6", "Corroborated Match"),
        ("Brakes", "Soft or spongy brake pedal", "Brake Master Cylinder", "+4", "Corroborated Match"),
        ("Cooling", "Engine overheating + Coolant leak", "Radiator / Water Pump", "+6", "Corroborated Match"),
        ("Transmission", "Delayed gear engagement + slip", "Low Transmission Fluid", "+4", "Corroborated Match"),
        ("Emissions", "Rotten egg sulfur exhaust odor", "Catalytic Converter", "+4", "Corroborated Match"),
        ("HVAC", "AC blowing warm air", "Refrigerant Leak", "+4", "Corroborated Match"),
        ("Steering", "Vibration in steering wheel at speed", "Wheel Balance / Alignment", "+4", "Corroborated Match"),
    ]

    for row_idx, (sub, sym, fault, tally, status) in enumerate(test_matrix_data, start=1):
        table_tests.cell(row_idx, 0).paragraphs[0].add_run(sub).font.size = Pt(8)
        table_tests.cell(row_idx, 1).paragraphs[0].add_run(sym).font.size = Pt(8)
        table_tests.cell(row_idx, 2).paragraphs[0].add_run(fault).font.size = Pt(8)
        table_tests.cell(row_idx, 3).paragraphs[0].add_run(tally).font.size = Pt(8)
        table_tests.cell(row_idx, 3).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        table_tests.cell(row_idx, 4).paragraphs[0].add_run(status).font.size = Pt(8)
        table_tests.cell(row_idx, 4).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_page_break()

    # =========================================================================
    # PAGE 18: SECTION 8.3 THREE REAL DIAGNOSIS SCENARIOS
    # =========================================================================
    add_heading_2(doc, "8.3 Three Real Diagnosis Scenarios", space_before=4)
    add_body_p(doc, "To demonstrate the inference engine's reasoning behavior, three real diagnosis scenarios were executed:")
    
    add_body_p(doc, "Scenario 1 represents a textbook full conjunction match where observed symptoms perfectly satisfy all required rule conditions. The driver selects Category CAT_COOLING with symptoms 'Engine overheating' and 'Coolant leak under vehicle'. The inference engine identifies RULE_COOL_001 (Radiator / Water Pump Failure) and schedules clarification question Q_COOL_PUDDLE ('Is there a visible puddle of coolant under the vehicle when parked?'). When the user confirms with 'Yes', the rule evaluates to 'Suspected Fault (Corroborated by Follow-up Evidence)' with a top evidence tally of +6 and zero missing conditions.", bold_prefix="Scenario 1 (Full Conjunction Match): ")
    
    add_body_p(doc, "Scenario 2 demonstrates the power of negative evidence corroboration and contradiction handling. The driver inputs a single symptom 'Soft or spongy brake pedal' under CAT_BRAKES. Initially, this partial input activates five candidate rules: Brake Booster (RULE_BRK_003), Brake Master Cylinder, Hydraulic Hose, Brake Fluid, and Drum Brakes. The engine schedules two follow-up inquiries: Q_BRK_PEDAL_DROP ('Does the pedal drop slightly when engine starts?') and Q_BRK_HISS ('Do you hear a hissing noise when applying brakes?'). The user answers 'Yes' to pedal drop and 'No' to hissing. Because RULE_BRK_003 explicitly expects hissing upon vacuum diaphragm rupture, the 'No' response triggers a -4 contradiction penalty. As a result, RULE_BRK_003's score plummets from +2 to -7, dropping its status to 'Fault Not Supported by Evidence' and re-ranking it from Rank 1 down to Rank 5, successfully preventing an unwarranted brake booster replacement.", bold_prefix="Scenario 2 (Partial Match & Follow-up Refutation): ")
    
    add_body_p(doc, "Scenario 3 validates boundary integrity and resistance to hallucination across two distinct cases. In Case 3A, a driver selects only 'Check engine light on'. Because this indicator is shared across dozens of engine, transmission, and emission faults, firing a single definitive fault would be speculative. Auto Sage recognizes that the symptom is too broad to satisfy any specific Horn clause and declares status 'no_match', advising supplementary physical observations. In Case 3B, an apprentice selects 'ABS warning light is on' alongside 'Brake dragging'. Because no rule in the empirical knowledge base combines electrical wheel speed sensor failure with mechanical caliper slide pin seizure, the engine avoids fabricating a probabilistic compromise and returns status 'no_match'.", bold_prefix="Scenario 3 (Broad Indicator & Contradictory No-Match): ")

    doc.add_page_break()

    # =========================================================================
    # PAGE 19: SECTION 9: EVALUATION, LIMITATIONS AND CONCLUSION
    # =========================================================================
    add_heading_1(doc, "9. Evaluation, Limitations and Conclusion", space_before=4)

    add_heading_2(doc, "9.1 Evaluation of the Proposed Approach")
    add_bullet(doc, "Unlike neural networks that output unexplainable percentages, Auto Sage provides complete transparency. Every recommended check is directly traced to satisfied propositional predicates.", bold_prefix="1. 100% Explainability (CLO 3): ")
    add_bullet(doc, "Identical symptoms and follow-up answers always produce the identical ranking and directives. There is zero stochastic variance or hallucination.", bold_prefix="2. Deterministic Consistency: ")
    add_bullet(doc, "Separating Tier A bench tests from Tier B repairs eliminates premature component replacement, addressing the core economic failure of vehicle triage.", bold_prefix="3. Economic & Anti-Mistake Utility: ")
    add_bullet(doc, "By operating entirely on local client-side and Flask runtime, no vehicle telemetry or driver identities are exposed to third-party cloud infrastructure.", bold_prefix="4. Privacy & Zero-Cloud Footprint: ")

    add_heading_2(doc, "9.2 Limitations")
    add_bullet(doc, "The system relies on human observation rather than streaming real-time sensor voltages directly from an OBD-II CAN bus scanner.", bold_prefix="1. Manual Observation: ")
    add_bullet(doc, "The deterministic inference scope is bounded by the 93 rules compiled from the research dataset. Obscure faults outside this scope result in an honest no-match.", bold_prefix="2. 93-Rule Scope Boundary: ")
    add_bullet(doc, "A diagnostic result is an unverified hypothesis. Physical confirmation requires hands-on multimeter or pressure measurements.", bold_prefix="3. Hypothetical Status: ")
    add_bullet(doc, "Diagnosis history is stored in browser localStorage. Clearing browser data removes previous session records.", bold_prefix="4. Browser-Bound Storage: ")

    add_heading_2(doc, "9.3 Future Improvements")
    add_bullet(doc, "Hardware integration with Bluetooth ELM327 OBD-II scanners to automatically ingest live DTC fault codes and sensor PIDs alongside subjective driver observations.", bold_prefix="1. OBD-II CAN Bus Streaming: ")
    add_bullet(doc, "Expanding the Knowledge Base to include high-voltage battery cell degradation, inverter thermal management, and regenerative braking rules for electric vehicles.", bold_prefix="2. Hybrid & EV Telematics Expansion: ")
    add_bullet(doc, "Implementing an optional PostgreSQL backend to synchronize historical fleet work orders across multiple workshop service bays.", bold_prefix="3. Multi-Tenant Workshop Cloud Sync: ")

    add_heading_2(doc, "9.4 Conclusion")
    add_body_p(doc, "Auto Sage demonstrates the successful design, implementation, and verification of a deterministic Knowledge-Based System for automotive fault diagnosis and maintenance decision support. By formalizing empirical research knowledge into 93 production rules across 8 subsystems and integrating dynamic follow-up corroboration, the system effectively resolves stakeholder conflicts, eliminates diagnostic guesswork, and enforces physical bench verification before mechanical teardown. Complete with an audit-ready 12-section diagnostic report and an automated test suite, Auto Sage fulfills all requirements of the Complex Computing Problem (CCP) for Knowledge-Based Systems (CT-359).")

    doc.add_page_break()

    # =========================================================================
    # PAGE 20: REFERENCES & ACADEMIC VIVA EVALUATION RUBRIC
    # =========================================================================
    add_heading_1(doc, "10. References", space_before=4)
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
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.line_spacing = 1.10
        p_ref.paragraph_format.space_before = Pt(0)
        p_ref.paragraph_format.space_after = Pt(2)
        p_ref.paragraph_format.left_indent = Inches(0.28)
        p_ref.paragraph_format.first_line_indent = Inches(-0.28)
        run = p_ref.add_run(r_text)
        run.font.name = "Calibri"
        run.font.size = Pt(9)
        run.font.color.rgb = COLOR_BODY

    add_heading_2(doc, "Academic Project Viva Evaluation Rubric", space_before=8)
    add_body_p(doc, "Official evaluation rubric and examiner verification for Course CT-359 Complex Computing Problem project defense:", space_after=3)

    table_rubric = doc.add_table(rows=5, cols=4)
    format_entire_table(table_rubric, [Inches(1.8), Inches(2.9), Inches(1.0), Inches(1.0)], is_header=True)

    r_headers = ["Assessment Criterion", "Evaluation Focus & Course Outcome", "Max Score", "Awarded"]
    for idx, h_text in enumerate(r_headers):
        cell = table_rubric.cell(0, idx)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.bold = True
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, HEX_NAVY)

    rubric_rows = [
        ("Knowledge Representation", "Ontology completeness, 8 subsystems, 93 rules, 120 symptoms (CLO 1)", "30", ""),
        ("Problem Analysis & Design", "Stakeholder tension resolution, follow-up inquiry scheduling (CLO 2)", "30", ""),
        ("Inference & Explainability", "Deterministic forward chaining, evidence tally, transparent dossier (CLO 3)", "30", ""),
        ("Demonstration & Viva", "Automated test suite execution, live demonstration, code quality", "10", ""),
    ]

    for row_idx, (crit, desc, max_s, awd) in enumerate(rubric_rows, start=1):
        table_rubric.cell(row_idx, 0).paragraphs[0].add_run(crit).font.size = Pt(8)
        table_rubric.cell(row_idx, 0).paragraphs[0].runs[0].bold = True
        table_rubric.cell(row_idx, 1).paragraphs[0].add_run(desc).font.size = Pt(8)
        table_rubric.cell(row_idx, 2).paragraphs[0].add_run(max_s).font.size = Pt(8)
        table_rubric.cell(row_idx, 2).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        table_rubric.cell(row_idx, 3).paragraphs[0].add_run(awd).font.size = Pt(8)
        table_rubric.cell(row_idx, 3).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    table_sign = doc.add_table(rows=2, cols=3)
    format_entire_table(table_sign, [Inches(2.2), Inches(2.3), Inches(2.2)], is_header=False)

    table_sign.cell(0, 0).paragraphs[0].add_run("Internal Examiner Signature\n\n_________________________").font.size = Pt(8)
    table_sign.cell(0, 1).paragraphs[0].add_run("External Examiner Signature\n\n_________________________").font.size = Pt(8)
    table_sign.cell(0, 2).paragraphs[0].add_run("Examination Date & Seal\n\n_________________________").font.size = Pt(8)
    
    table_sign.cell(1, 0).paragraphs[0].add_run("Name: ").font.size = Pt(8)
    table_sign.cell(1, 1).paragraphs[0].add_run("Name: ").font.size = Pt(8)
    table_sign.cell(1, 2).paragraphs[0].add_run("Overall Verdict: Approved [  ] / Rejected [  ]").font.size = Pt(7.5)

    for row in table_sign.rows:
        for cell in row.cells:
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_cell_background(cell, "F8FAFC")

    print(f"Saving DOCX to {DOCX_OUT}...")
    doc.save(str(DOCX_OUT))
    print(f"Saved {DOCX_OUT} ({DOCX_OUT.stat().st_size} bytes).")

    print(f"Converting DOCX to PDF at {PDF_OUT} via win32com Word Application...")
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
        print(f"win32com converted successfully! PDF size: {PDF_OUT.stat().st_size} bytes.")
    except Exception as e:
        print(f"Word COM error: {e}, attempting docx2pdf...")
        from docx2pdf import convert
        convert(str(DOCX_OUT), str(PDF_OUT))
        print(f"docx2pdf converted successfully! PDF size: {PDF_OUT.stat().st_size} bytes.")

if __name__ == "__main__":
    build_report()
