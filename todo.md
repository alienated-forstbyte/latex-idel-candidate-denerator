# Project Roadmap & Feature Backlog: Job-to-Ideal-Resume

This document tracks all planned features, technical requirements, and architectural milestones for the Job-to-Ideal-Resume application.

---

## 📌 Feature Backlog

### Feature 1: Resume Personalization & Tailoring (Resume Fusion)
* **Status:** In Backlog / Ready for Planning
* **Objective:** Take an actual candidate's real resume and tailor it to match a target Job Description and specific ATS engine rules, rather than generating a purely synthetic benchmark profile.
* **Core Capabilities:**
  * **Dual-Input Interface:** Support providing both the **Target Job Description** and the **User's Current Resume** (via text area or file upload).
  * **Generation Mode Selection:** Allow toggling between:
    * `Tailor My Resume to JD` (merges user background with target JD requirements).
    * `Generate Benchmark Candidate` (synthesizes the 10/10 ideal profile).
  * **Truth Anchoring Guardrails:**
    * Strictly preserve genuine user identity: Candidate Name, Contact Information, Real Company Names, Employment Dates, and Education/Degrees.
    * Prevent hallucinations of non-existent employers, credentials, or degree programs.
  * **ATS Alignment & Bullet Enhancement:**
    * Cross-map the candidate's existing experience against the target JD competencies.
    * Reframe real work achievements using the Google XYZ formula (`Accomplished [X], measured by [Y], by doing [Z]`).
    * Infuse exact JD keywords, tools, and technical terms directly into relevant roles.
  * **ATS Layout & Engine Compliance:**
    * Adhere to Workday or Generic ATS requirements (single-column, non-hyphenated terms, dual acronym/full-phrase format, suppressed page numbers).
    * Compile cleanly into compilable LaTeX and downloadable single-page PDF via `latexmk`.

---

### Feature 2: Structured User Profile Input Form
* **Status:** In Backlog
* **Objective:** Provide a guided, multi-section interactive form (`st.form`) allowing users to enter and save their career profile once, without needing to format or upload a raw resume text file every time.
* **Core Capabilities:**
  * **Sectioned Form Fields:**
    * Personal Contact Details (Name, Email, Phone, Location, Portfolio/LinkedIn/GitHub).
    * Work Experience (Company, Title, Start/End Dates, Core Responsibilities/Wins).
    * Education (Degree, Major, Institution, Graduation Date, GPA/Honors optional).
    * Skills & Certifications (Categorized by languages, cloud, tools, and credentials).
    * Key Projects (Title, Tech Stack, Description, Impact).
  * **Profile Persistence:** Save the profile locally (JSON / SQLite) so it automatically preloads on future sessions.
  * **Quick Import/Export:** Option to export/import profile as JSON.

---

### Feature 3: Multi-ATS Specialized Prompt Library
* **Status:** In Backlog
* **Objective:** Expand the prompt engine beyond Workday and Generic ATS to enforce system-specific rules for all major recruiting platforms.
* **Core Capabilities:**
  * **Greenhouse:** Optimized for modern typography, dense keyword tagging, clean section demarcations, and high title similarity weighting.
  * **Lever:** Optimized for linear text extraction, portfolio/GitHub link preservation, and strong skill-to-experience proximity matching.
  * **iCIMS & Oracle Taleo:** Legacy enterprise rules (zero tables/columns, strict standard headers, chronological work blocks, precise keyword density without stuffing).
  * **SmartRecruiters & BambooHR:** Formatted for web-native parsers with structured project breakdowns and categorized skill hierarchies.
  * **Dynamic Rule Injection:** Automatically injects the correct formatting constraints and prompt clauses based on the user's dropdown selection in `app.py`.

---

### Feature 4: Daily Career Diary & Work Journal
* **Status:** Completed
* **Objective:** Allow users to log daily tasks, wins, solved tickets, and metrics as they happen, enabling the AI to periodically synthesize everyday work into fresh, high-impact resume bullets.
* **Core Capabilities:**
  * **Daily Journal Interface:** A lightweight Streamlit view where users record daily work notes, deployed features, tools used, and quantifiable results.
  * **AI Bullet Synthesizer:** An aggregation engine that analyzes a date range of journal entries and synthesizes them into Google XYZ achievement bullets using Gemini.
  * **Persistent Career Vault:** Local JSON persistence (`diary_entries.json`) storing all historical logs.
  * **One-Click Sync:** Automatically update the candidate's active profile and resume experience section with newly synthesized bullet points.
