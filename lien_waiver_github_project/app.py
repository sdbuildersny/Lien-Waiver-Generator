import os
import streamlit as st
from jinja2 import Template
from reportlab.platypus import SimpleDocTemplate, Preformatted
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import LETTER

# -------------------------------
# Template configuration
# -------------------------------
TEMPLATES = {
    "Partial Conditional": "partial_conditional.txt",
    "Partial Unconditional": "partial_unconditional.txt",
    "Final Conditional": "final_conditional.txt",
    "Final Unconditional": "final_unconditional.txt",
}

def load_template(template_name):
    """
    Load a template file from the templates/ folder relative to this script.
    Works both locally and on Streamlit Cloud.
    """
    base_dir = os.path.dirname(__file__)
    template_path = os.path.join(base_dir, "templates", template_name)
    template_path = os.path.abspath(template_path)

    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("Lien Waiver Generator")

waiver_type = st.selectbox("Select Waiver Type", list(TEMPLATES.keys()))

# Fields for the waiver
subcontractor = st.text_input("Subcontractor")
contractor = st.text_input("Contractor")
owner = st.text_input("Owner")
premises_project = st.text_input("Premises/Project")
contract_date = st.text_input("Contract Date")
original_amount = st.text_input("Original Contract Amount")
change_orders = st.text_input("Change Order Amounts")
adjusted_amount = st.text_input("Adjusted Contract Amount")
total_payments = st.text_input("Total Payments Received to Date")
final_application_date = st.text_input("Date of Final Application for Payment")
final_application_amount = st.text_input("Amount of Final Application for Payment")
notes = st.text_area("Notes (optional)")

# -------------------------------
# Generate PDF
# -------------------------------
if st.button("Generate PDF"):
    # Load template
    template_text = load_template(TEMPLATES[waiver_type])
    template = Template(template_text)

    # Render template with user input
    rendered_text = template.render(
        subcontractor=subcontractor,
        contractor=contractor,
        owner=owner,
        premises_project=premises_project,
        contract_date=contract_date,
        original_amount=original_amount,
        change_orders=change_orders,
        adjusted_amount=adjusted_amount,
        total_payments=total_payments,
        final_application_date=final_application_date,
        final_application_amount=final_application_amount,
        notes=notes
    )

    # PDF path
    pdf_path = f"{waiver_type.replace(' ', '_')}.pdf"

    # Create PDF document
    doc = SimpleDocTemplate(pdf_path, pagesize=LETTER,
                            leftMargin=50, rightMargin=50,
                            topMargin=50, bottomMargin=50)

    # Define monospaced style
    styles = getSampleStyleSheet()
    preformatted_style = styles["Code"]  # Monospaced
    preformatted_style.fontSize = 11
    preformatted_style.leading = 14

    # Use Preformatted to preserve exact formatting
    flowable = Preformatted(rendered_text, preformatted_style)

    # Build PDF
    doc.build([flowable])

    st.success(f"PDF generated: {pdf_path}")
    st.download_button(
        "Download PDF",
        data=open(pdf_path, "rb").read(),
        file_name=pdf_path
    )
