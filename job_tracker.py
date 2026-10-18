import os
import json
import deconstruct_jd
import streamlit as st
import imap_gmail

FILE_PATH = 'job_application_status.json'

def load_applications(file_path: str = FILE_PATH) -> dict:
    if os.path.exists(file_path):
        try:
            with open(file_path, mode='r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    # Clean out any empty placeholder keys from prior tests
                    if "application_id" in data and not data["application_id"].get("company_name"):
                        del data["application_id"]
                    return data
                elif isinstance(data, list):
                    return {item.get("company_name", f"App_{i}"): item for i, item in enumerate(data) if isinstance(item, dict)}
        except Exception:
            return {}
    return {}

def save_applications(applications: dict, file_path: str = FILE_PATH) -> None:
    with open(file_path, mode='w', encoding='utf-8') as f:
        json.dump(applications, f, indent=4)
    st.session_state.job_application_status = applications

def init_session_state() -> None:
    if "job_application_status" not in st.session_state:
        st.session_state.job_application_status = load_applications()

def job_classifier(email_text: str = None) -> None:
    if not email_text or not email_text.strip():
        st.warning("Please paste email text before updating.")
        return

    prompt = f"""
Read this email and extract the job application status into JSON.
Return a single JSON object with these exact fields:
- company_name: Name of the hiring company.
- job_title: Title of the role applied for.
- application_date: Date applied (YYYY-MM-DD or as stated in email).
- last_updated: Date of this email/update (YYYY-MM-DD or as stated).
- status: Exactly one of: "Applied", "Interviewing", "Offer Received", "Rejected".
- notes: Brief summary of key details, next steps, or interview schedule.

JSON structure:
{{
    "company_name": "",
    "job_title": "",
    "application_date": "",
    "last_updated": "",
    "status": "",
    "notes": ""
}}

Email:
{email_text}
"""
    response = deconstruct_jd.generate_content_with_fallback(
        contents=prompt,
        config={"response_mime_type": "application/json"},
        preferred_model="gemini-2.5-flash"
    )

    new_app = json.loads(response.text)
    if isinstance(new_app, list) and new_app:
        new_app = new_app[0]
    elif not isinstance(new_app, dict):
        new_app = {}

    company = new_app.get("company_name", "").strip() or f"Application_{len(st.session_state.job_application_status) + 1}"

    applications = load_applications()

    if company in applications:
        applications[company]["status"] = new_app.get("status", applications[company].get("status", "Applied"))
        if new_app.get("last_updated"):
            applications[company]["last_updated"] = new_app.get("last_updated")
        if new_app.get("job_title") and not applications[company].get("job_title"):
            applications[company]["job_title"] = new_app.get("job_title")
        if new_app.get("notes"):
            existing_notes = applications[company].get("notes", "")
            applications[company]["notes"] = f"{existing_notes} | {new_app.get('notes')}".strip(" |")
    else:
        applications[company] = new_app

    save_applications(applications)

def render_tracker_tab() -> None:
    init_session_state()
    st.markdown("### Job Application Tracker")
    st.caption("Automatically detect and track job applications, recruiter communications, and interview statuses.")

    email_text = st.text_area(
        "Paste Recruiter / Confirmation Email:",
        placeholder="Paste confirmation email, interview invite, or update here...",
        height=160,
        key="tracker_email_input"
    )

    if st.button("Classify & Update Tracker", type="primary"):
        if not email_text.strip():
            st.warning("Please paste email content first.")
        else:
            with st.spinner("Analyzing email with Gemini..."):
                try:
                    job_classifier(email_text=email_text)
                    st.toast("Application record updated successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error classifying email: {e}")

    st.markdown("#### Tracked Applications")
    applications = st.session_state.job_application_status

    if st.button("Sync Gmail"):
        imap_gmail.sync_inbox_with_tracker()
        st.toast("Gmail inbox synced successfully!")
        st.rerun()

    if applications:
        table_data = list(applications.values())
        st.dataframe(table_data, use_container_width=True)
        with st.expander("View Raw JSON"):
            st.json(applications)
    else:
        st.info("No job applications tracked yet. Paste a job application or recruiter email above to track your first application.")