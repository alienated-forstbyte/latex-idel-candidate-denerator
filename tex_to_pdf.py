import os
import shutil
import subprocess

LATEXMK_PATH = "/Library/TeX/texbin/latexmk"

def compile_latex_to_pdf(file_name):
    pdflatex_bin = shutil.which("latexmk") or LATEXMK_PATH

    if not (shutil.which("latexmk") or os.path.exists(LATEXMK_PATH)):
        raise FileNotFoundError("pdflatex compiler not found in this system")

    print(f"Building PDF from {file_name}..")

    # result = subprocess.run([
    #     "mkdir -p ./resumes/"
    # ])

    step = subprocess.run([
        shutil.which("latexmk") or LATEXMK_PATH,
        "-C",
        file_name
    ])

    result = subprocess.run([
        shutil.which("latexmk") or LATEXMK_PATH,
        "-pdf",
        "-interaction=nonstopmode",
        "-file-line-error",
        file_name
        ],
        capture_output=True,
        text=True
    )
    pdf_filename = file_name.replace(".tex",".pdf")
    if os.path.exists(pdf_filename):
        print("Successfully generated pdf resume")
        for ext in ['.aux','.log','.out','.fls','.fdb_latexmk'] :
            temp_file = file_name.replace('.tex',ext)
            if os.path.exists(temp_file):
                os.remove(temp_file)
    else :
        print("Error compiling latex")