* **Backlog Enhancements for Career Diary:**
  * **Structured Entries & Metadata:** Date picker (`st.date_input`) and category tagging (Feature, Bug Fix, Architecture, Optimization).
  * **Two-Step Preview Workflow:** Synthesize bullets -> Preview & edit -> Confirm Sync to profile.
  * **Date-Range Filtering:** Filter entries across specific timeframes for targeted resume versions.

---

### Feature 5: Gmail Integration & Application Status Tracker
* **Status:** Active
* **Objective:** Automatically detect and track job applications, recruiter communications, and interview/rejection outcomes directly from the user's Gmail inbox.
* **Core Capabilities:**
  * **OAuth 2.0 Gmail Connection:** Secure, read-only connector to scan job-related emails (using patterns from `enterprise-workspace-agent`).
  * **AI Email Classifier:** Parses emails from companies, LinkedIn, Workday, Greenhouse, etc., and categorizes them into:
    * `Applied / Acknowledged`
    * `Interview Invitation / Scheduling`
    * `Assessment / Take-Home Test`
    * `Offer Received`
    * `Rejection Letter`
  * **Application Kanban / Tracker Dashboard:** Streamlit table/board showing Company Name, Job Title, Date Applied, Current Status, and Last Received Email Snippet.

---

### Feature 6: Docker Containerization & Cloud Deployment
* **Status:** In Backlog / Pending Containerization
* **Objective:** Containerize the entire application into a reproducible, production-grade Docker image with all system binaries (Python, Streamlit, TeX Live / `latexmk`).
* **Core Capabilities:**
  * **Optimized `Dockerfile`:**
    * Base Linux image with Python 3.11/3.12 slim.
    * Headless TeX Live distribution (`texlive-latex-base`, `texlive-latex-extra`, `latexmk`) pre-installed.
    * Cached dependency installation via `requirements.txt`.
  * **`docker-compose.yml`:**
    * Single-command local startup (`docker-compose up`) exposing port 8501.
    * Environment file forwarding (`.env` for `GCP_API_KEY`, `GMAIL_USER`, etc.).
    * Persistent volume mounts for data vaults (`user_profile.json`, `job_application_status.json`, `diary_entries.json`).
  * **`.dockerignore` Optimization:**
    * Exclude `.venv`, `__pycache__`, `.git`, local `.env`, and auxiliary LaTeX build artifacts (`*.aux`, `*.fls`, `*.log`, `*.fdb_latexmk`).
  * **Health Check & Cloud Run Readiness:**
    * Native container health check (`curl -f http://localhost:8501/_stcore/health`).
    * Configured for scale-to-zero serverless deployment on Google Cloud Run.

---

### Feature 7: External Platform & Ecosystem Integrations (ChatGPT, Cursor, LinkedIn, Naukri)
* **Status:** In Backlog
* **Objective:** Connect and syndicate the candidate's verified profile across major AI tools and professional hiring ecosystems.
* **Core Capabilities:**
  * **ChatGPT Integration:**
    * **System Persona & Context Export:** One-click generation of structured prompts / Custom GPT instructions containing the user's career profile and target JD.
    * **Interview Prep Assistant:** Generates JD-specific behavioral interview questions (STAR method) and technical architecture questions tailored to the candidate's exact background.
  * **Cursor AI Integration:**
    * **`.cursorrules` Generator:** Automatically outputs a customized `.cursorrules` or `.cursor/rules/` configuration reflecting the engineer's exact tech stack, coding standards, and architectural style for AI pair programming.
    * **Project Context Injection:** Exports technical competencies formatted for immediate use in Cursor coding sessions.
  * **LinkedIn Integration:**
    * **Profile Section Optimization:** Converts user profile data into optimized LinkedIn fields:
      * High-ranking, keyword-dense LinkedIn Headline.
      * Compelling "About / Summary" section highlighting key technical wins.
      * Experience bullet points formatted with clean Unicode bullets for web rendering.
    * **Recruiter Outreach Generator:** Drafts personalized connection notes and InMail messages tailored to specific hiring managers and job postings.
  * **Naukri Integration:**
    * **Resdex Search Algorithm Tuning:** Formats candidate profile for optimal ranking on Naukri.com's recruiter search engine:
      * High-converting Resume Headline (optimized for 180-character limits with priority keywords).
      * Tagged Key Skills block matching top recruiter search filters.
      * Notice period and location alignment for Indian tech market hiring.

---

