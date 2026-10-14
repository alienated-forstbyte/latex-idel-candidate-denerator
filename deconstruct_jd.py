from google import genai
from tex_to_pdf import compile_latex_to_pdf
client = genai.Client(api_key=GCP_API_KEY)

def get_response(model):
    with open("JD.txt","r",encoding="utf-8") as c:
        content = c.read()
        prompt = f"""
Analyze this job description and extract:
1. Job Title
2. Seniority Level
3. Required Years of Experience
4. Top 5 Must-Have Skills
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

def generate_resume(model):
    with open('extracted_jd.txt', mode='r', encoding='utf-8') as e:
        criteria = e.read()
        prompt = '''
You are an Executive Resume Writer and LaTeX typographer specializing in ATS optimization.
Using the following Job Criteria, write a 100% matching, high-impact single-page "Ideal Candidate Resume" in standard compilable LaTeX.
Every experience bullet MUST follow the Google XYZ formula: "Accomplished [X], measured by [Y], by doing [Z]" and naturally weave in the required keywords.
REQUIREMENTS:
1. Output ONLY valid LaTeX code starting with \\documentclass and ending with \\end{document}.
2. Escape all special characters like %, _, &, and $.
3. Include: Header, Professional Summary, Technical Skills (Python, Go, Kubernetes, Docker, Terraform), Work Experience with XYZ metric bullets, and Education.
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
def pipeline():
    client = genai.Client(api_key=GCP_API_KEY)
    for m in client.models.list():
        if "generateContent" in (m.supported_actions or []): 
            print(f" -> {m.name}")
            try:
                get_response(m.name)
                print("Resulted")
                generate_resume(m.name)
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