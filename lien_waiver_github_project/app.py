import io
import streamlit as st
from jinja2 import Template
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import locale
import os

# -------------------------------
# Locale for number formatting
# -------------------------------
locale.setlocale(locale.LC_ALL, '')  # system locale

# -------------------------------
# Load templates
# -------------------------------
template_folder = os.path.join(os.path.dirname(__file__), "templates")
templates_list = [f for f in os.listdir(template_folder) if f.endswith(".txt")]
TEMPLATES = {os.path.splitext(f)[0]: f for f in templates_list}

# -------------------------------
# Streamlit page config
# -------------------------------
st.set_page_config(
    page_title="Lien Waiver Generator",
    page_icon="📝",
    layout="centered",
)

# -------------------------------
# Landing page
# -------------------------------
st.markdown("<h1 style='text-align: center;'>📝 Lien Waiver Generator</h1>", unsafe_allow_html=True)
st.markdown(
    """
    Generate professional lien waivers quickly and easily.  
    Fill in the details below and click 'Generate PDF' to download your waiver.
    """,
    unsafe_allow_html=True
)
st.markdown("---")

if not templates_list:
    st.warning("⚠️ No templates found in the 'templates' folder.")
    st.stop()

# -------------------------------
# Waiver type selection
# -------------------------------
waiver_type = st.selectbox(
    "Select Waiver Type",
    options=list(TEMPLATES.keys()),
    help="Choose the type of waiver you want to generate."
)

st.markdown("### Enter Waiver Details")
st.info("Fields marked below will appear bold in the generated PDF.")

# -------------------------------
# User input fields
# -------------------------------
col1, col2 = st.columns(2)
fields = {}

with col1:
    fields["subcontractor"] = st.text_input("Subcontractor")
    fields["contractor"] = st.text_input("Contractor")
    fields["owner"] = st.text_input("Owner")
    fields["premises_project"] = st.text_input("Premises/Project")
    fields["contract_date"] = st.text_input("Contract Date")
    fields["original_amount"] = st.text_input("Original Contract Amount")
    fields["change_orders"] = st.text_input("Change Order Amounts")

with col2:
    fields["adjusted_amount"] = st.text_input("Adjusted Contract Amount")
    fields["total_payments"] = st.text_input("Total Payments Received to Date")
    fields["requisition_number"] = st.text_input("Requisition No.")
    fields["date_of_this_requisition"] = st.text_input("Date of this Requisition")
    fields["amount_of_this_requisition"] = st.text_input("Amount of this Requisition")
    fields["final_application_date"] = st.text_input("Date of Final Application for Payment")
    fields["final_application_amount"] = st.text_input("Amount of Final Application for Payment")

# -------------------------------
# Generate PDF
# -------------------------------
if st.button("Generate PDF"):
    # Load template
    template_text = open(os.path.join(template_folder, TEMPLATES[waiver_type]), "r", encoding="utf-8").read()
    template = Template(template_text)

    # Format numeric fields
    formatted_fields = fields.copy()
    for key in ["original_amount", "change_orders", "adjusted_amount", "total_payments", "amount_of_this_requisition", "final_application_amount"]:
        formatted_fields[key] = "${:,.2f}".format(float(fields[key])) if fields[key] else ""

    # Render template
    rendered_text = template.render(**formatted_fields)

    # -------------------------------
    # Build PDF in memory
    # -------------------------------
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=LETTER,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    lines = rendered_text.splitlines()
    flowables = []

    # Header (first non-empty line)
    for idx, line in enumerate(lines):
        if line.strip():
            flowables.append(Paragraph(f"<b>{line.strip()}</b>", ParagraphStyle(
                name="Header",
                fontName="Times-Roman",
                fontSize=14,
                leading=16,
                alignment=TA_CENTER,
                spaceAfter=12,
            )))
            lines.pop(idx)
            break

    # Body
    body_style = ParagraphStyle(
        name="Body",
        fontName="Times-Roman",
        fontSize=10,
        leading=12,
        leftIndent=0,
        firstLineIndent=0,
        spaceAfter=4,
    )

    for line in lines:
        if line.strip():
            flowables.append(Paragraph(line, body_style))

    doc.build(flowables)

    st.success("✅ PDF generated successfully!")
    st.download_button(
        "Download PDF",
        data=pdf_buffer.getvalue(),
        file_name=f"{waiver_type.replace(' ', '_')}.pdf",
        mime="application/pdf"
    )


