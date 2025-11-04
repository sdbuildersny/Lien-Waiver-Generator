# 🧱 Lien Waiver Generator (Streamlit)

A simple internal-use Streamlit app for generating **Partial** and **Final** lien waivers automatically as ready-to-sign PDFs.

## 🚀 Features
- Choose between Partial/Final and Conditional/Unconditional waivers
- Fill out project, owner, contractor, and payment info
- Upload your company logo for the letterhead
- Export a clean, formatted PDF instantly

## 🛠️ Setup
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/lien-waiver-generator.git
cd lien-waiver-generator

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate    # Windows PowerShell

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 🧩 Customizing Templates
Templates are stored in `/templates`. You can modify or add new ones to match your state or company wording.

Each template uses Jinja2 placeholders:
```
{{ project_name }}, {{ owner_name }}, {{ contractor_name }}, {{ amount }}, {{ date }}
```

## 📄 Example Output
Each generated PDF includes:
- Company name and optional logo
- Filled-in waiver text
- Signature lines
- Auto date footer

---

*Created with ❤️ for construction companies to save time on lien paperwork.*
