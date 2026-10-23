import os
import re
from google import genai
from tex_to_pdf import compile_latex_to_pdf
from dotenv import load_dotenv

load_dotenv()

GCP_API_KEY = os.environ.get("GCP_API_KEY")
WORKDAY_RULES = """
STRICT WORKDAY COMPLIANCE RULES:
1. LAYOUT: Pure single-column linear layout only. Do NOT use tables, minipages, text boxes, sidebars, or graphic icons.
2. DATES: Every role must strictly use 'Mon YYYY – Present' or 'Mon YYYY – Mon YYYY' (e.g., 'Jan 2024 – Present').
3. HEADINGS: Use only standard section headings: Professional Summary, Work Experience, Skills, Education, Certifications.
4. KEYWORD MIRRORING & DUAL ACRONYMS: Pair both the acronym and spelled-out form: e.g., 'Continuous Integration / Continuous Deployment (CI/CD)', 'Infrastructure as Code (IaC)'.
5. PAGINATION: Add '\\pagestyle{empty}' to suppress footer page numbers.
"""
GREENHOUSE_RULES = """
STRICT GREENHOUSE COMPLIANCE RULES:
1. JOB TITLE ALIGNMENT: Align the candidate's professional headline and target title directly with the target Job Title for high semantic matching.
2. DIGITAL PRESENCE & LINKS: Prominently format clickable LinkedIn and GitHub profile links in the contact header.
3. ACTION-VERB FRONT-LOADING: Every bullet MUST begin with a powerful technical action verb (e.g., 'Architected', 'Automated', 'Engineered', 'Orchestrated', 'Optimized').
4. GOOGLE XYZ IMPACT: Quantify achievements with metrics (latency reductions, infrastructure cost savings, build failure decreases).
"""
LEVER_RULES = """
STRICT LEVER COMPLIANCE RULES:
1. LINEAR TEXT EXTRACTION: Pure single-column linear layout with clean section boundaries for Lever's plain-text extraction reader.
2. FRONT-LOADED SKILLS INVENTORY: Place the Technical Skills block immediately below the Professional Summary so core competencies are tagged first.
3. SKILL-TO-EXPERIENCE PROXIMITY: Explicitly mention tools and frameworks inside the bullet points where they were used to trigger Lever's contextual matching.
4. HYPERLINKED PROFILES: Hyperlink all portfolio and repository URLs in the header.
"""
TALEO_ICIMS_RULES = """
STRICT TALEO & iCIMS COMPLIANCE RULES:
1. LEGACY PARSER SAFETY: Zero tables, zero columns, zero custom bullets or non-standard glyphs. Use standard LaTeX '\\item'.
2. CHRONOLOGICAL INTEGRITY: Strict reverse-chronological experience ordering with clear month/year demarcations on their own lines.
3. CATEGORIZED TAXONOMY: Structure skills into explicit categories: 'Programming Languages', 'Cloud & DevOps Infrastructure', 'Frameworks & Tools', 'Databases'.
4. NATURAL KEYWORD FREQUENCY: Naturally distribute required keywords across the Summary, Skills, and Experience sections.
"""
GENERIC_RULES = """
STANDARD ATS COMPLIANCE RULES:
1. LAYOUT: Professional, modern, single-page LaTeX document.
2. BULLETS: Every experience bullet must strictly follow the Google XYZ formula: "Accomplished [X], measured by [Y], by doing [Z]".
3. SECTIONS: Include Contact Header, Professional Summary, Technical Skills, Work Experience with XYZ metric bullets, and Education.
"""

client = genai.Client(api_key=GCP_API_KEY)

DEFAULT_FALLBACK_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-flash-latest",
    "gemini-2.5-pro",
]

def generate_content_with_fallback(contents, config=None, preferred_model=None):
    """
    Calls Gemini generate_content with automatic model fallback across
    multiple models to prevent 503 UNAVAILABLE or 429 high demand crashes.
    """
    models_to_try = []
    if preferred_model:
        models_to_try.append(preferred_model)
    for m in DEFAULT_FALLBACK_MODELS:
        if m not in models_to_try:
            models_to_try.append(m)

    last_error = None
    for model_name in models_to_try:
        try:
            kwargs = {"model": model_name, "contents": contents}
            if config:
                kwargs["config"] = config
            response = client.models.generate_content(**kwargs)
            return response
        except Exception as e:
            last_error = e
            print(f"[Model Fallback] {model_name} failed: {e}. Trying next model...")
            continue

    # Dynamic fallback to any available model supported on client
    try:
        for m in client.models.list():
            if "generateContent" in (m.supported_actions or []) and m.name not in models_to_try:
                try:
                    kwargs = {"model": m.name, "contents": contents}
                    if config:
                        kwargs["config"] = config
                    response = client.models.generate_content(**kwargs)
                    return response
                except Exception:
                    continue
    except Exception:
        pass

    raise last_error

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
        response = generate_content_with_fallback(
            contents=prompt,
            preferred_model=model
        )

        with open("extracted_jd.txt", mode = "w", encoding="utf-8") as f:
            f.write(response.text)

def get_ats_rules(ats_system: str) -> str:
    if ats_system == "Workday":
        return WORKDAY_RULES
    elif ats_system == "Greenhouse":
        return GREENHOUSE_RULES
    elif ats_system == "Lever":
        return LEVER_RULES
    elif ats_system in ["Oracle Taleo", "iCIMS", "SAP SuccessFactors"]:
        return TALEO_ICIMS_RULES
    return GENERIC_RULES