### Feature 8: Existing Resume Parser & Profile Auto-Fill
* **Status:** In Backlog
* **Objective:** Allow users to upload an existing resume (PDF, DOCX, LaTeX, or plain text) to automatically extract and populate all fields in the User Profile form.
* **Core Capabilities:**
  * **Multi-Format Ingestion:** Support uploading existing resume files (`.pdf`, `.tex`, `.docx`, `.txt`) or pasting raw resume text directly.
  * **Structured LLM Extraction:** Use Gemini with structured JSON schema output to parse and isolate:
    * Contact info (`name`, `email`, `phone`, `linkedin`, `github`)
    * Professional Summary
    * Technical Skills (categorized / comma-separated)
    * Work Experience (roles, company names, dates, achievements)
    * Education (degree, university, graduation year)
  * **One-Click Form Auto-Fill:** Automatically populate `user_profile.json` and sync `st.session_state` so the user doesn't have to manually type their history.
  * **Conflict & Merge Resolution:** Preview extracted fields with an option to selectively overwrite or append to existing profile data.

---

### Feature 9: Jira Ticket Tracking & Automated Diary / Skill Sync
* **Status:** In Backlog
* **Objective:** Connect to Jira (via Atlassian REST API / Personal Access Token) to automatically scan resolved and in-progress tickets, transform day-to-day engineering deliverables into Daily Career Diary entries, and dynamically update the candidate's Technical Skills inventory.
* **Core Capabilities:**
  * **Jira REST API Connector:** Secure, token-based connection querying user's resolved issues (e.g., `status = Done AND assignee = currentUser() ORDER BY updated DESC`).
  * **Automated Work Diary Logging:** Uses Gemini to synthesize ticket summaries, technical descriptions, and PR discussions into clean, dated entries for the Daily Career Diary (`diary_entries.json`).
  * **Skill & Tech Stack Discovery:** Detects new tools, libraries, frameworks, cloud services, and languages referenced in ticket metadata or commit messages, comparing them against `user_profile.json` to highlight or auto-add newly demonstrated competencies.
  * **Impact & Velocity Metric Synthesizer:** Extracts story points, resolved bug severities, system latency reductions, or delivery milestones directly into Google XYZ achievement bullets.

---

### Feature 10: Centralized Logging, Diagnostics & Error Observability
* **Status:** In Backlog
* **Objective:** Implement comprehensive structured file and console logging across all modules to capture background execution states, Gemini API latency/failures, LaTeX compilation errors, and Streamlit session events for rapid troubleshooting.
* **Core Capabilities:**
  * **Centralized Logging Engine:** Configure standard Python `logging` with a unified format (`%(asctime)s | %(levelname)s | %(name)s:%(lineno)d | %(message)s`), rotating log file handler (`app.log`), and console streaming.
  * **End-to-End Pipeline Tracing:**
    * **LLM Pipeline:** Log prompt inputs, model names, latency, token consumption, and API retry events.
    * **Compiler Subsystem:** Log full `latexmk` / `pdflatex` stdout and stderr, return codes, and missing TeX package alerts.
    * **State & Persistence:** Trace all profile and diary reads/writes, schema validation warnings, and file mutation timestamps.
    * **Job Tracker:** Log raw email ingestion, parsed JSON payloads, and application status transitions.
  * **Silent Failure Prevention:** Eliminate bare `except: pass` and silent console printouts across `deconstruct_jd.py` and `job_tracker.py` by capturing full stack traces via `logger.exception()`.
  * **In-App Diagnostics Log Viewer:** Provide an expander or developer panel in Streamlit allowing the user to view and download live `app.log` contents directly from the UI without terminal access.

---

### Feature 11: Truth & Fact-Check Auditor Module ("Anti-Lie" / Hallucination Detector)
* **Status:** In Backlog
* **Objective:** Automatically cross-examine generated resumes against the candidate's verified profile (`user_profile.json`) and career diary (`diary_entries.json`) to detect and flag any fabricated metrics, unverified tools, or exaggerated claims before submission.
* **Core Capabilities:**
  * **Ground Truth Verification Engine:** Analyzes every generated resume bullet point against the candidate's actual history using strict semantic fact-checking prompts.
  * **Hallucination & "Lie" Scoring:** Identifies unanchored technologies, unverified company names, or fabricated numerical claims (e.g., claiming to manage \$10M budgets or leading teams when profile indicates individual contributor).
  * **Confidence & Discrepancy Highlighting:** Displays a side-by-side audit report with green badges for truth-anchored claims, yellow warnings for extrapolations, and red flags for ungrounded claims.
  * **Automated Rewriter / Grounding Correction:** One-click re-prompting to replace flagged bullets with verified accomplishments from the user's career diary.
  * **Decoupled Architecture Layer:** Modularize verification into an independent validation service layer between generation and PDF compilation.

