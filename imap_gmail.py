import imaplib
import os
import streamlit as st
import dotenv
import email
from email.header import decode_header
import job_tracker

dotenv.load_dotenv()

def get_credentials():
    dotenv.load_dotenv()
    user = os.environ.get("GMAIL_USER", "").strip()
    # Remove spaces from Google's 16-character App Password format (e.g. 'abcd efgh ijkl mnop' -> 'abcdefghijklmnop')
    app_pwd = os.environ.get("GMAIL_APP_PASSWORD", "").replace(" ", "").strip()
    return user, app_pwd

def connect_to_gmail(username, app_password):
    if not username or not app_password:
        return None
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        mail.login(username, app_password)
        return mail
    except imaplib.IMAP4.error as e:
        print(f"IMAP login failed: {e}")
        return None
    except Exception as e:
        print(f"IMAP connection failed: {e}")
        return None

def clean_header_text(header_val: str) -> str:
    if not header_val:
        return ""
    try:
        decoded_parts = decode_header(header_val)
        parts = []
        for text, encoding in decoded_parts:
            if isinstance(text, bytes):
                parts.append(text.decode(encoding or "utf-8", errors="replace"))
            else:
                parts.append(str(text))
        return " ".join(parts).strip()
    except Exception:
        return str(header_val)

def search_emails(mail, max_results: int = 10):
    try:
        mail.select("inbox")
    except Exception as e:
        print(f"Failed to select inbox: {e}")
        return []

    # Gmail raw query targeting common ATS senders and recruiter keywords
    raw_query = 'from:(greenhouse.io OR lever.co OR myworkday.com OR smartrecruiters.com OR jobvite.com OR ashbyhq.com OR icims.com) OR "application received" OR "interview" OR "job offer"'
    
    email_ids = []
    try:
        # Note: Gmail's X-GM-RAW syntax strictly requires the query string to be wrapped in double quotes
        result, data = mail.search(None, "X-GM-RAW", f'"{raw_query}"')
        if result == "OK" and data and data[0]:
            email_ids = data[0].split()
    except Exception as e:
        print(f"X-GM-RAW search failed: {e}. Falling back to recent emails.")

    # Fallback to standard search if X-GM-RAW yields no results or is unsupported
    if not email_ids:
        try:
            result, data = mail.search(None, "ALL")
            if result == "OK" and data and data[0]:
                email_ids = data[0].split()
        except Exception as e:
            print(f"Fallback search failed: {e}")
            return []

    return email_ids[-max_results:] if email_ids else []

def decode_email_body(msg) -> str:
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition", ""))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or "utf-8"
                    return payload.decode(charset, errors="replace")
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or "utf-8"
            return payload.decode(charset, errors="replace")
    return ""

def fetch_job_emails(mail, email_ids: list) -> list:
    job_emails = []
    for e_id in email_ids:
        try:
            result, data = mail.fetch(e_id, "(RFC822)")
            if result == "OK" and data and isinstance(data[0], tuple):
                raw_email = data[0][1]
                msg = email.message_from_bytes(raw_email)
                subject = clean_header_text(msg.get("subject", ""))
                body = decode_email_body(msg)
                job_emails.append({"subject": subject, "body": body})
        except Exception as e:
            print(f"Error fetching email {e_id}: {e}")
            continue
    return job_emails

def sync_inbox_with_tracker(max_results: int = 10) -> int:
    username, app_password = get_credentials()
    if not username or not app_password:
        st.warning("Gmail credentials missing. Please set GMAIL_USER and GMAIL_APP_PASSWORD in your .env file.")
        return 0

    mail = connect_to_gmail(username, app_password)
    if not mail:
        st.error("Failed to connect to Gmail. Please check your App Password in .env.")
        return 0

    synced_count = 0
    try:
        email_ids = search_emails(mail, max_results=max_results)
        if not email_ids:
            return 0
        job_emails = fetch_job_emails(mail, email_ids)
        for job_email in job_emails:
            subject = job_email.get("subject", "")
            body = job_email.get("body", "")
            full_email_text = f"Subject: {subject}\n\n{body}"
            try:
                job_tracker.job_classifier(email_text=full_email_text)
                synced_count += 1
            except Exception as e:
                print(f"[Sync Warning] Failed to classify email '{subject}': {e}")
                continue
        return synced_count
    finally:
        try:
            mail.close()
            mail.logout()
        except Exception:
            pass

def render_sync_gmail():
    st.markdown("### Gmail Inbox Synchronization")
    st.caption("Sync recent recruiter communications (Greenhouse, Lever, Workday, etc.) directly into your Tracker.")

    username, app_password = get_credentials()
    if not username or not app_password:
        st.warning("Gmail credentials not found. Please set `GMAIL_USER` and `GMAIL_APP_PASSWORD` in your `.env` file.")
        return

    st.info(f"Connected Account: **{username}**")

    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("Sync Inbox Now", type="primary", use_container_width=True):
            with st.spinner("Connecting to Gmail and parsing recruiter emails..."):
                synced = sync_inbox_with_tracker(max_results=10)
                if synced > 0:
                    st.toast(f"Successfully processed {synced} emails into Tracker!")
                    st.success(f"Processed {synced} recruiter emails. Head to the Tracker tab to view updated statuses.")
                    st.rerun()
                else:
                    st.info("No new recruiter emails found in inbox.")