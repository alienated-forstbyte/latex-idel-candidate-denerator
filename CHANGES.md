# Summary of Recent Changes & Review Log

This document records the architectural improvements, bug fixes, and feature integrations made across the codebase for review.

---

## 1. `job_tracker.py` (Refactoring & Bug Fixes)

* **Unified Data Model & Merging Logic:**
  * Replaced conflicting loader functions with a single, clean `load_applications()` returning `{}` when no applications exist (ensuring the `Total Applied` metric starts accurately at `0` instead of `1`).
  * Eliminated the `TypeError` (`unsupported operand type(s) for +: 'dict' and 'dict'`) and `AttributeError` (`'dict' object has no attribute 'append'`) by standardizing on a dictionary collection keyed by company name (`applications[company] = new_app`).
  * Implemented automatic company updating: if an email is received from an already tracked company, it updates the `status`, updates `last_updated`, and appends new notes without creating duplicate records.
* **Structured Output Enforcement:**
  * Configured `client.models.generate_content` with `config={"response_mime_type": "application/json"}` to guarantee pure JSON responses from Gemini, completely eliminating markdown code fence (` ```json `) decode crashes in `json.loads`.
* **Persistence & Session Synchronization:**
  * Implemented `save_applications()` using overwrite mode (`mode='w'`), updating `st.session_state.job_application_status` in-place so the UI refreshes immediately upon submission.
* **Presentation Layer:**
  * In `render_tracker_tab()`, added a dedicated recruiter email text area, submission button with loading spinner, toast notifications, an interactive `st.dataframe` table, and an expander for raw JSON inspection.

---

## 2. `app.py` (State & Metric Hardening)

* **Startup Initialization:**
  * Added `import job_tracker` and invoked `job_tracker.init_session_state()` inside `app.py`'s `init_session_state()`, eliminating the startup crash where top-level metrics rendered before the Tracker tab was loaded.
* **Safe Metric Counters:**
  * Hardened the KPI metric row (`Total Applied`, `In Interviews`, `Offers Received`, `Rejected`) using `isinstance(v, dict)` and `.get("status")` checks to prevent `KeyError` crashes if records have missing keys.
* **Tab Navigation:**
  * Wired the 4th tab (`Tracker`) to call `job_tracker.render_tracker_tab()`.

---

## 3. `todo.md` (Roadmap & Backlog Updates)

* **Status Milestones:**
  * Updated **Phase 4 (Multi-ATS Rules Library)** to **[COMPLETED]**.
  * Updated **Phase 5 (Daily Career Diary)** to **[COMPLETED]**.
  * Updated **Phase 6 (Job Search OS & Gmail Tracker)** to **[ACTIVE]**.
* **Backlog Additions:**
  * Added Career Diary enhancements (date-stamping, two-step preview & sync, date-range filtering).
  * Added **Feature 8: Existing Resume Parser & Profile Auto-Fill** (upload PDF/DOCX/LaTeX/TXT resumes to auto-populate the User Profile form via structured LLM extraction).
  * Added **Feature 9: Jira Ticket Tracking & Skill Extraction Integration** (scans completed Jira tickets to automatically log career diary entries and update technical skills).
  * Added **Feature 10: Centralized Logging, Diagnostics & Error Observability** (structured `app.log` file/console logging and in-app diagnostics viewer to prevent silent failures).
  * Added **Feature 11: Truth & Fact-Check Auditor Module ("Anti-Lie" / Hallucination Detector)** (cross-examines generated resumes against ground truth profile/diary to flag fabricated claims).
  * Added **Feature 12: Streamlit UI / UX Modernization & Live PDF Preview** (live inline PDF viewer, drag-and-drop Kanban application tracker, and responsive CSS theming).
  * Added **Feature 13: Dynamic & Configurable Resume File Naming** (configurable token-based filenames such as `{Name}_{Role}_{Company}_Resume.pdf` with sanitization).

---

## 4. `deconstruct_jd.py` (Strategy Pattern & Multi-ATS Rules)

* **Single-Pass Prompt Assembly:**
  * Replaced duplicated LaTeX template concatenations with the unified `build_prompt(criteria, ats_system, user_profile)` strategy pattern.
* **ATS Rule Sets & Guardrails:**
  * Integrated dedicated rulesets for Workday, Greenhouse, Lever, Taleo, iCIMS, and Generic ATS systems.
  * Added Truth Anchoring constraints for candidate profile mode and Dynamic Domain synthesis for synthetic candidate mode to prevent generic placeholder company repetition.

---

## 5. `imap_gmail.py` (IMAP Protocol Hardening & Bug Fixes)

* **Resolved `SEARCH command error: BAD [b'Could not parse command']`:**
  * Enclosed the `X-GM-RAW` search query in literal double quotes (`f'"{raw_query}"'`), ensuring IMAP interprets multi-word queries as a single argument.
  * Added fallback to standard `ALL` search if `X-GM-RAW` is unsupported, with slicing to the most recent 10 emails.
* **Resolved `IMAP login failed: socket error: EOF`:**
  * Prevented unmanaged connections on every page load by removing eager connection in `render_sync_gmail()`. Connection now triggers only when the user clicks **"Sync Inbox Now"**.
  * Enclosed socket interactions in `try ... finally` blocks to guarantee `mail.close()` and `mail.logout()` execute, preventing Gmail connection pool exhaustion.
* **MIME Header & Body Robustness:**
  * Added `clean_header_text()` using `email.header.decode_header()` to decode MIME-encoded subject headers (`=?UTF-8?B?...`).
  * Combined `Subject: ...` and `Body: ...` before forwarding to `job_classifier()`, ensuring Gemini captures company names and job titles from headers.
  * Auto-stripped whitespace from Google's 16-character App Password format to prevent `AUTHENTICATIONFAILED` errors.

---

## 6. Multi-Model Failover & Resiliency Engine (`deconstruct_jd.py`, `job_tracker.py`, `career_dairy.py`)

* **Resolved `503 UNAVAILABLE` / High Demand Crashes:**
  * Created `generate_content_with_fallback()` in `deconstruct_jd.py` with an automated failover chain:
    `["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-flash-latest", "gemini-2.5-pro"]`.
  * If the primary model experiences sudden demand spikes or temporary 503/429 errors, the system seamlessly catches the error, logs a failover warning, and tries the next model in the tier.
  * Integrated across `job_tracker.py` (email classification), `career_dairy.py` (bullet synthesis), and `imap_gmail.py` batch loops.
  * Wrapped batch email processing in `imap_gmail.py` with per-email exception handling so a single failed email never aborts the rest of the inbox sync.

---

## 7. Backlog Specification: Feature 14 (Email Triage & Noise Filtering Engine)

* **Documented in [`todo.md`](file:///Users/tk-agrawal/ATK/MLOps/job-to-ideal-resume/todo.md):**
  * Added Feature 14 to specify a two-tier filtering system:
    1. Fast heuristic pre-filtering for known automated alert senders and alert subject lines (`"new jobs matching"`, `"job alert"`).
    2. Lightweight structured LLM classifier to filter out job recommendation digests, talent newsletters, and promotional spam before invoking the deep application extractor.
  * Added UI audit / noise metrics tracking so filtered emails can be inspected without polluting active application records.



