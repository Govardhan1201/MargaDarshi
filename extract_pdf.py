import pypdf2
import os

pdf_path = r"C:\Users\user\Margadarshi\369649169-Visakhapatnam-City-Bus-Routes.pdf"

if os.path.exists(pdf_path):
    with open(pdf_path, "rb") as f:
        reader = pypdf2.PdfReader(f)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"
        
    with open(r"C:\Users\user\Margadarshi\full_pdf_text.txt", "w", encoding="utf-8") as f:
        f.write(full_text)
    print("Full text extracted to full_pdf_text.txt")
else:
    print("PDF not found at path")
