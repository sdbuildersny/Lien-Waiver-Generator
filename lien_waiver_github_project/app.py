import streamlit as st
from jinja2 import Template
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from io import BytesIO
import datetime
import os

# --- Helper functions ---
def load_template(template_name):
    path = os.path.join("templates", template_name)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def render_template(template_text, context):
    tpl = Template(template_text)
    return tpl.render(**context)

def create_pdf_bytes(title, body_text, company_name=None, logo_bytes=None):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=LETTER,
                            rightMargin=72,leftMargin=72,
                            topMargin=72,bottomMargin=72)
    styles = getSampleStyleSheet()
    normal = styles['Normal']
    heading = ParagraphStyle('Heading', parent=styles['Heading1'], fontSize=14, spaceAfter=12)
    small = ParagraphStyle('Small', parent=styles['Normal'], fontSize=9)

    story = []
    if logo_bytes:
        try:
            img = Image(BytesIO(logo_bytes))
            img.drawHeight = 0.8*inch
            img.drawWidth = 0.8*inch
            story.append(img)
        except Exception:
            pass

    if company_name:
        story.append(Paragraph(f"<b>{company_name}</b>", heading))
    story.append(Paragraph(f"<b>{title}</b>", heading))
    story.append(Spacer(1, 12))

    for para in body_text.split("\n\n"):
        para = para.replace("\n", "<br/>")
        story.append(Paragraph(para.strip(), normal))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 18))
    story.append(Paragraph("Signature: _________________________________", normal))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Printed Name: _____________________________", normal))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Title: _____________________________________", normal))
    story.append(Spacer(1, 24))
    story.append(Paragraph(f"Generated on {datetime.date.today().isoformat()}", small))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()

# --- Streamlit UI ---
st.set_page_config(page_title="Lien Waiver Generator", layout="centered")
st.title("Lien Waiver Generator")

TEMPLATES = {
    "Partial Conditional": "partial_conditional.txt",
    "Partial Unconditional": "partial_unconditional.txt",
    "Final Conditional": "final_conditional.txt",
    "Final Unconditional": "final_unconditional.txt",
}

st.sidebar.header("Options")
waiver_type = st.sidebar.selectbox("Lien Waiver Type", list(TEMPLATES.keys()))
company_name = st.sidebar.text_input("Company/Letterhead name (optional)")
logo_file = st.sidebar.file_uploader("Upload logo (optional)", type=['png','jpg','jpeg'])

st.header("Waiver Details")
col1, col2 = st.columns(2)
with col1:
    subcontractor = st.text_input("Subcontractor")
    contractor = st.text_input("Contractor")
    owner = st.text_input("Owner")
    premises_project = st.text_input("Premises/Project")
    contract_date = st.date_input("Contract Date", datetime.date.today())
    original_amount = st.text_input("Original Contract Amount")
with col2:
    change_orders = st.text_input("Change Order Amounts")
    adjusted_amount = st.text_input("Adjusted Contract Amount")
    total_payments = st.text_input("Total Payments Received to Date")
    final_app_date = st.date_input("Date of Final Application for Payment", datetime.date.today())
    final_app_amount = st.text_input("Amount of Final Application for Payment")

notes = st.text_area("Additional notes or custom language (optional)", height=120)

if st.button("Generate PDF"):
    def parse_amount(val):
        try:
            return f"{float(val.replace(',','')):,.2f}" if val else "0.00"
        except:
            return val

    context = {
        "subcontractor": subcontractor,
        "contractor": contractor,
        "owner": owner,
        "premises_project": premises_project,
        "contract_date": contract_date.isoformat(),
        "original_amount": parse_amount(original_amount),
        "change_orders": parse_amount(change_orders),
        "adjusted_amount": parse_amount(adjusted_amount),
        "total_payments": parse_amount(total_payments),
        "final_application_date": final_app_date.isoformat(),
        "final_application_amount": parse_amount(final_app_amount),
        "notes": notes
    }

    tpl_text = load_template(TEMPLATES[waiver_type])
    filled = render_template(tpl_text + "\n\n" + (notes or ""), context)
    logo_bytes = logo_file.read() if logo_file else None
    pdf_bytes = create_pdf_bytes(f"{waiver_type} Lien Waiver", filled, company_name, logo_bytes)

    st.success("PDF generated successfully!")
    st.download_button("Download Lien Waiver PDF", pdf_bytes,
                       file_name=f"lien_waiver_{waiver_type.replace(' ','_').lower()}.pdf",
                       mime="application/pdf")

st.markdown("---")
st.markdown("Customize templates in the `/templates` folder for state-specific wording or additional fields.")
