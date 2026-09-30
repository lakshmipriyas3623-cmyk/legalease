import os
from dotenv import load_dotenv

load_dotenv()

try:
    import google.generativeai as genai
except ImportError:
    genai = None


class GeminiDocumentGenerator:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-pro").strip()

        if genai and self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
        else:
            self.model = None

    def generate_document(self, document_type, parties, terms, dates):
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY is missing. Add it to your .env file.")

        if not self.model:
            raise RuntimeError(
                "Google Generative AI package is unavailable. Run pip install -r requirements.txt."
            )

        prompt = f'''
You are LegalEase, an AI assistant that drafts structured legal documents.

Create a professional draft for this document.

Document type:
{document_type}

Parties:
{parties}

Terms and conditions:
{terms}

Effective date:
{dates}

Requirements:
1. Use clear formal legal-document language.
2. Include a title.
3. Include parties and effective date.
4. Organize the document with numbered sections.
5. Incorporate supplied terms without inventing important facts.
6. Include appropriate general provisions where useful.
7. End with signature blocks for relevant parties.
8. Do not claim the draft is legally reviewed or legally guaranteed.
9. Return plain text only, without Markdown code fences.
'''

        response = self.model.generate_content(prompt)

        if not response or not getattr(response, "text", None):
            raise RuntimeError("Gemini returned an empty response.")

        return response.text.strip()