---

### Feature 12: Streamlit UI / UX Modernization & Live PDF Preview
* **Status:** In Backlog
* **Objective:** Upgrade the Streamlit user interface with modern visual styling, inline live PDF viewing, drag-and-drop Kanban application tracking, and streamlined workflow navigation.
* **Core Capabilities:**
  * **Live Inline PDF Viewer:** Embed a real-time PDF preview (via PDF.js or base64 iframe viewer) directly inside the Streamlit output column, eliminating the need to download the PDF to inspect layout.
  * **Drag-and-Drop Kanban Board:** Upgrade the Job Tracker tab into an interactive visual board where applications can be dragged or clicked across stages (`Applied` ➔ `Assessment` ➔ `Interviewing` ➔ `Offer` ➔ `Rejected`).
  * **Modern Theming & Custom CSS:** Clean typography, glassmorphism card containers, responsive column layouts, and distinct status badges for ATS compatibility scores.
  * **Step-by-Step Guided Wizard:** Interactive onboarding flow guiding users through Profile setup ➔ Diary logging ➔ Resume customization.

---

### Feature 13: Dynamic & Configurable Resume File Naming
* **Status:** Completed
* **Objective:** Replace static download filenames (`new_id_resume.pdf`) with dynamic, ATS-optimized, and customizable file naming conventions.
* **Core Capabilities:**
  * **Template Pattern Tokens:** Support customizable naming patterns such as:
    * `{Candidate_Name}_{Job_Title}_{Company}_{ATS}_Resume.pdf` (e.g., `John_Doe_MLOps_Engineer_Google_Workday_Resume.pdf`)
    * `{FirstName}_{LastName}_{Year}_CV.pdf`
  * **Smart Character Sanitization:** Automatically replaces illegal OS characters, strips accents and extra whitespace, and enforces recruiter-preferred casing (snake_case or CamelCase).
  * **In-UI Name Override:** Allow the user to preview and directly edit the suggested filename on the download card before saving.

---

### Feature 14: Intelligent Email Triage & Noise Filtering Engine (Alerts vs. Real Applications)
* **Status:** In Backlog
* **Objective:** Prevent automated job recommendation alerts (e.g. LinkedIn Job Alerts, Indeed Daily Picks, Glassdoor) and promotional recruiting newsletters from polluting the Job Tracker with dummy/irrelevant applications.
* **Core Capabilities:**
  * **Two-Tier Architecture (Triage Gatekeeper vs. Deep Parsing):**
    * **Tier 1 (Triage Gatekeeper):** Fast, low-latency classifier categorizing each incoming email into:
      * `ACTIVE_APPLICATION`: Genuine status update for a role the user actually applied to (Application Received, Interview Invitation, Online Assessment, Offer, Rejection).
      * `JOB_RECOMMENDATION_ALERT`: Automated digest of open positions ("10 new jobs for you", "Top job picks", "Job Alert").
      * `PROMOTIONAL_MARKETING`: Newsletters, recruiter cold outreach, talent network invites, webinars.
      * `IRRELEVANT_OTHER`: Generic personal or system emails.
    * **Tier 2 (Deep Extraction):** Only emails classified as `ACTIVE_APPLICATION` proceed to `job_tracker.job_classifier()` to extract company name, job title, and application stage.
  * **Zero-Cost Heuristic Pre-Filtering:**
    * Regex and sender pattern matching on known automated alert senders (`jobalerts-noreply@linkedin.com`, `alert@indeed.com`, `messages-noreply@linkedin.com`, `talent@...`).
    * Subject line keyword filtering (`"new jobs matching"`, `"job alert"`, `"recommended jobs"`, `"weekly job digest"`).
    * Bypasses Gemini API calls entirely for obvious automated digests to conserve rate limits and prevent 503/429 errors.
  * **Lightweight Structured LLM Filter:**
    * For ambiguous emails that pass heuristics, prompt Gemini with a compact binary/multi-class schema (`{"is_active_application": bool, "category": str, "confidence": float}`).
  * **Transparency & Triage Audit UI:**
    * Streamlit metrics displaying total emails scanned vs. noise discarded vs. applications tracked.
    * Collapsible expander ("View Filtered Noise") allowing users to inspect discarded emails so no authentic opportunity is silently dropped.

