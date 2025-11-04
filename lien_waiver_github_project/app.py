import os
import streamlit as st
from jinja2 import Template
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
import locale

# -------------------------------
# Locale for number formatting
# -------------------------------
locale.setlocale(locale.LC_ALL, '')  # system locale

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
# Formatting functions
# -------------------------------
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
    template_text = load_template(TEMPLATES[waiver_type])
    template = Template(template_text)

    # Format numeric fields
    formatted_fields = fields.copy()
    for key in ["original_amount", "change_orders", "adjusted_amount", "total_payments", "final_application_amount"]:
        formatted_fields[key] = format_currency(fields[key])

    # Render template
    rendered_text = template.render(**formatted_fields)

    # Wrap all field values in <b> for bold
    for key, value in formatted_fields.items():
        if value.strip():  # only wrap non-empty
            rendered_text = rendered_text.replace(value, f"<b>{value}</b>")

    pdf_path = f"{waiver_type.replace(' ', '_')}.pdf"

    # PDF document setup
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=LETTER,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    # Preformatted style to preserve spacing/indentation
    pre_style = ParagraphStyle(
        name="Preformatted",
        fontName="Courier",
        fontSize=10,
        leading=12,
        leftIndent=0,
        firstLineIndent=0,
        spaceAfter=2,
    )

    # Replace tabs with spaces
    rendered_text = rendered_text.replace('\t', '    ')

    # Split into individual lines to preserve exact formatting
    lines = rendered_text.splitlines()

    flowables = []
    for line in lines:
        flowables.append(Paragraph(f"<pre>{line}</pre>", pre_style))

    # Build PDF
    doc.build(flowables)

    st.success(f"PDF generated: {pdf_path}")
    st.download_button(
        "Download PDF",
        data=open(pdf_path, "rb").read(),
        file_name=pdf_path
    )
