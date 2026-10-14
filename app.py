import streamlit as st
import os
import deconstruct_jd

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


def generate_resume(jd_text:str):
    with open('JD.txt',mode='w',encoding='utf-8') as f:
        f.write(jd_text)
    deconstruct_jd.pipeline()

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
    col_input , col_output = st.columns([1,1],gap="medium")
    with col_input:
        st.subheader("Job Description")
        default_jd = ""
        if os.path.exists('JD.txt'):
            with open('JD.txt',mode = 'r', encoding='utf-8') as f:
                default_jd = f.read()

        jd_input = st.text_area("Job Description",default_jd,400,placeholder="Paste JD here")

        generate_button = st.button("Generate",type="primary",use_container_width=True)

        if generate_button:
            if not jd_input.strip():
                st.warning("Please paste JD")
            else:
                with st.spinner():
                    try:
                        generate_resume(jd_input)
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

if __name__ == "__main__":
    main()


# def set_ui():

#     col_input, col_output = st.columns([1,1])

#     with col_input:
#         st.subheader("Job Desciption")
#         jd = st.text_area("Paste JD here: ",height=350)
#         st.button("generate")
#     with col_output:
#         st.subheader("Generated resume")

#     with st.spinner("Analyzing JD and compiling resume"):
#         generate_resume()

#     tab_preview, tab_latex = st.tabs(["Preview","Latex"])
#     with tab_preview:
#         st.markdown("### Overview")
#     with tab_latex:
#         st.code(st.session_state.latex_code, language="latex")


# def download_resume():
#     try:
#         with open('new_resume.pdf', 'rb') as f:
#             generated_pdf = f.read()
#         st.download_button("Download",generated_pdf,"resume_company.pdf",mime="application/pdf")
#     except Exception as e:
#         print(e)
