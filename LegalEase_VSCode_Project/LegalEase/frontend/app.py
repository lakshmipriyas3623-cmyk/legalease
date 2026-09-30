import os
import requests
import streamlit as st
from dotenv import load_dotenv

from utils.document_formatter import (
    format_docx,
    format_pdf,
    format_html_preview,
    sanitize_text,
)

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")

st.set_page_config(page_title="LegalEase", page_icon="⚖️", layout="wide")

st.markdown(
    '''
    <style>
    .main-title {text-align:center;font-size:42px;font-weight:700;margin-bottom:0;}
    .subtitle {text-align:center;color:#6b7280;margin-bottom:28px;}
    </style>
    ''',
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">⚖️ LegalEase</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">AI-Powered Legal Document Generator</div>',
    unsafe_allow_html=True,
)

if "generated_text" not in st.session_state:
    st.session_state.generated_text = ""
if "editing" not in st.session_state:
    st.session_state.editing = False
if "doc_type" not in st.session_state:
    st.session_state.doc_type = "Agreement"

with st.form("legal_form"):
    col1, col2 = st.columns(2)

    with col1:
        doc_type = st.text_input(
            "Document Type",
            value=st.session_state.doc_type,
            placeholder="e.g. Employment Contract",
        )
        parties = st.text_area(
            "Parties Involved",
            placeholder="Jane Doe (Employee), ABC Corp (Employer)",
            height=120,
        )

    with col2:
        dates = st.text_input(
            "Effective Date",
            placeholder="e.g. April 10, 2025",
        )
        terms = st.text_area(
            "Terms & Conditions",
            placeholder="Separate clauses with semicolons; Payment within 30 days; Maintain confidentiality",
            height=120,
        )

    submitted = st.form_submit_button(
        "✨ Generate Document",
        use_container_width=True,
        type="primary",
    )

if submitted:
    if not all([doc_type.strip(), parties.strip(), terms.strip(), dates.strip()]):
        st.error("Please fill in all four fields.")
    else:
        with st.spinner("Generating your legal document..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json={
                        "document_type": doc_type,
                        "parties": parties,
                        "terms": terms,
                        "dates": dates,
                    },
                    timeout=120,
                )
                response.raise_for_status()
                data = response.json()
                st.session_state.generated_text = data["text"]
                st.session_state.doc_type = doc_type
                st.session_state.editing = False
                st.success("Document generated successfully.")
            except requests.exceptions.ConnectionError:
                st.error(
                    "Cannot connect to FastAPI. Start it with: "
                    "uvicorn backend.main:app --reload --port 8000"
                )
            except requests.exceptions.RequestException as exc:
                try:
                    detail = response.json().get("detail", str(exc))
                except Exception:
                    detail = str(exc)
                st.error(f"Generation failed: {detail}")

if st.session_state.generated_text:
    st.divider()
    st.subheader("Document Preview")

    if st.button(
        "✏️ Edit Document" if not st.session_state.editing else "👁️ Preview Document"
    ):
        st.session_state.editing = not st.session_state.editing

    if st.session_state.editing:
        st.session_state.generated_text = st.text_area(
            "Edit the generated document",
            value=st.session_state.generated_text,
            height=520,
        )
    else:
        st.markdown(
            format_html_preview(
                st.session_state.generated_text,
                st.session_state.doc_type,
            ),
            unsafe_allow_html=True,
        )

    st.subheader("Download")

    txt_data = sanitize_text(st.session_state.generated_text).encode("utf-8")
    docx_data = format_docx(
        st.session_state.generated_text,
        st.session_state.doc_type,
    )
    pdf_data = format_pdf(
        st.session_state.generated_text,
        st.session_state.doc_type,
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.download_button(
            "⬇️ Download TXT",
            data=txt_data,
            file_name="legalease_document.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with c2:
        st.download_button(
            "⬇️ Download DOCX",
            data=docx_data,
            file_name="legalease_document.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )
    with c3:
        st.download_button(
            "⬇️ Download PDF",
            data=pdf_data,
            file_name="legalease_document.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

st.divider()
st.caption(
    "Educational project. AI-generated legal text should be reviewed by a qualified legal professional before real-world use."
)
