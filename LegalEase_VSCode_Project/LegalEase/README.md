# LegalEase – AI-Powered Legal Document Generator

This is a complete local VS Code project based on the supplied LegalEase specification.

## Features
- FastAPI backend
- Streamlit frontend
- Google Gemini document generation
- Inputs for document type, parties, terms, and effective date
- Editable preview
- TXT, DOCX and PDF downloads
- `.env` configuration

## Structure

```text
LegalEase/
├── backend/
│   ├── main.py
│   ├── routes.py
│   └── ai_core/
│       ├── __init__.py
│       └── gemini_generator.py
├── frontend/
│   └── app.py
├── utils/
│   ├── __init__.py
│   └── document_formatter.py
├── assets/
│   └── README.txt
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Run in VS Code

### 1. Create virtual environment

PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If activation is blocked:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 2. Install packages

```powershell
pip install -r requirements.txt
```

### 3. Configure Gemini

Copy `.env.example` to `.env` and add your API key:

```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-1.5-pro
BACKEND_URL=http://127.0.0.1:8000
```

### 4. Start FastAPI

Terminal 1:
```powershell
uvicorn backend.main:app --reload --port 8000
```

API:
`http://127.0.0.1:8000`

Swagger:
`http://127.0.0.1:8000/docs`

### 5. Start Streamlit

Terminal 2:
```powershell
streamlit run frontend/app.py
```

## Example

Document Type: `Freelance Work Contract`

Parties: `Jane Doe (Service Provider), TechNova Inc. (Client)`

Terms:
`Payment to be made within 30 days; Confidentiality must be maintained; Either party may terminate with 15 days notice`

Effective Date: `April 10, 2025`

## Important
This is an educational document-generation application. AI-generated legal content should be reviewed by a qualified legal professional before real-world use.
