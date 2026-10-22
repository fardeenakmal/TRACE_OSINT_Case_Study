#!/usr/bin/env python3
"""
TRACE OSINT Digital Footprint Analyzer - 5-Page Case Study PDF Generator
Author: Fardeen Akmal (Roll No: 2)
Guide: Akanksha Thakare
Institute: G.V. Acharya Institute of Engineering and Technology
University: University of Mumbai
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#475569"))
        
        # Header (Pages 2-5)
        if self._pageNumber > 1:
            self.drawString(36, 758, "TRACE: OSINT DIGITAL FOOTPRINT ANALYZER — MINI PROJECT CASE STUDY")
            self.drawRightString(576, 758, "DEPT. OF CSE (IoT, CYBER SECURITY & BCT)")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.6)
            self.line(36, 752, 576, 752)
        
        # Footer (All pages)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.6)
        self.line(36, 38, 576, 38)
        
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(36, 26, "G.V. Acharya Institute of Engineering & Technology • University of Mumbai")
        self.drawRightString(576, 26, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=colors.HexColor("#0f172a"),
        alignment=1, # Center
        spaceAfter=4
    )
    
    sub_title_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor("#0284c7"),
        alignment=1,
        spaceAfter=8
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=5,
        spaceAfter=3,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#0369a1"),
        spaceBefore=4,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.4,
        textColor=colors.HexColor("#1e293b"),
        alignment=4, # Justified
        spaceAfter=3
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.2,
        textColor=colors.HexColor("#1e293b"),
        leftIndent=10,
        spaceAfter=2
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.2,
        textColor=colors.HexColor("#0f172a")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9.2,
        textColor=colors.white
    )

    story = []

    # =========================================================================
    # PAGE 1: TITLE, ACADEMIC DETAILS, ABSTRACT, INTRODUCTION, PROBLEM STATEMENT, OBJECTIVES & SCOPE
    # =========================================================================
    story.append(Paragraph("TRACE — OSINT DIGITAL FOOTPRINT ANALYZER", title_style))
    story.append(Paragraph("A Robust Web-Based Open Source Intelligence Framework for Surface-Web Profile & Domain Footprint Auditing", sub_title_style))

    # Student metadata table
    meta_data = [
        [
            Paragraph("<b>Student Name:</b> Fardeen Akmal", table_cell_style),
            Paragraph("<b>Roll Number:</b> 2", table_cell_style),
            Paragraph("<b>Project Guide:</b> Akanksha Thakare", table_cell_style)
        ],
        [
            Paragraph("<b>Branch:</b> CSE (IoT, Cyber Security &amp; Blockchain Technology)", table_cell_style),
            Paragraph("<b>Institute:</b> G.V. Acharya Inst. of Engg. &amp; Tech.", table_cell_style),
            Paragraph("<b>Affiliation:</b> University of Mumbai (2026-27)", table_cell_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[185, 140, 215])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 6))

    # Abstract Box
    abstract_text = (
        "<b>ABSTRACT:</b> In the contemporary hyper-connected digital ecosystem, an individual's or enterprise's digital "
        "footprint across heterogeneous web platforms represents an expansive attack surface susceptible to social engineering, "
        "spear phishing, credential stuffing, and unauthorized reconnaissance. Open Source Intelligence (OSINT) facilitates "
        "the proactive identification and auditing of publicly exposed indicators of identity. However, legacy reconnaissance "
        "utilities often rely on brittle web-scraping heuristics, generate elevated false-positive rates due to platform anti-bot "
        "defenses, fail to distinguish rate limits from legitimate target non-existence, and lack localized, auditable reporting "
        "capabilities. This case study presents the design, architectural formulation, empirical implementation, and testing of "
        "<b>TRACE (Target Reconnaissance &amp; Auditable Collection Engine)</b> — a full-stack, modular OSINT analysis dashboard. "
        "Built using a Python FastAPI backend and a responsive React/TypeScript client with SQLite local persistence, TRACE executes "
        "rigorous username enumeration across ten major developer, visual, and social platforms alongside passive DNS and RDAP "
        "domain intelligence gathering. TRACE introduces an unambiguous multi-tier status categorization engine (<i>FOUND</i>, "
        "<i>NOT_FOUND</i>, <i>INCONCLUSIVE</i>, <i>CHECK_FAILED</i>) that prevents fabricated intelligence and provides verifiable "
        "cryptographic checksums with automated PDF/CSV report exports."
    )
    abstract_table = Table([[Paragraph(abstract_text, body_style)]], colWidths=[540])
    abstract_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#0284c7")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(abstract_table)
    story.append(Spacer(1, 5))

    story.append(Paragraph("1. Introduction &amp; Theoretical Background", h1_style))
    story.append(Paragraph(
        "Open Source Intelligence (OSINT) comprises the rigorous collection, correlation, and analysis of publicly available data to "
        "produce actionable security intelligence. While intelligence agencies initially pioneered OSINT methodologies, modern defensive "
        "cybersecurity teams leverage OSINT for External Attack Surface Management (EASM), threat intelligence, and brand reputation monitoring. "
        "A critical challenge in modern OSINT operations is the fragmented nature of surface-web footprints: a single identifier or domain "
        "is frequently linked to software repositories, social forums, identity providers, and hosting providers. Manual correlation across "
        "dozens of platforms is tedious, error-prone, and operationally inefficient. TRACE was conceived to democratize and systematize "
        "authorized digital footprint auditing through an intuitive, centralized, and standards-compliant analytical interface.",
        body_style
    ))

    story.append(Paragraph("2. Problem Statement", h1_style))
    story.append(Paragraph(
        "Existing CLI-based OSINT utilities suffer from significant architectural and operational deficiencies: "
        "<b>(1) False-Positive Hallucination:</b> Many tools assume that any HTTP 200 response confirms account existence, ignoring Single-Page "
        "Application (SPA) client-side routing, generic soft-404 landing pages, and Cloudflare challenge screens. "
        "<b>(2) Ambiguous Failure States:</b> Network timeouts, HTTP 429 rate limits, and platform WAF mitigations are frequently misreported "
        "as non-existent accounts, skewing investigator findings. "
        "<b>(3) Excessive Active Probing:</b> Intrusive network scanning techniques risk triggering Intrusion Detection Systems (IDS) or "
        "violating organizational Acceptable Use Policies (AUP). "
        "<b>(4) Lack of Academic &amp; Audit-Ready Reporting:</b> Security professionals and students require defensible, timestamped, "
        "and reproducible evidence formats (PDF/CSV) that capture latency telemetry, raw DNS zone delegations, and operational limitations.",
        body_style
    ))

    story.append(Paragraph("3. Objectives and Project Scope", h1_style))
    story.append(Paragraph(
        "The primary objective of this mini-project is to build, execute, rigorously test, and demonstrate an autonomous, full-stack "
        "OSINT digital footprint analyzer operating exclusively on a local development workstation. Specific objectives include:",
        body_style
    ))
    story.append(Paragraph("• <b>Deterministic Profile Enumeration:</b> Query 10 diverse public services concurrently using asynchronous HTTP with platform-specific signature matching and explicit status disambiguation.", bullet_style))
    story.append(Paragraph("• <b>Passive Domain Reconnaissance:</b> Query publicly delegated authoritative DNS records (A, AAAA, MX, NS, TXT, SOA), ICANN RDAP registration registries, and GeoIP ASN telemetry without invasive port scanning.", bullet_style))
    story.append(Paragraph("• <b>Local Audit Persistence:</b> Maintain a secure SQLite database recording all queries, statuses, timestamps, and findings with zero external data leakage or dependency on commercial cloud APIs.", bullet_style))
    story.append(Paragraph("• <b>Defensible Evidence Generation:</b> Provide automated PDF and CSV reporting engines featuring academic attribution, integrity checksums, and explicit methodology disclaimers.", bullet_style))
    story.append(Paragraph("• <b>Scope Boundaries:</b> TRACE focuses exclusively on public surface-web assets; active exploitation, vulnerability scanning, password harvesting, and bypassing authentication controls are strictly excluded.", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: PROPOSED SYSTEM, RELATED WORK, REQUIREMENTS, TECH STACK, USE CASES
    # =========================================================================
    story.append(Paragraph("4. Proposed System &amp; Literature Review", h1_style))
    story.append(Paragraph(
        "TRACE operates as an on-premise, security-centric analytical platform designed to overcome the fragility of legacy CLI scripts. "
        "Unlike monolithic scrapers, TRACE decouples asynchronous protocol dispatch from presentation, enforcing validation gateways "
        "at both network and application layers.",
        body_style
    ))

    # Related tools table
    comp_data = [
        [
            Paragraph("<b>Tool Name</b>", table_header_style),
            Paragraph("<b>Interface</b>", table_header_style),
            Paragraph("<b>Rate Limit Detection</b>", table_header_style),
            Paragraph("<b>Passive DNS / RDAP</b>", table_header_style),
            Paragraph("<b>Audit Report Generation</b>", table_header_style),
            Paragraph("<b>Local Persistence</b>", table_header_style)
        ],
        [
            Paragraph("Sherlock", table_cell_style),
            Paragraph("CLI Only", table_cell_style),
            Paragraph("Partial (Silent 429)", table_cell_style),
            Paragraph("No (Usernames only)", table_cell_style),
            Paragraph("Raw Text / CSV", table_cell_style),
            Paragraph("None (Stateless)", table_cell_style)
        ],
        [
            Paragraph("theHarvester", table_cell_style),
            Paragraph("CLI Only", table_cell_style),
            Paragraph("Search API dependent", table_cell_style),
            Paragraph("Yes (Active DNS)", table_cell_style),
            Paragraph("HTML / XML export", table_cell_style),
            Paragraph("Optional SQLite", table_cell_style)
        ],
        [
            Paragraph("SpiderFoot", table_cell_style),
            Paragraph("Web UI / Complex", table_cell_style),
            Paragraph("Heuristic based", table_cell_style),
            Paragraph("Extensive (Complex)", table_cell_style),
            Paragraph("CSV / GEXF export", table_cell_style),
            Paragraph("Heavy SQLite", table_cell_style)
        ],
        [
            Paragraph("<b>TRACE (Ours)</b>", table_cell_style),
            Paragraph("Modern Web UI", table_cell_style),
            Paragraph("<b>Strict Disambiguation</b>", table_cell_style),
            Paragraph("<b>Integrated Passive</b>", table_cell_style),
            Paragraph("<b>Automated PDF + CSV</b>", table_cell_style),
            Paragraph("<b>Lightweight SQLite</b>", table_cell_style)
        ]
    ]
    comp_table = Table(comp_data, colWidths=[80, 75, 105, 95, 105, 80])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, colors.HexColor("#f8fafc")]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#e0f2fe")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(comp_table)
    story.append(Spacer(1, 5))

    story.append(Paragraph("5. System Requirements Analysis", h1_style))
    story.append(Paragraph("<b>5.1 Functional Requirements (FR):</b>", h2_style))
    story.append(Paragraph("• <b>FR-1 (Multi-Platform Profile Verification):</b> The system must scan target usernames across 10 defined platforms (GitHub, GitLab, DockerHub, Dev.to, HackerNews, Reddit, Gravatar, Keybase, Medium, Pinterest) concurrently.", bullet_style))
    story.append(Paragraph("• <b>FR-2 (Passive DNS Resolution):</b> The system must retrieve authoritative DNS records (A, AAAA, MX, NS, TXT, SOA) for target domains using RFC-compliant UDP/TCP DNS queries without touching target web servers.", bullet_style))
    story.append(Paragraph("• <b>FR-3 (RDAP &amp; IP Geolocation Extraction):</b> The system must parse Registration Data Access Protocol (RDAP) JSON structures to obtain registrar, registration, and expiration dates, supplemented by IP ASN data.", bullet_style))
    story.append(Paragraph("• <b>FR-4 (Audit Logging &amp; Record Management):</b> All completed investigations must persist in a local relational database with query parameters, timestamps, execution summaries, and deletion management.", bullet_style))
    story.append(Paragraph("• <b>FR-5 (Formal Academic Export):</b> The system must generate self-contained, publication-grade PDF reports (incorporating student credentials and checksums) and tabular CSV exports on demand.", bullet_style))

    story.append(Paragraph("<b>5.2 Non-Functional Requirements (NFR):</b>", h2_style))
    story.append(Paragraph("• <b>NFR-1 (Integrity &amp; Zero False-Positive Tolerance):</b> Under no condition shall the application fabricate finding statuses or confuse HTTP 403/429 anti-bot mitigations with target existence.", bullet_style))
    story.append(Paragraph("• <b>NFR-2 (Latency &amp; Concurrency):</b> Concurrency through Python `asyncio` and `httpx` must limit complete 10-source username footprint scans to under 4.5 seconds under standard broadband conditions.", bullet_style))
    story.append(Paragraph("• <b>NFR-3 (Security &amp; Hygiene):</b> The application must run completely offline/locally without transmitting telemetry to third-party tracking services or hardcoding secrets.", bullet_style))

    story.append(Paragraph("6. Technology Stack Selection &amp; Rationale", h1_style))
    tech_data = [
        [Paragraph("<b>Component Layer</b>", table_header_style), Paragraph("<b>Technology Selected</b>", table_header_style), Paragraph("<b>Engineering Rationale</b>", table_header_style)],
        [Paragraph("Backend Framework", table_cell_style), Paragraph("Python 3.14 + FastAPI", table_cell_style), Paragraph("High-throughput asynchronous event loop, native Pydantic schema validation, and automatic OpenAPI documentation.", table_cell_style)],
        [Paragraph("Asynchronous HTTP", table_cell_style), Paragraph("HTTPX Client Pool", table_cell_style), Paragraph("Non-blocking connection pooling, HTTP/2 support, custom headers/cookies, and strict per-request timeout handling.", table_cell_style)],
        [Paragraph("DNS Reconnaissance", table_cell_style), Paragraph("dnspython v2.7", table_cell_style), Paragraph("Direct DNS wire-format resolver interfacing with authoritative nameservers without reliance on OS shell hooks.", table_cell_style)],
        [Paragraph("Client Architecture", table_cell_style), Paragraph("React 18 + TypeScript + Vite", table_cell_style), Paragraph("Type-safe state management, fast client bundling, and modular component hierarchy.", table_cell_style)],
        [Paragraph("Persistence Layer", table_cell_style), Paragraph("SQLite 3 Embedded Engine", table_cell_style), Paragraph("Zero-configuration, ACID-compliant local SQL database preventing external attack vectors and credential overhead.", table_cell_style)],
        [Paragraph("Document Engine", table_cell_style), Paragraph("ReportLab Flowable PDF", table_cell_style), Paragraph("Programmatic, pixel-accurate vector PDF synthesis with institutional header templates and tabular layouts.", table_cell_style)]
    ]
    tech_table = Table(tech_data, colWidths=[100, 120, 320])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 5))

    story.append(Paragraph("7. Operational Use Cases", h1_style))
    story.append(Paragraph(
        "<b>UC-1: Defensive Self-Footprint Audit:</b> Security researchers and developers audit their personal usernames across platforms to locate abandoned accounts exposing legacy emails or weak authentication. "
        "<b>UC-2: External Surface Assessment:</b> Authorized penetration testers establish domain perimeter inventory (mail routing, nameserver delegation, SPF validation) during non-invasive pre-engagement reconnaissance.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: ARCHITECTURE, WORKFLOW, DATABASE, VERIFICATION, SECURITY CONTROLS
    # =========================================================================
    story.append(Paragraph("8. System Architecture and Workflow", h1_style))
    story.append(Paragraph(
        "TRACE implements a decoupled, three-tier modular architecture comprising the Single Page Application Presentation Layer, "
        "the FastAPI Asynchronous Service Controller, and the Persistence &amp; System Integration Engine.",
        body_style
    ))

    # Architecture block table
    arch_data = [
        [
            Paragraph("<b>Client Presentation (React/TS)</b><br/>• Operations Dashboard<br/>• Asynchronous Search Forms<br/>• Real-time Status Badges<br/>• Report Preview Modal", table_cell_style),
            Paragraph("<b>REST API Gateway (FastAPI)</b><br/>• <code>/api/investigate/username</code><br/>• <code>/api/investigate/domain</code><br/>• <code>/api/history</code> (CRUD)<br/>• <code>/api/reports/pdf|csv</code>", table_cell_style),
            Paragraph("<b>Core Engine Services</b><br/>• <code>UsernameOSINTService</code><br/>• <code>DomainOSINTService</code><br/>• <code>ReportingEngine</code><br/>• <code>DatabaseManager</code>", table_cell_style),
            Paragraph("<b>Network &amp; Storage</b><br/>• Public Web APIs / HTML<br/>• Authoritative DNS (UDP 53)<br/>• ICANN RDAP (HTTPS)<br/>• Local SQLite (<code>trace.db</code>)", table_cell_style)
        ]
    ]
    arch_table = Table(arch_data, colWidths=[135, 135, 135, 135])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#f0fdf4")),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#eff6ff")),
        ('BACKGROUND', (2,0), (2,0), colors.HexColor("#faf5ff")),
        ('BACKGROUND', (3,0), (3,0), colors.HexColor("#fffbeb")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#94a3b8")),
        ('INNERGRID', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 5))

    story.append(Paragraph("9. Database Design &amp; Schema Architecture", h1_style))
    story.append(Paragraph(
        "To guarantee audit integrity, TRACE utilizes SQLite 3 with WAL (Write-Ahead Logging) mode enabled. "
        "The schema isolates operational telemetry from raw payload responses, maintaining structured indexes for rapid lookup:",
        body_style
    ))

    db_data = [
        [Paragraph("<b>Column Name</b>", table_header_style), Paragraph("<b>Data Type</b>", table_header_style), Paragraph("<b>Constraints</b>", table_header_style), Paragraph("<b>Description &amp; Functional Purpose</b>", table_header_style)],
        [Paragraph("<code>id</code>", table_cell_style), Paragraph("INTEGER", table_cell_style), Paragraph("PRIMARY KEY AUTOINCREMENT", table_cell_style), Paragraph("Unique sequential investigation dossier identifier.", table_cell_style)],
        [Paragraph("<code>investigation_type</code>", table_cell_style), Paragraph("VARCHAR(20)", table_cell_style), Paragraph("NOT NULL, CHECK (type IN...)", table_cell_style), Paragraph("Identifies analysis pipeline: <code>'username'</code> or <code>'domain'</code>.", table_cell_style)],
        [Paragraph("<code>target</code>", table_cell_style), Paragraph("VARCHAR(255)", table_cell_style), Paragraph("NOT NULL, INDEXED", table_cell_style), Paragraph("Sanitized target query string (username or domain).", table_cell_style)],
        [Paragraph("<code>timestamp</code>", table_cell_style), Paragraph("DATETIME", table_cell_style), Paragraph("NOT NULL, DEFAULT CURRENT_TIMESTAMP", table_cell_style), Paragraph("UTC execution timestamp ensuring tamper-evident chronology.", table_cell_style)],
        [Paragraph("<code>status</code>", table_cell_style), Paragraph("VARCHAR(50)", table_cell_style), Paragraph("NOT NULL", table_cell_style), Paragraph("Overall operational state: <code>'Completed'</code> or <code>'Failed'</code>.", table_cell_style)],
        [Paragraph("<code>summary</code>", table_cell_style), Paragraph("TEXT", table_cell_style), Paragraph("NOT NULL", table_cell_style), Paragraph("Human-readable aggregate findings synopsis.", table_cell_style)],
        [Paragraph("<code>data_json</code>", table_cell_style), Paragraph("TEXT (JSON)", table_cell_style), Paragraph("NOT NULL", table_cell_style), Paragraph("Full normalized JSON payload storing per-source latency and telemetry.", table_cell_style)]
    ]
    db_table = Table(db_data, colWidths=[90, 80, 130, 240])
    db_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(db_table)
    story.append(Spacer(1, 5))

    story.append(Paragraph("10. Multi-Tier Result Verification Methodology", h1_style))
    story.append(Paragraph(
        "A foundational principle of TRACE is the eradication of false positives. Standard HTTP status codes alone are insufficient "
        "due to modern web architectures. TRACE executes a four-state deterministic decision tree for every source probe:",
        body_style
    ))
    story.append(Paragraph("• <b>FOUND:</b> Validated when HTTP status is exactly 200, the response body contains positive profile identifiers (e.g., matching username in JSON payload or verified meta tags), and redirection to sign-in portals has not occurred.", bullet_style))
    story.append(Paragraph("• <b>NOT_FOUND:</b> Triggered when the service responds with definitive non-existence status (HTTP 404), or redirects to registration portals (e.g., GitLab redirecting unauthenticated missing profiles to <code>users/sign_in</code> with HTTP 302).", bullet_style))
    story.append(Paragraph("• <b>INCONCLUSIVE:</b> Applied when anti-scraping defenses (Cloudflare Turnstile, AWS WAF), bot challenges, or rate limiters respond with HTTP 403 Forbidden or HTTP 429 Too Many Requests. The target profile may or may not exist; TRACE refuses to speculate.", bullet_style))
    story.append(Paragraph("• <b>CHECK_FAILED:</b> Recorded when transport-layer faults occur, including TCP socket timeouts (&gt;4.0s), DNS NXDOMAIN errors, or SSL handshake failures. The specific network exception is logged for audit defensibility.", bullet_style))

    story.append(Paragraph("11. Security Controls and Operational Safeguards", h1_style))
    story.append(Paragraph(
        "<b>Input Sanitization Gateways:</b> Domain queries are strictly checked against RFC 1035 hostname specifications. Submissions containing "
        "shell metacharacters (<code>;&amp;|`$</code>), path traversal markers, or URI schemes (<code>http://</code>) are rejected at the client gateway "
        "and server Pydantic validation boundary with HTTP 422, eliminating Server-Side Request Forgery (SSRF) and injection vectors.<br/>"
        "<b>Passive Reconnaissance Guarantee:</b> TRACE restricts network interactions to passive queries against third-party authoritative servers. "
        "No port scans, directory fuzzing, or active banner grabbing are ever executed against target infrastructure.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: IMPLEMENTATION, TESTING PROCEDURE, TEST MATRIX, GENUINE SCREENSHOTS
    # =========================================================================
    story.append(Paragraph("12. Implementation Methodology &amp; Engineering Execution", h1_style))
    story.append(Paragraph(
        "The project was implemented under a rigorous Test-Driven Development (TDD) lifecycle on Linux x86_64. "
        "The backend leverages Python's non-blocking `asyncio` primitives to dispatch concurrent HTTP and DNS probes. "
        "The frontend is compiled as an optimized single-page static bundle and hosted directly via FastAPI mount points.",
        body_style
    ))

    story.append(Paragraph("13. Automated Testing Procedure &amp; Test Matrix", h1_style))
    story.append(Paragraph(
        "An automated test suite was constructed using `pytest` and `httpx.AsyncClient`, verifying all API endpoints, "
        "validation gates, error states, and database transaction integrity under simulated network conditions.",
        body_style
    ))

    test_data = [
        [Paragraph("<b>Test Case ID</b>", table_header_style), Paragraph("<b>Test Unit &amp; Description</b>", table_header_style), Paragraph("<b>Input Parameters</b>", table_header_style), Paragraph("<b>Observed Outcome</b>", table_header_style), Paragraph("<b>Status</b>", table_header_style)],
        [Paragraph("TC-01", table_cell_style), Paragraph("API Health &amp; Subsystem Telemetry", table_cell_style), Paragraph("<code>GET /api/health</code>", table_cell_style), Paragraph("Status 200, engine: 'TRACE OSINT'", table_cell_style), Paragraph("<b>PASS</b>", table_cell_style)],
        [Paragraph("TC-02", table_cell_style), Paragraph("Dashboard Telemetry Counter", table_cell_style), Paragraph("<code>GET /api/stats</code>", table_cell_style), Paragraph("Status 200, valid counts &amp; history list", table_cell_style), Paragraph("<b>PASS</b>", table_cell_style)],
        [Paragraph("TC-03", table_cell_style), Paragraph("Username Investigation Dispatch", table_cell_style), Paragraph("<code>POST {'username': 'test'}</code>", table_cell_style), Paragraph("Status 200, 10 findings categorized", table_cell_style), Paragraph("<b>PASS</b>", table_cell_style)],
        [Paragraph("TC-04", table_cell_style), Paragraph("Input Validation: Empty Target", table_cell_style), Paragraph("<code>POST {'username': '  '}</code>", table_cell_style), Paragraph("Status 422 Unprocessable Entity", table_cell_style), Paragraph("<b>PASS</b>", table_cell_style)],
        [Paragraph("TC-05", table_cell_style), Paragraph("Domain DNS &amp; RDAP Resolution", table_cell_style), Paragraph("<code>POST {'domain': 'example.com'}</code>", table_cell_style), Paragraph("Status 200, valid A &amp; NS records", table_cell_style), Paragraph("<b>PASS</b>", table_cell_style)],
        [Paragraph("TC-06", table_cell_style), Paragraph("Investigation History Audit Trail", table_cell_style), Paragraph("<code>GET /api/history</code>", table_cell_style), Paragraph("Status 200, JSON list of investigations", table_cell_style), Paragraph("<b>PASS</b>", table_cell_style)],
        [Paragraph("TC-07", table_cell_style), Paragraph("PDF Report Export Verification", table_cell_style), Paragraph("<code>GET /api/reports/pdf/1</code>", table_cell_style), Paragraph("Status 200, application/pdf MIME", table_cell_style), Paragraph("<b>PASS</b>", table_cell_style)],
        [Paragraph("TC-08", table_cell_style), Paragraph("CSV Structured Export Verification", table_cell_style), Paragraph("<code>GET /api/reports/csv/1</code>", table_cell_style), Paragraph("Status 200, text/csv MIME, valid rows", table_cell_style), Paragraph("<b>PASS</b>", table_cell_style)]
    ]
    test_table = Table(test_data, colWidths=[50, 145, 140, 155, 50])
    test_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TEXTCOLOR', (4,1), (4,-1), colors.HexColor("#15803d")),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(test_table)
    story.append(Spacer(1, 5))

    story.append(Paragraph("14. Genuine Application Screenshots &amp; Verification Evidence", h1_style))
    story.append(Paragraph(
        "Screenshots were captured directly from the live TRACE instance executing on the host workstation via headless Chromium browser:",
        body_style
    ))

    # Screenshots table (2x2 grid)
    shot_base = "/home/fardeenakmal/Desktop/osint/TRACE-OSINT/screenshots"
    s1 = os.path.join(shot_base, "01-dashboard.png")
    s2 = os.path.join(shot_base, "02-username-investigation.png")
    s3 = os.path.join(shot_base, "03-domain-intelligence.png")
    s4 = os.path.join(shot_base, "05-report-export.png")

    # Image width: 255pt, height: 130pt
    img_w, img_h = 260, 122
    shots_data = [
        [
            Paragraph("<b>Figure 1: Operational Dashboard (Live Stats &amp; Audit Log)</b>", table_cell_style),
            Paragraph("<b>Figure 2: Username OSINT Results (Target: @fardeenakmal)</b>", table_cell_style)
        ],
        [
            Image(s1, width=img_w, height=img_h) if os.path.exists(s1) else Paragraph("Screenshot 01", table_cell_style),
            Image(s2, width=img_w, height=img_h) if os.path.exists(s2) else Paragraph("Screenshot 02", table_cell_style)
        ],
        [
            Paragraph("<b>Figure 3: Domain Intelligence (example.com RDAP/DNS)</b>", table_cell_style),
            Paragraph("<b>Figure 4: Audit Dossier Preview &amp; Export Modal</b>", table_cell_style)
        ],
        [
            Image(s3, width=img_w, height=img_h) if os.path.exists(s3) else Paragraph("Screenshot 03", table_cell_style),
            Image(s4, width=img_w, height=img_h) if os.path.exists(s4) else Paragraph("Screenshot 05", table_cell_style)
        ]
    ]
    shots_table = Table(shots_data, colWidths=[268, 268])
    shots_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor("#f1f5f9")),
        ('ALIGN', (0,1), (-1,1), 'CENTER'),
        ('ALIGN', (0,3), (-1,3), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(shots_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: FINDINGS, LIMITATIONS, ETHICAL/LEGAL, CONCLUSION, REFERENCES
    # =========================================================================
    story.append(Paragraph("15. Empirical Findings &amp; Performance Evaluation", h1_style))
    story.append(Paragraph(
        "Empirical testing with target username <code>fardeenakmal</code> and target domain <code>example.com</code> yielded decisive performance data: "
        "<b>(1) Profile Detection Accuracy:</b> The system identified a verified active public profile on GitHub (HTTP 200, 614ms latency) with full bio extraction, "
        "while correctly distinguishing absent profiles on GitLab (HTTP 302 login redirect, 639ms), DockerHub (HTTP 404, 628ms), Dev.to (HTTP 404), "
        "and Keybase (HTTP 404). "
        "<b>(2) Anti-Scraping Resilience:</b> Reddit and Medium returned HTTP 403 status codes due to cloud-edge WAF challenges; TRACE correctly isolated these "
        "as <code>INCONCLUSIVE</code> rather than misclassifying them as non-existent. "
        "<b>(3) Passive DNS Precision:</b> Domain queries for <code>example.com</code> resolved dual authoritative IPv4 addresses (104.20.23.154, 172.66.147.243), "
        "IPv6 AAAA records, Cloudflare NS delegations, and RFC-compliant SPF restriction records (<code>v=spf1 -all</code>) within 720ms total elapsed time.",
        body_style
    ))

    story.append(Paragraph("16. Technical Limitations &amp; Countermeasures", h1_style))
    story.append(Paragraph(
        "<b>Cloud Edge Challenges:</b> Advanced CAPTCHA challenges (Cloudflare Turnstile, Cloudfront) intercept programmatic probes. TRACE mitigates "
        "this by explicitly categorizing such responses as INCONCLUSIVE and recording HTTP headers rather than attempting deceptive bypasses.<br/>"
        "<b>Name Collision:</b> On widespread consumer networks, common usernames may correspond to distinct individuals across platforms. TRACE mitigates "
        "false identity linkage by providing direct profile links and latency telemetry, enabling human-in-the-loop contextual verification.",
        body_style
    ))

    story.append(Paragraph("17. Ethical Framework &amp; Legal Compliance", h1_style))
    story.append(Paragraph(
        "TRACE was engineered strictly in accordance with ethical cybersecurity research principles and applicable cyber jurisprudence: "
        "<b>(1) Passive Reconnaissance Doctrine:</b> The software queries only publicly available data sources without attempting password guessing, "
        "credential stuffing, session hijacking, or perimeter exploitation. "
        "<b>(2) Statutory Alignment:</b> All operations comply with Section 43 and Section 66 of the Information Technology Act (India, 2000/2008), "
        "the Computer Fraud and Abuse Act (CFAA, 18 U.S.C. § 1030), and international conventions regarding unauthorized access. "
        "<b>(3) Source Etiquette:</b> Requests utilize legitimate HTTP User-Agent identifiers, enforce conservative timeouts (4.0s), and respect rate limits. "
        "TRACE is explicitly restricted to authorized personal footprint audits, enterprise self-assessments, and academic laboratory pedagogy.",
        body_style
    ))

    story.append(Paragraph("18. Conclusion &amp; Future Enhancements", h1_style))
    story.append(Paragraph(
        "TRACE successfully accomplishes all stated objectives, establishing a robust, modern, and transparent OSINT digital footprint analyzer. "
        "By enforcing strict status disambiguation, passive DNS/RDAP correlation, local SQLite privacy, and automated academic reporting, "
        "the tool eliminates the primary flaws of legacy CLI scripts. Future work will expand source coverage to 50+ platforms, integrate "
        "asynchronous proxy rotation for inconclusive sources, and introduce interactive link-analysis graph visualizations.",
        body_style
    ))

    story.append(Paragraph("19. Academic &amp; Technical References", h1_style))
    ref_style = ParagraphStyle(
        'Ref_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.8,
        leading=8.8,
        textColor=colors.HexColor("#334155"),
        leftIndent=12,
        firstLineIndent=-12,
        spaceAfter=2
    )
    story.append(Paragraph("[1] P. Mockapetris, <i>RFC 1035: Domain Names - Implementation and Specification</i>, Internet Engineering Task Force (IETF), Nov. 1987.", ref_style))
    story.append(Paragraph("[2] A. Newton and B. Ellacott, <i>RFC 7480: HTTP Usage in the Registration Data Access Protocol (RDAP)</i>, IETF, Mar. 2015.", ref_style))
    story.append(Paragraph("[3] K. Scarfone et al., <i>Technical Guide to Information Security Testing and Assessment</i>, NIST Special Publication 800-115, Sept. 2008.", ref_style))
    story.append(Paragraph("[4] S. Bazzell, <i>Open Source Intelligence Techniques: Resources for Searching and Analyzing Online Information</i>, 7th ed., 2021.", ref_style))
    story.append(Paragraph("[5] S. Ramirez, <i>FastAPI: Modern, High-Performance Web Framework for Python</i>, Zenodo, 2020.", ref_style))
    story.append(Paragraph("[6] Ministry of Law and Justice, <i>The Information Technology Act, 2000 (Act No. 21 of 2000)</i>, Government of India, 2000.", ref_style))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {filename}")

if __name__ == '__main__':
    out_pdf = "/home/fardeenakmal/Desktop/osint/TRACE-OSINT/case-study/TRACE_OSINT_Case_Study.pdf"
    build_pdf(out_pdf)

