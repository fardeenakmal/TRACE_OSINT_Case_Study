# TRACE — OSINT Digital Footprint Analyzer

> **Academic Cybersecurity Mini Project & 5-Page Case Study**  
> **Student:** Fardeen Akmal (Roll No: 2)  
> **Project Guide:** Akanksha Thakare  
> **Department:** Computer Science and Engineering (IoT, Cyber Security and Blockchain Technology)  
> **Institute:** G.V. Acharya Institute of Engineering and Technology, Shelu  
> **Affiliation:** University of Mumbai • Academic Year 2026–2027  

---

## 1. Project Overview

**TRACE (Target Reconnaissance & Auditable Collection Engine)** is a modular, high-performance, full-stack Open Source Intelligence (OSINT) analytical web application. It enables security researchers, incident responders, and students to audit surface-web digital footprints without resorting to intrusive network exploitation or brittle web-scraping heuristics.

TRACE eliminates the hallmark failure modes of legacy command-line scrapers:
- **Zero False-Positive Hallucination:** Rigorously distinguishes verified profiles (`FOUND`) from client-side SPA routing redirects, generic soft-404s, or login gateways (`NOT_FOUND`).
- **Defensive Error Handling:** Accurately isolates Cloudflare Turnstile, AWS WAF challenges, and HTTP 429 rate limits as `INCONCLUSIVE`, refusing to speculate or fabricate negative findings.
- **Passive DNS & RDAP Intelligence:** Resolves authoritative DNS zones (`A`, `AAAA`, `MX`, `NS`, `TXT`, `SOA`), ICANN RDAP registration registries, and GeoIP autonomous system telemetry purely through passive name resolution.
- **Defensible Local Auditability:** Persists all investigations in a local SQLite database and generates formal, publication-ready PDF and CSV reports stamped with academic attribution and integrity checksums.

---

## 2. Technology Stack

| Layer | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| **Backend API** | Python / FastAPI | 3.14+ / 0.115+ | High-throughput asynchronous REST gateway and Pydantic validation |
| **Concurrency** | HTTPX Async Client | 0.28+ | Non-blocking connection pooling, HTTP/2, and strict per-request timeouts |
| **DNS Engine** | dnspython | 2.7+ | Direct wire-format DNS socket queries to authoritative nameservers |
| **Frontend UI** | React / TypeScript / Vite | 18.3+ / 5.4+ | Type-safe single-page reactive dashboard with cybersecurity theme |
| **Icons & Style** | Lucide React / CSS Grid | Latest | Modern dark-mode SOC dashboard with responsive telemetry cards |
| **Persistence** | SQLite 3 | 3.x | ACID-compliant, zero-credential relational database with WAL mode |
| **Reporting** | ReportLab Flowables | 4.3+ | Programmatic generation of formal academic PDF dossiers and CSV exports |
| **Automated Tests** | pytest / pytest-asyncio | 8.3+ | Comprehensive test suite verifying 100% of endpoints and error states |

---

## 3. Supported Features

### 3.1 Operations Dashboard
- Live investigation metric counters: Total inquiries, username footprint scans, and domain intelligence runs.
- Visual status breakdown: Supported source platform registry and live daemon health telemetry.
- Recent activity timeline featuring one-click inspection links.

### 3.2 Username OSINT Scanner
- Asynchronous concurrent queries across 10 high-value developer, identity, and social platforms:
  - **GitHub** (Developer / Code)
  - **GitLab** (Developer / DevOps)
  - **DockerHub** (Containers / Tech)
  - **Dev.to** (Developer Community)
  - **HackerNews** (Tech Forum)
  - **Reddit** (Social / Discussions)
  - **Gravatar** (Avatar / Identity)
  - **Keybase** (Cryptography / Identity)
  - **Medium** (Blogging / Publishing)
  - **Pinterest** (Media / Visual)
- Filterable result views: `ALL`, `FOUND`, `INCONCLUSIVE`, `NOT_FOUND`.
- Per-source latency metrics (ms) and public profile hyperlink navigation.

### 3.3 Domain Intelligence
- Authoritative DNS resolution across record types: `A` (IPv4), `AAAA` (IPv6), `MX` (Mail routing), `NS` (Delegated nameservers), `TXT` (SPF / domain verification), `SOA` (Start of Authority).
- ICANN RDAP parsing: Registrant organization, registrar name, domain creation, update, and expiration dates.
- IP Geolocation & ASN telemetry: Resolving ISP, Autonomous System Number, hosting country, and city.
- Passive Reconnaissance Guarantee: Zero TCP port scanning or active web application fuzzing.

