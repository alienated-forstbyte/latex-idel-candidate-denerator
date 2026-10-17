from google import genai
from tex_to_pdf import compile_latex_to_pdf
import user_form

GCP_API_KEY = os.environ.get("GCP_API_KEY", None)

client = genai.Client(api_key=GCP_API_KEY)

def get_response(model):
    with open("JD.txt","r",encoding="utf-8") as c:
        content = c.read()
        prompt = f"""
Analyze this job description and extract:
1. Job Title
2. Seniority Level
3. Required Years of Experience
4. Top Must-Have Skills
5. Core Responsibilities
Job Description:
{content}
"""
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )

        with open("extracted_jd.txt", mode = "w", encoding="utf-8") as f:
            f.write(response.text)


def build_workday_prompt(criteria: str) -> str:
    WORKDAY_PROMPT = """
You are an expert Resume Strategist specializing in Workday ATS parser compliance.
Using the following Job Criteria, generate a single-page compilable LaTeX resume.
STRICT WORKDAY PARSER RULES:
1. LAYOUT: Pure single-column linear layout only. Do NOT use tables, minipages, text boxes, or icons.
2. DATES: Every role must strictly use 'Mon YYYY – Present' or 'Mon YYYY – Mon YYYY' (e.g., 'Jan 2024 – Present').
3. HEADINGS: Use only standard section headings: Professional Summary, Work Experience, Skills, Education, Certifications.
4. KEYWORD MIRRORING: Match exact casing, tenses, and wording from the JD (do not substitute synonyms or plurals).
5. ACRONYMS: Pair both the acronym and the spelled-out form: e.g., 'Project Management Professional (PMP)'.
6. EDUCATION: Clearly list Degree, Institution, and Graduation Date on separate lines.
Job Criteria:
__CRITERIA__
""".replace("__CRITERIA__",criteria)
    return WORKDAY_PROMPT

def build_personalized_prompt(criteria: str, user_profile: dict) -> str:
    PERSONALIZED_PROMPT = f"""
You are an Executive Resume Writer and LaTeX typographer specializing in ATS optimization.
Using the following Job Criteria and User Profile, write a 100% matching, high-impact single-page "Ideal Candidate Resume" in standard compilable LaTeX.
Every experience bullet MUST follow the Google XYZ formula: "Accomplished [X], measured by [Y], by doing [Z]" and naturally weave in the required keywords.
REQUIREMENTS:
1. Output ONLY valid LaTeX code starting with \\documentclass and ending with \\end{document}.
2. Escape all special characters like %, _, &, and $.
3. Include: Header, Professional Summary, Technical Skills , Work Experience with XYZ metric bullets, and Education.
4. Strictly preserve the candidate's actual company names, employment dates, and university degrees from the User Profile. Do NOT fabricate fake employers or degrees. Enhance their actual responsibilities using the Google XYZ formula.
Target Job Criteria:
__CRITERIA__
User Profile:
Name: {user_profile.get("name","")}
Email: {user_profile.get("email","")}
Phone: {user_profile.get("phone","")}
LinkedIn: {user_profile.get("linkedin","")}
GitHub: {user_profile.get("github","")}
Professional Summary: {user_profile.get("summary","")}
Technical Skills: {user_profile.get("skills","")}
Work Experience: {user_profile.get("experience","")}
Education: {user_profile.get("education","")}
""".replace("__CRITERIA__",criteria)
    return PERSONALIZED_PROMPT

def generate_resume(model, ats_system, user_profile):
    with open('extracted_jd.txt', mode='r', encoding='utf-8') as e:
        criteria = e.read()
        if user_profile:
            prompt = build_personalized_prompt(criteria, user_profile)
        elif ats_system == "Workday":
            prompt = build_workday_prompt(criteria)
        else:
            prompt = '''
    You are an Executive Resume Writer and LaTeX typographer specializing in ATS optimization.
    Using the following Job Criteria, write a 100% matching, high-impact single-page "Ideal Candidate Resume" in standard compilable LaTeX.
    Every experience bullet MUST follow the Google XYZ formula: "Accomplished [X], measured by [Y], by doing [Z]" and naturally weave in the required keywords.
    REQUIREMENTS:
    1. Output ONLY valid LaTeX code starting with \\documentclass and ending with \\end{document}.
    2. Escape all special characters like %, _, &, and $.
    3. Include: Header, Professional Summary, Technical Skills , Work Experience with XYZ metric bullets, and Education.
    Target Job Criteria:
    __CRITERIA__
    '''.replace("__CRITERIA__",criteria)
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )

        with open('new_resume.tex',mode='w',encoding='utf-8') as r:
            latex_code = response.text
            if "```latex" in latex_code:
                latex_code = latex_code.split("```latex")[1].split("```")[0].strip()
            elif "```" in latex_code:
                latex_code = latex_code.split("```")[1].split("```")[0].strip()
            r.write(latex_code)
        compile_latex_to_pdf('new_resume.tex')


print("Available Models"),
def pipeline(ats_system:str, user_profile: dict = None):
    client = genai.Client(api_key=GCP_API_KEY)
    for m in client.models.list():
        if "generateContent" in (m.supported_actions or []): 
            print(f" -> {m.name}")
            try:
                get_response(m.name)
                print("Resulted")
                generate_resume(m.name, ats_system, user_profile)
                print("Done")
                break
            except Exception as e:
                print(e)
                continue
# try:
#     get_response(models[0])
# except Exception as e:
#     print(e)

# def get_response(model):
#     with open("JD.txt","r",encoding="utf-8") as c:
#         content = c.read()
#         prompt = f"""
# Analyze this job description and extract:
# 1. Job Title
# 2. Seniority Level
# 3. Required Years of Experience
# 4. Top 5 Must-Have Skills
# 5. Core Responsibilities
# Job Description:
# {content}
# """
#         client.models.generate_content(
#             model=model,
#             contents=prompt
#         )