---

## 🐛 Known Issues & Quality Enhancements

### Issue 1: Workday Mode Generates Identical/Repetitive Resumes Across Different JDs [RESOLVED]
* **Reported:** User observed that selecting **Workday** for different JDs consistently produces virtually identical resumes.
* **Root Causes Identified:**
  1. **Static Placeholder Companies:** `build_workday_prompt` lacked guidance on company naming or project domains.
  2. **Verbatim JD Copying:** `build_workday_prompt` lacked Google XYZ formula integration.
  3. **Silent Failure & Stale File Masking:** `deconstruct_jd.pipeline()` swallowed exceptions without raising, allowing `app.py` to re-serve old PDFs.
* **Resolution Completed:**
  * Added `purge_generation_artifacts()` and `st.session_state` reset in `app.py`.
  * Added strict negative prompt constraints forbidding placeholder companies (`Tech Solutions Inc.`, `Cloud Systems Corp`, `Acme Corp`).
  * Propagated errors in `deconstruct_jd.pipeline()` with model failover and explicit `RuntimeError` checks in `app.py`.

---

## 🚦 Agreed Execution Order & Phasing

Updated priority order per user direction:

```
Phase 1: Docker Containerization (Feature 6) [COMPLETED]
  └── Multi-stage Dockerfile + Linux TeX Live environment + local & cloud deployment
Phase 2: User Profile Form (Feature 2) [COMPLETED]
  └── Multi-section structured input form + local JSON/SQLite persistence
Phase 3: Resume Personalization & Tailoring (Feature 1) [COMPLETED]
  └── Fusion engine + truth anchoring + Google XYZ bullet rewriting
Phase 4: Multi-ATS Rules Library (Feature 3) [COMPLETED]
  └── Specialized prompt rules for Greenhouse, Lever, iCIMS, Taleo
Phase 5: Daily Career Diary (Feature 4) [COMPLETED]
  └── Work journal + continuous bullet synthesizer
Phase 6: Job Search OS (Feature 5) [ACTIVE]
  └── Gmail OAuth integration + Automated application tracking dashboard
Phase 7: Ecosystem Integrations (Feature 7)
  └── Export & sync with ChatGPT, Cursor (.cursorrules), LinkedIn, and Naukri
```

| Phase | Milestone | Rationale & Value |
| :--- | :--- | :--- |
| **Phase 1 (Completed)** | **Docker Containerization** | Solves the dual Python + TeX Live environment dependency once and for all, making the app 100% portable. |
| **Phase 2 (Completed)** | **User Profile Form** | Establishes the structured data model and UI for user profile inputs and persistence. |
| **Phase 3 (Completed)** | **Resume Personalization** | Fuses real candidate profile data with target JDs using truth anchoring and XYZ formulas. |
| **Phase 4 (Completed)** | **Multi-ATS Rules Library** | Extends Workday rules to Greenhouse, Lever, Taleo, and iCIMS. |
| **Phase 5 (Completed)** | **Daily Career Diary** | Adds day-to-day work journaling and automatic resume bullet updates. |
| **Phase 6 (Active)** | **Gmail Job Tracker** | End-to-end tracking of job applications, rejection letters, and interview invites. |
| **Phase 7** | **Ecosystem Integrations** | Syndicates verified candidate data to ChatGPT, Cursor AI, LinkedIn, and Naukri. |
| **Backlog** | **Resume Parser & Auto-Fill** | Parses existing PDF/DOCX/LaTeX resumes to pre-fill the User Profile form automatically. |
| **Backlog** | **Jira Ticket Integration** | Ingests Jira tickets to auto-log career diary entries and extract new technical skills. |
| **Backlog** | **Centralized Logging** | Structured file/console logging (`app.log`) and in-app diagnostics for end-to-end tracing. |
| **Backlog** | **Truth / Anti-Lie Auditor** | Cross-verifies resume bullets against profile/diary to flag fabricated claims & hallucinations. |
| **Backlog** | **UI / UX Modernization** | Live inline PDF viewer, drag-and-drop Kanban tracker, and modern responsive CSS theming. |
| **Completed** | **Dynamic Resume Naming** | Configurable token-based filenames (e.g. `{Name}_{Role}_{Company}_Resume.pdf`) and sanitization. |
| **Backlog** | **Email Triage & Noise Filter** | Two-tier heuristic + LLM filter discarding job alert digests and promotional emails. |