### 3.4 Local Investigation History & Report Export
- Auditable SQLite database logging every query target, execution timestamp, and aggregate findings.
- Interactive **Report Dossier Modal** providing instant browser preview of audit packages.
- Publication-ready **PDF Report Export** styled with university headers, student credentials, and verification tables.
- Tabular **CSV Export** for external SIEM, spreadsheet, or pipeline ingestion.
- Granular record deletion and complete database clearing controls.

### 3.5 Robust Error Diagnostics & Input Validation Gateways
- Strict RFC 1035 / RFC 1123 domain syntax validation preventing command injection and SSRF.
- Input validation gates rejecting malformed, empty, or dangerous target queries before socket allocation.
- Explicit visual badges differentiating `FOUND`, `NOT_FOUND`, `INCONCLUSIVE` (rate-limited / bot-blocked), and `CHECK_FAILED` (socket timeout / transport error).

---

## 4. Directory Structure

```text
TRACE-OSINT/
├── backend/
│   ├── main.py                     # FastAPI application entry point, routes, static mount
│   ├── database.py                 # SQLite database schema, CRUD, and telemetry functions
│   ├── services/
│   │   ├── username_osint.py       # Asynchronous 10-platform username scanner
│   │   ├── domain_osint.py         # Passive DNS, RDAP, and IP geolocation engine
│   │   └── reporting.py            # Academic PDF & CSV report export synthesizer
│   ├── tests/
│   │   └── test_api.py             # 8 pytest unit and integration test cases
│   └── static/                     # Compiled React single-page application bundle
├── frontend/
│   ├── src/
│   │   ├── App.tsx                 # Main React component, state, and modal views
│   │   ├── main.tsx                # React DOM bootstrap
│   │   ├── index.css               # Modern cybersecurity dark theme styling
│   │   └── types.ts                # TypeScript interface definitions
│   ├── package.json                # Frontend package configuration
│   └── vite.config.ts              # Vite compilation and proxy configuration
├── screenshots/                    # Genuine application screenshots captured on PC
│   ├── 01-dashboard.png            # Live operations dashboard
│   ├── 02-username-investigation.png # Live username OSINT findings (@fardeenakmal)
│   ├── 03-domain-intelligence.png  # Passive DNS & RDAP results (example.com)
│   ├── 04-investigation-history.png# Completed investigation audit history
│   ├── 05-report-export.png        # Report preview modal & export confirmation
│   └── 06-error-handling.png       # RFC validation error handling view
├── reports/                        # Exported PDF and CSV dossiers
│   ├── TRACE_Report_domain_example.com_2.pdf
│   ├── TRACE_Report_domain_example.com_2.csv
│   ├── TRACE_Report_username_fardeenakmal_7.pdf
│   └── TRACE_Report_username_fardeenakmal_7.csv
├── case-study/                     # Formatted 5-page academic case study deliverables
│   ├── TRACE_OSINT_Case_Study.docx # Exactly 5 pages in Microsoft Word format
│   └── TRACE_OSINT_Case_Study.pdf  # Exactly 5 pages in PDF format
├── generate_pdf_study.py           # Programmatic ReportLab case study generator
├── generate_docx_study.py          # Programmatic python-docx case study generator
├── .env.example                    # Environment variable configuration template
└── README.md                       # Comprehensive system documentation (this file)
```

---

## 5. Installation and Setup Instructions

### 5.1 Prerequisites
- **Operating System:** Linux (Fedora, Ubuntu, Debian, Arch), macOS, or Windows (WSL2 recommended).
- **Python:** Python 3.10 or higher.
- **Node.js:** Node.js v18 or higher with `npm`.

### 5.2 Step 1 — Clone / Navigate to Project Directory
```bash
cd TRACE-OSINT
```

### 5.3 Step 2 — Configure Environment
```bash
cp .env.example .env
```

### 5.4 Step 3 — Install Backend Dependencies
```bash
cd backend
python3 -m pip install fastapi uvicorn httpx dnspython reportlab python-docx pytest
```

### 5.5 Step 4 — Build Frontend Assets
```bash
cd ../frontend
npm install
npm run build
```
*(This automatically builds the production bundle into `backend/static/`)*

### 5.6 Step 5 — Start the TRACE Server
```bash
cd ../backend
python3 -m uvicorn main:app --host 127.0.0.1 --port 8000
```
Open your browser and navigate to:  
👉 **`http://127.0.0.1:8000`**

---

## 6. Automated Testing Suite

TRACE includes a rigorous automated test suite executing across all core endpoints, input validation gates, and export modules:

```bash
cd backend
python3 -m pytest tests/test_api.py -v
```

