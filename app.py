import streamlit as st
import os
import deconstruct_jd
from user_form import render_profile_tab 
import user_form

def init_session_state():
    if "extracted_criteria" not in st.session_state:
        if os.path.exists('extracted_jd.txt'):
            with open('extracted_jd.txt', mode = 'r',encoding='utf-8') as f:
                st.session_state.extracted_criteria = f.read()
        else:
            st.session_state.extracted_criteria = ""
    if "generated_pdf" not in st.session_state:
        if os.path.exists('new_resume.pdf'):
            with open('new_resume.pdf', mode='rb') as f:
                st.session_state.generated_pdf = f.read()
        else:
            st.session_state.generated_pdf = None
    if "latex_code" not in st.session_state:
        if os.path.exists('new_resume.tex'):
            with open('new_resume.tex', mode='r',encoding='utf-8') as f:
                st.session_state.latex_code = f.read()
        else :
            st.session_state.latex_code = ""
    if "user_profile" not in st.session_state:
        user_form.init_session_state()


def generate_resume(jd_text:str, ats_system:str, user_profile: dict = None):
    with open('JD.txt',mode='w',encoding='utf-8') as f:
        f.write(jd_text)
    deconstruct_jd.pipeline(ats_system, user_profile)

    if os.path.exists("extracted_jd.txt"):
        with open('extracted_jd.txt',mode='r',encoding='utf-8') as f:
            st.session_state.extracted_criteria = f.read()

    if os.path.exists("new_resume.tex"):
        with open('new_resume.tex',mode='r',encoding='utf-8') as f:
            st.session_state.latex_code = f.read()

    if os.path.exists('new_resume.pdf'):
        with open('new_resume.pdf',mode='rb') as f:
            st.session_state.generated_pdf = f.read()

def main():
    st.set_page_config(
        "Job Resume Generator",
        layout="wide"
    )

    init_session_state()

    st.title("Job Resume Generator")
    st.caption("Create an ideal candidate")

    tab_generate, tab_profile = st.tabs(["Generate Resume","Profile"])
    with tab_generate:

        col_input , col_output = st.columns([1,1],gap="medium")
        with col_input:
            st.subheader("Job Description")
            default_jd = ""
            if os.path.exists('JD.txt'):
                with open('JD.txt',mode = 'r', encoding='utf-8') as f:
                    default_jd = f.read()

            jd_input = st.text_area("Job Description",default_jd,400,placeholder="Paste JD here")

            ats_systems = ["Workday","Greenhouse","Lever","iCIMS","SmartRecruiters","Jobvite","BambooHR","JazzHR","Bullhorn","SAP SuccessFactors","Oracle Taleo","ADP Recruiting Management","ClearCompany","CATS","ApplicantPro","Zoho Recruit","Recruitee","Breezy HR","Hireology","Avature","Recruiterbox","PeopleFluent","PCRecruiter","JobDiva","Vincere","TrackerRMS","Manatal","Freshteam","Teamtailor","Workable","Recruitee","SmartRecruiters","JazzHR","Breezy HR","Zoho Recruit","CATS","ClearCompany","iCIMS","Bullhorn","Greenhouse","Lever","BambooHR","Jobvite","SAP SuccessFactors","Oracle Taleo","ADP Recruiting Management","ApplicantPro","Recruitee","Hireology","Avature","Recruiterbox","PeopleFluent","PCRecruiter","JobDiva","Vincere","TrackerRMS","Manatal","Freshteam","Teamtailor","Generic"]
            ats_system = st.selectbox("Select ATS System",ats_systems)

            mode_toggle = st.toggle("Profile",value=True,key="user_profile_toggle")

            generate_button = st.button("Generate",type="primary",use_container_width=True)

            if generate_button:
                if not jd_input.strip():
                    st.warning("Please paste JD")
                else:
                    with st.spinner():
                        try:
                            generate_resume(jd_input, ats_system, user_profile=st.session_state.user_profile if mode_toggle else None)
                            st.success("Succeded")
                        except Exception as e:
                            st.error(e)

        with col_output:
            st.subheader("benchmark")
            if st.session_state.generated_pdf:
                st.download_button(
                    label="Download",
                    data=st.session_state.generated_pdf,
                    file_name="new_id_resume.pdf",
                    mime="application/pdf",
                    type='primary',
                    use_container_width=True)
            else:
                st.info("Unable to download")
            
            tab_preview, tab_latex = st.tabs(["Extracted Criteria","latex preview"])

            with tab_preview:
                st.markdown("###Job Criteria")
                if st.session_state.extracted_criteria:
                    st.markdown(st.session_state.extracted_criteria)
                else:
                    st.caption("No Criteria was extracted")

            with tab_latex:
                st.markdown("##Latex Code")
                if st.session_state.latex_code:
                    st.code(st.session_state.latex_code)
                else:
                    st.caption("No latex code generated")
    with tab_profile:
        render_profile_tab()


if __name__ == "__main__":
    main()
