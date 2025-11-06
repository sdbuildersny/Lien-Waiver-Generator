import os
import streamlit as st
from jinja2 import Template
from reportlab.platypus import SimpleDocTemplate, Paragraph, Preformatted
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import locale

# -------------------------------
# Locale for number formatting
# -------------------------------
locale.setlocale(locale.LC_ALL, '')

# -------------------------------
# Load templates dynamically
# -------------------------------
template_folder = os.path.join(os.path.dirname(__file__), "templates")
templates_list = [f for f in os.listdir(template_folder) if f.endswith(".txt")]
TEMPLATES = {os.path.splitext(f)[0]: f for f in templates_list}

# -------------------------------
# Helper functions
# -------------------------------
def load_template(template_name):
    template_path = os.path.join(template_folder, TEMPLATES[template_name])
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()

def format_currency(value):
    try:
        number = float(value)
        return f"${number:,.2f}"
    except:
        return value

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("Lien Waiver Generator")

if not templates_list:
    st.warning("No templates found in the 'templates' folder.")
    st.stop()

waiver_type = st.selectbox("Select Waiver Type", list(TEMPLATES.keys()))

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
    template_text = load_template(waiver_type)
    template = Template(template_text)

    # Format numeric fields
    formatted_fields = fields.copy()
    for key in ["original_amount", "change_orders", "adjusted_amount", "total_payments", "final_application_amount"]:
        formatted_fields[key] = format_currency(fields[key])

    # Render template with values
    rendered_text = template.render(**formatted_fields)

    pdf_path = f"{waiver_type.replace(' ', '_')}.pdf"

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=LETTER,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    # Split lines
    lines = rendered_text.splitlines()
    flowables = []

    # Extract header (first non-empty line)
    header_line = None
    for idx, line in enumerate(lines):
        if line.strip():
            header_line = line.strip()
            lines.pop(idx)
            break

    if header_line:
        header_style = ParagraphStyle(
            name="Header",
            fontName="Times-Roman",
            fontSize=14,
            leading=16,
            alignment=TA_CENTER,
            spaceAfter=12
        )
        flowables.append(Paragraph(f"<b>{header_line}</b>", header_style))

    # Preformatted style for body text
    pre_style = ParagraphStyle(
        name="Preformatted",
        fontName="Times-Roman",
        fontSize=10,
        leading=12,
    )

    # Bold inputs inside the preformatted text
    for key, value in formatted_fields.items():
        if value.strip():
            rendered_text = rendered_text.replace(value, f"<b>{value}</b>")

    # Re-split lines after bolding
    lines = rendered_text.splitlines()
    for line in lines:
        # Replace tabs with spaces for proper alignment
        line = line.replace("\t", "    ")
        flowables.append(Preformatted(line, pre_style))

    # Build PDF
    doc.build(flowables)

    st.success(f"PDF generated: {pdf_path}")
    st.download_button(
        "Download PDF",
        data=open(pdf_path, "rb").read(),
        file_name=pdf_path
    )