### Verified Test Matrix (100% Pass Rate):
- `test_health_check`: Validates API availability and engine identifier.
- `test_dashboard_stats`: Validates metrics counters and recent activity array.
- `test_username_investigation`: Validates async dispatch and 10-source categorization.
- `test_username_validation_error`: Validates HTTP 422 rejection of blank usernames.
- `test_domain_investigation`: Validates DNS record parsing and RDAP registration.
- `test_history_crud`: Validates SQLite insertion, retrieval, and single record deletion.
- `test_pdf_report_generation`: Validates ReportLab PDF stream and binary validity.
- `test_csv_report_generation`: Validates CSV tabular export and MIME headers.

---

## 7. REST API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Returns service health status and timestamp. |
| `GET` | `/api/stats` | Returns aggregate metrics and the 5 most recent activities. |
| `POST` | `/api/investigate/username` | Accepts `{"username": "target"}`, returns 10 platform findings. |
| `POST` | `/api/investigate/domain` | Accepts `{"domain": "target.com"}`, returns DNS/RDAP/GeoIP data. |
| `GET` | `/api/history?limit=50` | Returns historical investigation records from local SQLite. |
| `GET` | `/api/history/{id}` | Returns single investigation detail and complete telemetry. |
| `DELETE` | `/api/history/{id}` | Deletes a specific investigation record from local SQLite. |
| `DELETE` | `/api/history` | Truncates all investigation records from local SQLite. |
| `GET` | `/api/reports/pdf/{id}` | Generates and downloads the official academic PDF dossier. |
| `GET` | `/api/reports/csv/{id}` | Generates and downloads the tabular CSV export. |

---

## 8. Five-Page Academic Case Study Deliverables

The project deliverables include an academic case study document formatted to be **strictly 5 pages**:
- **Microsoft Word Document:** `case-study/TRACE_OSINT_Case_Study.docx`
- **PDF Document:** `case-study/TRACE_OSINT_Case_Study.pdf`

### Document Structure:
- **Page 1 — Introduction:** Title, Academic Metadata, Abstract, Introduction, Problem Statement, Objectives and Scope.
- **Page 2 — Proposed System:** Background & Literature Review, Tool Comparison Matrix, Functional & Non-Functional Requirements, Technology Stack Table, Operational Use Cases.
- **Page 3 — Architecture & Workflow:** Modular Architecture Topology, Data Flow Pipeline, SQLite Database Schema, Multi-Tier Result Verification Decision Tree, Security & Ethical Controls.
- **Page 4 — Implementation & Testing:** Engineering Methodology, Automated Pytest Verification Matrix, Genuine Application Screenshots Grid (Figures 1–4).
- **Page 5 — Results & Conclusion:** Empirical Findings & Telemetry, Technical Limitations & Countermeasures, Ethical & Legal Compliance Framework, Conclusion & Future Enhancements, Academic References.

---

## 9. Ethical and Legal Compliance Framework

TRACE was engineered strictly as an educational and defensive cybersecurity auditing tool. Its operational philosophy adheres to the following principles:

1. **Passive Reconnaissance Doctrine:** TRACE only queries publicly available endpoints and public authoritative DNS servers. It performs no intrusive port scanning, web application fuzzing, or vulnerability exploitation.
2. **Statutory Alignment:** All operations comply with Section 43 and Section 66 of the Information Technology Act (India, 2000/2008), the Computer Fraud and Abuse Act (CFAA, 18 U.S.C. § 1030), and international conventions regarding unauthorized system access.
3. **No Credential Access or Exploitation:** TRACE contains no functionality to brute-force credentials, scrape private communications, or bypass authentication barriers.
4. **Target Authorization:** Users are legally and ethically obligated to scan only usernames and domains that they own, or for which they possess explicit written authorization.

---

## 10. Technical Limitations

- **Cloud-Edge WAF Challenges:** Platforms protected by Cloudflare Turnstile, Cloudfront, or aggressive anti-bot protections (e.g., Reddit, Medium) may return HTTP 403. TRACE transparently labels these as `INCONCLUSIVE` rather than guessing.
- **Username Collision:** A single username on multiple services may belong to distinct individuals. TRACE provides direct profile URLs and response latency to facilitate human-in-the-loop contextual verification.
- **Rate Limiting:** Consecutive high-frequency queries to the same platform may trigger temporary IP throttling. Users should introduce conservative delays when conducting extensive batch audits.

---

## 11. Academic Attribution

- **Student:** Fardeen Akmal (Roll No: 2)  
- **Project Guide:** Akanksha Thakare  
- **Department:** Computer Science and Engineering (IoT, Cyber Security and Blockchain Technology)  
- **College:** G.V. Acharya Institute of Engineering and Technology, Shelu  
- **Affiliation:** University of Mumbai  
- **Academic Year:** 2026–2027  