def build_prompt(criteria: str, ats_system: str, user_profile: dict = None) -> str:
    ats_rules = get_ats_rules(ats_system)
    
    if user_profile and user_profile.get("name"):
        candidate_section = f"""
TRUTH ANCHORING: Strictly preserve the candidate's genuine Name, Contact Info, Company Names, Employment Dates, and Education from the User Profile. Do NOT invent fake employers or degrees. Enhance their actual experience using the Google XYZ formula.

Candidate Profile:
Name: {user_profile.get("name", "")}
Email: {user_profile.get("email", "")}
Phone: {user_profile.get("phone", "")}
LinkedIn: {user_profile.get("linkedin", "")}
GitHub: {user_profile.get("github", "")}
Professional Summary: {user_profile.get("summary", "")}
Technical Skills: {user_profile.get("skills", "")}
Work Experience: {user_profile.get("experience", "")}
Education: {user_profile.get("education", "")}
"""
    else:
        candidate_section = """
SYNTHETIC CANDIDATE MODE:
Generate a 10/10 ideal candidate profile matching the target job description.
DYNAMIC DOMAINS: Invent realistic, varied company names and technical projects that reflect the target industry (e.g., FinTech, Cloud SaaS, Healthcare), avoiding repetitive placeholder names.
SYNTHETIC CANDIDATE DOMAIN DIVERSITY:
1. Deduce the target industry from the Job Criteria (e.g., FinTech, HealthTech, CyberSecurity, E-Commerce, Autonomous Robotics).
2. Invent 2-3 realistic, distinguished company names that reflect that specific industry (e.g., 'Aura Payments Group', 'Helix Clinical AI').
3. STRICT PROHIBITION: Do NOT use generic placeholder names like 'Tech Solutions Inc.', 'Cloud Systems Corp', 'Acme Corp', or 'Software LLC'.
"""

    return f"""
You are an Executive Resume Writer and LaTeX typographer specializing in ATS optimization.
Using the following Job Criteria and Candidate Details, write a 100% matching, high-impact single-page resume in standard compilable LaTeX.

REQUIREMENTS:
1. Output ONLY valid LaTeX code starting with \\documentclass and ending with \\end{{document}}.
2. Escape all special characters like %, _, &, and $.
3. Every experience bullet MUST follow the Google XYZ formula: "Accomplished [X], measured by [Y], by doing [Z]" and naturally weave in the required keywords.

{ats_rules}

Target Job Criteria:
{criteria}

{candidate_section}
"""

def generate_resume(model, ats_system, user_profile):
    with open('extracted_jd.txt', mode='r', encoding='utf-8') as e:
        criteria = e.read()
        prompt = build_prompt(criteria, ats_system, user_profile)
        response = generate_content_with_fallback(contents=prompt,preferred_model=model)
        # response = client.models.generate_content(
        #     model=model,
        #     contents=prompt
        # )

        with open('new_resume.tex',mode='w',encoding='utf-8') as r:
            latex_code = response.text
            if "```latex" in latex_code:
                latex_code = latex_code.split("```latex")[1].split("```")[0].strip()
            elif "```" in latex_code:
                latex_code = latex_code.split("```")[1].split("```")[0].strip()
            r.write(latex_code)
        compile_latex_to_pdf('new_resume.tex')

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename components by removing illegal filesystem characters
    and collapsing multiple spaces into underscores.
    """
    if not filename:
        return ""
    cleaned = re.sub(r'[^\w\s-]', '', str(filename))
    return re.sub(r'\s+', '_', cleaned.strip())

def extract_job_title(criteria_text: str) -> str:
    """
    Extract the job title from the LLM-analyzed criteria text.
    """
    if not criteria_text:
        return ""
    match = re.search(r"Job Title[\*\:]*\s*[\n:]+\s*([^\n\*\#]+)", criteria_text, re.IGNORECASE)
    if match:
        title = match.group(1).replace("*", "").strip()
        return title[:50].strip()
    return ""

def generate_resume_filename(candidate_name: str = "", job_title: str = "", company: str = "", ats_type: str = "") -> str:
    """
    Assemble an ATS-friendly, standardized resume filename:
    {Candidate_Name}_{Job_Title}_{Company}_{ATS}_Resume.pdf
    """
    parts = []
    
    clean_name = sanitize_filename(candidate_name)
    if clean_name:
        parts.append(clean_name)
    else:
        parts.append("Candidate")
        
    clean_title = sanitize_filename(job_title)
    if clean_title:
        parts.append(clean_title)
        
    clean_company = sanitize_filename(company)
    if clean_company:
        parts.append(clean_company)
        
    clean_ats = sanitize_filename(ats_type)
    if clean_ats:
        parts.append(clean_ats)
        
    parts.append("Resume")
    return "_".join(parts) + ".pdf"

print("Available Models")
def pipeline(ats_system:str, user_profile: dict = None):
    client = genai.Client(api_key=GCP_API_KEY)

    success = False
    last_error = None

    for m in client.models.list():
        if "generateContent" in (m.supported_actions or []): 
            print(f" -> {m.name}")
            try:
                get_response(m.name)
                generate_resume(m.name, ats_system, user_profile)
                if os.path.exists('new_resume.pdf'):
                    success = True
                    break
                else:
                    raise RuntimeError("LaTeX compilation failed to produce new_resume.pdf")
            except Exception as e:
                last_error = e
                print(f"[Model Failover] Model {m.name} failed: {e}")
                continue
    if not success:
        error_msg = f"Failed to generate resume across all available models. Last error: {last_error}"
        if last_error:
            raise RuntimeError(error_msg) from last_error
        else:
            raise RuntimeError(error_msg)
