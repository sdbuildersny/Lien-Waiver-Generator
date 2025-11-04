import os
import streamlit as st
from jinja2 import Template
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle

# -------------------------------
# Template configuration
# -------------------------------
TEMPLATES = {
    "Final Unconditional": "final_unconditional.txt",
}

def load_template(template_name):
    base_dir = os.path.dirname(__file__)
    template_path = os.path.join(base_dir, "templates", template_name)
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("Lien Waiver Generator")

waiver_type = st.selectbox("Select Waiver Type", list(TEMPLATES.keys()))

# User input fields
fields = {
    "subcontractor": st.text_input("Subcontractor"),
    "contractor": st.text_input("Contractor"),
    "owner": st.text_input("Owner"),
    "premises_project": st.text_input("Premises/Project"),
    "contract_date": st.text_input("Contract Date"),
    "original_amount": st.text_input("Original Contract Amount"),
    "change_orders": st.text_input("Change Order Amounts"),
    "adjusted_amount": st.text_input("Adjusted Contract Amount"),
    "total_payments": st.text_input("Total Payments Received to Date"),
    "final_application_date": st.text_input("Date of Final Application for Payment"),
    "final_application_amount": st.text_input("Amount of Final Application for Payment"),
}

# -------------------------------
# Generate PDF
# -------------------------------
if st.button("Generate PDF"):
    # Load and render template
    template_text = load_template(TEMPLATES[waiver_type])
    template = Template(template_text)
    rendered_text = template.render(**fields)

    pdf_path = f"{waiver_type.replace(' ', '_')}.pdf"

    # Create PDF document
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=LETTER,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    # Define style to preserve spacing and indentation
    pre_style = ParagraphStyle(
        name="Preformatted",
        fontName="Courier",
        fontSize=10,
        leading=12,
        leftIndent=0,
        firstLineIndent=0,
        spaceAfter=6,
    )

    # Replace tabs with spaces for alignment
    rendered_text = rendered_text.replace('\t', '    ')

    # Split the text into paragraphs at double newlines
    paragraphs = rendered_text.split("\n\n")

    # Convert each paragraph to a Paragraph flowable
    flowables = []
    for para in paragraphs:
        flowables.append(Paragraph(f"<pre>{para}</pre>", pre_style))
        flowables.append(Spacer(1, 6))

    # Build the PDF
    doc.build(flowables)

    st.success(f"PDF generated: {pdf_path}")
    st.download_button(
        "Download PDF",
        data=open(pdf_path, "rb").read(),
        file_name=pdf_path
    )
