from pdf2docx import Converter
import subprocess
import os
import mammoth
import platform

IS_WINDOWS = platform.system() == "Windows"

if IS_WINDOWS:
    import comtypes.client
    import pythoncom


# ===============================
# DOCX → HTML
# ===============================
def convert_docx_to_html(input_path):
    with open(input_path, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        return result.value


# ===============================
# PDF → DOCX
# ===============================
def convert_pdf_to_docx(input_path, output_path):
    cv = Converter(input_path)
    cv.convert(output_path, start=0, end=None)
    cv.close()


# ===============================
# DOCX → PDF (LibreOffice)
# ===============================
def convert_docx_to_pdf(input_path, output_folder):

    input_path = os.path.abspath(input_path)
    output_folder = os.path.abspath(output_folder)

    if IS_WINDOWS:
        soffice = r"C:\Program Files\LibreOffice\program\soffice.exe"
    else:
        soffice = "libreoffice"   # Linux command

    command = [
        soffice,
        "--headless",
        "--convert-to",
        "pdf",
        input_path,
        "--outdir",
        output_folder
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        print(result.stderr)
        raise Exception("DOCX to PDF conversion failed.")


# ===============================
# WORD → PDF (Windows only)
# ===============================
def convert_word_to_pdf(input_path, output_path):

    if not IS_WINDOWS:
        raise Exception("MS Word conversion only works on Windows")

    pythoncom.CoInitialize()

    try:
        word = comtypes.client.CreateObject("Word.Application")
        word.Visible = False

        doc = word.Documents.Open(os.path.abspath(input_path))
        doc.SaveAs(os.path.abspath(output_path), FileFormat=17)
        doc.Close()
        word.Quit()

    finally:
        pythoncom.CoUninitialize()


# ===============================
# POWERPOINT → PDF (Windows only)
# ===============================
def convert_ppt_to_pdf(input_path, output_path):

    if not IS_WINDOWS:
        raise Exception("PowerPoint conversion only works on Windows")

    pythoncom.CoInitialize()

    try:
        powerpoint = comtypes.client.CreateObject("PowerPoint.Application")
        powerpoint.Visible = 1

        presentation = powerpoint.Presentations.Open(os.path.abspath(input_path))
        presentation.SaveAs(os.path.abspath(output_path), 32)
        presentation.Close()

        powerpoint.Quit()

    finally:
        pythoncom.CoUninitialize()


# ===============================
# EXCEL → PDF (Windows only)
# ===============================
def convert_excel_to_pdf(input_path, output_path):

    if not IS_WINDOWS:
        raise Exception("Excel conversion only works on Windows")

    pythoncom.CoInitialize()

    try:
        excel = comtypes.client.CreateObject("Excel.Application")
        excel.Visible = False

        workbook = excel.Workbooks.Open(os.path.abspath(input_path))
        workbook.ExportAsFixedFormat(0, os.path.abspath(output_path))
        workbook.Close()

        excel.Quit()

    finally:
        pythoncom.CoUninitialize()