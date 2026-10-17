import os
import json
import streamlit as st

def init_session_state():
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = load_user_profile()
    

def load_user_profile():
    if os.path.exists('user_profile.json'):
        with open('user_profile.json', mode='r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return {
            "name": "",
            "email": "",
            "phone": "",
            "linkedin": "",
            "github": "",
            "summary" : "",
            "skills": "",
            "experience": "",
            "education": ""
        }

def save_user_profile(profile_data: dict, file_path: str = 'user_profile.json'):
    with open(file_path, mode='w', encoding='utf-8') as f:
        json.dump(profile_data, f, indent=4)
        st.session_state.user_profile = profile_data

def render_profile_tab():
    with st.form("profile_form"):
        with st.expander("Contact Information", expanded=True):
            st.text_input("Full Name", value=st.session_state.user_profile.get("name", ""), key="name")
            st.text_input("Email", value=st.session_state.user_profile.get("email", ""), key="email")
            st.text_input("Phone Number", value=st.session_state.user_profile.get("phone", ""), key="phone")
            st.text_input("LinkedIn Profile URL", value=st.session_state.user_profile.get("linkedin", ""), key="linkedin")
            st.text_input("GitHub Profile URL", value=st.session_state.user_profile.get("github", ""), key="github")
        with st.expander("Summary and Skills", expanded=True):
            st.text_input("Professional Summary", value=st.session_state.user_profile.get("summary", ""), key="summary")
            st.text_area("Technical Skills (comma-separated)", value=st.session_state.user_profile.get("skills", ""), key="skills")
        with st.expander("Work Experience", expanded=True):
            st.text_area("Experience Details", value=st.session_state.user_profile.get("experience", ""), key="experience")
        with st.expander("Education", expanded=True):
            st.text_area("Education Details", value=st.session_state.user_profile.get("education", ""), key="education")
        st_save_button =st.form_submit_button("Save Profile")
        if st_save_button:
            profile_data = {
                "name": st.session_state.name,
                "email": st.session_state.email,
                "phone": st.session_state.phone,
                "linkedin": st.session_state.linkedin,
                "github": st.session_state.github,
                "summary": st.session_state.summary,
                "skills": st.session_state.skills,
                "experience": st.session_state.experience,
                "education": st.session_state.education
            }
            save_user_profile(profile_data)
            st.success("Profile saved successfully!")

def main():
    st.set_page_config(
        "Job Resume Generator",
        layout="wide"
    )

    init_session_state()

    st.title("User Profile")
    st.caption("Fill in your profile information to generate resumes")

    render_profile_tab()

if __name__ == "__main__":
    main()