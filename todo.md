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
* **Status:** In Backlog
* **Objective:** Allow users to log daily tasks, wins, solved tickets, and metrics as they happen, enabling the AI to periodically synthesize everyday work into fresh, high-impact resume bullets.
* **Core Capabilities:**
  * **Daily Journal Interface:** A lightweight Streamlit view where users record daily work notes, deployed features, tools used, and quantifiable results.
  * **AI Bullet Synthesizer:** An aggregation engine that analyzes a date range of journal entries and synthesizes them into Google XYZ achievement bullets.
  * **Persistent Career Vault:** Local database (SQLite) storing all historical logs, tagged by project, tool, and date.
  * **One-Click Sync:** Automatically update the candidate's active profile and resume experience section with newly synthesized bullet points.

---

### Feature 5: Gmail Integration & Application Status Tracker
* **Status:** In Backlog
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
* **Status:** Completed
* **Objective:** Containerize the entire application into a self-contained, reproducible Docker image with all system binaries (Python, Streamlit, TeX Live / `latexmk`).
* **Core Capabilities:**
  * **Multi-Stage `Dockerfile`:**
    * Base Linux image with Python 3.11+.
    * Headless TeX Live distribution (`texlive-latex-base`, `texlive-latex-extra`, `latexmk`) pre-installed.
    * Python virtual environment with all required dependencies (`streamlit`, `google-genai`, etc.).
  * **`docker-compose.yml`:** Single-command local startup (`docker-compose up`) exposing port 8501.
  * **Cloud Run Ready:** Configured for scale-to-zero serverless deployment on Google Cloud Run.

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

## 🐛 Known Issues & Quality Enhancements

### Issue 1: Workday Mode Generates Identical/Repetitive Resumes Across Different JDs
* **Reported:** User observed that selecting **Workday** for different JDs consistently produces virtually identical resumes.
* **Root Causes Identified:**
  1. **Static Placeholder Companies:** `build_workday_prompt` lacks guidance on company naming or project domains. Without instruction, LLMs default to their most frequent training priors (`Tech Solutions Inc.` and `Cloud Systems Corp`).
  2. **Verbatim JD Copying:** `build_workday_prompt` strictly mandates exact keyword mirroring, but omits the Google XYZ formula (`Accomplished [X], measured by [Y], by doing [Z]`). Consequently, the model simply copies the extracted JD responsibilities verbatim as bullet points into the same two dummy companies.
  3. **Silent Failure & Stale File Masking:** In `deconstruct_jd.pipeline()`, exceptions during model calls are caught and printed to console without raising an exception to `app.py`. If a new generation fails or times out, `app.py` silently re-reads the old `new_resume.pdf` from the prior run and displays "Succeded".
* **Remediation Plan:**
  * **Dynamic Domain & Role Synthesis:** Instruct the Workday prompt to invent realistic, varied company names and projects that match the specific target industry (e.g., FinTech, E-commerce, Healthcare, Cloud SaaS) and target seniority.
  * **Google XYZ Metric Fusion:** Incorporate the Google XYZ achievement formula into `build_workday_prompt` so keywords are embedded within quantified impact statements rather than raw copied phrases.
  * **Artifact Purging & Error Propagation:** In `app.py` / `deconstruct_jd.py`, wipe existing `new_resume.pdf` before generation begins, and ensure API errors bubble up to display `st.error` in the UI rather than silently falling back to stale files.

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
Phase 4: Multi-ATS Rules Library (Feature 3) [ACTIVE]
  └── Specialized prompt rules for Greenhouse, Lever, iCIMS, Taleo
Phase 5: Daily Career Diary (Feature 4)
  └── Work journal + continuous bullet synthesizer
Phase 6: Job Search OS (Feature 5)
  └── Gmail OAuth integration + Automated application tracking dashboard
Phase 7: Ecosystem Integrations (Feature 7)
  └── Export & sync with ChatGPT, Cursor (.cursorrules), LinkedIn, and Naukri
```

| Phase | Milestone | Rationale & Value |
| :--- | :--- | :--- |
| **Phase 1 (Completed)** | **Docker Containerization** | Solves the dual Python + TeX Live environment dependency once and for all, making the app 100% portable. |
| **Phase 2 (Completed)** | **User Profile Form** | Establishes the structured data model and UI for user profile inputs and persistence. |
| **Phase 3 (Completed)** | **Resume Personalization** | Fuses real candidate profile data with target JDs using truth anchoring and XYZ formulas. |
| **Phase 4 (Active)** | **Multi-ATS Rules Library** | Extends Workday rules to Greenhouse, Lever, Taleo, and iCIMS. |
| **Phase 5** | **Daily Career Diary** | Adds day-to-day work journaling and automatic resume bullet updates. |
| **Phase 6** | **Gmail Job Tracker** | End-to-end tracking of job applications, rejection letters, and interview invites. |
| **Phase 7** | **Ecosystem Integrations** | Syndicates verified candidate data to ChatGPT, Cursor AI, LinkedIn, and Naukri. |
