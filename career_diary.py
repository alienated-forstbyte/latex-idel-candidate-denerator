import os
import streamlit as st
import json
import deconstruct_jd
from user_form import render_profile_tab
import datetime  


def load_diary_entries(file_path: str = 'diary_entries.json'):
    if os.path.exists(file_path):
        with open(file_path, mode='r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return []

def save_diary_entries(entries: list, file_path: str = 'diary_entries.json'):
    with open(file_path, mode='w', encoding='utf-8') as f:
        json.dump(entries, f, indent=4)

def systhesize_bullet_points(entries: list):
    criteria = "\n".join([f"- {entry}" for entry in entries])
    prompt = f"""
You are an Executive Resume Writer and LaTeX typographer specializing in ATS optimization.
Using the following diary entries, synthesize them into concise, high-impact bullet points suitable for a resume. Ensure that each bullet point follows the Google XYZ formula: "Accomplished [X], measured by [Y], by doing [Z]" and naturally weaves in relevant keywords."""
    bullet_points = deconstruct_jd.generate_content_with_fallback(
        contents=f"{prompt}\n\nDiary Entries:\n{criteria}",
        preferred_model="gemini-2.5-flash"
    )
    return bullet_points.text

def sync_bullets_to_user_profile(entries: list, user_profile: dict):
    if not entries:
        st.warning("No diary entries to sync.")
        return
    synthesized_bullets = systhesize_bullet_points(entries)
    user_profile["experience"] = f"{user_profile.get('experience', '').strip()} \n {synthesized_bullets}"
    with open('user_profile.json', mode='w', encoding='utf-8') as f:
        json.dump(user_profile, f, indent=4)
        st.toast("Diary entries synced to user profile successfully!")
def normalize_entry(entry: dict | str) -> dict:
    

def render_diary_tab():
    st.markdown("### Career Diary")
    entries = load_diary_entries()
    new_entry = st.text_area("Add a new diary entry", "")
    if st.button("Add Entry"):
        if new_entry.strip():
            entries.append(new_entry.strip())
            save_diary_entries(entries)
            st.toast("Entry added successfully!")
        else:
            st.warning("Please enter a valid diary entry.")
    if entries:
        st.markdown("#### Your Diary Entries:")
        for i, entry in enumerate(entries, 1):
            st.markdown(f"{i}. {entry}")
    if not entries:
        st.info("No diary entries yet. Add some to synthesize bullet points for your resume.")
    st.button("Sync to User Profile", on_click=sync_bullets_to_user_profile, args=(entries, st.session_state.user_profile))