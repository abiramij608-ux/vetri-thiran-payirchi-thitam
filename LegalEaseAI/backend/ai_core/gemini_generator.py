import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()


class GeminiDocumentGenerator:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured. "
                "Please add GEMINI_API_KEY to the .env file."
            )

        self.client = genai.Client(api_key=self.api_key)

        self.model = "gemini-3.7-flash"
    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
    ) -> str:
        """
        Generate a legal document draft using Gemini.
        """

        prompt = f"""
You are LegalEase, an AI-powered legal document drafting assistant.

Create a clear, professional legal document draft based on the
information provided below.

DOCUMENT TYPE:
{document_type}

PARTIES:
{parties}

TERMS AND CONDITIONS:
{terms}

EFFECTIVE DATE:
{effective_date}

Instructions:

1. Create a professional legal document suitable for editing.
2. Use clear and formal legal language.
3. Organize the document using appropriate headings and sections.
4. Include all information provided by the user.
5. Do not invent names, addresses, dates, amounts, case numbers,
   or other facts that were not provided.
6. If important information is missing, use placeholders such as
   [NAME], [ADDRESS], [DATE], or [AMOUNT].
7. Make the document easy to read and print.
8. Do not claim that this document is guaranteed to be legally valid.
9. At the end, add a short disclaimer stating that the draft should
   be reviewed by a qualified legal professional before use.

Generate only the legal document and the review disclaimer.
"""

        try:
            response = None

            for attempt in range(3):
                try:
                    response = self.client.models.generate_content(
                        model=self.model,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            temperature=0.35,
                            top_p=0.9,
                            max_output_tokens=4000,
                        ),
                    )

                    break

                except Exception as exc:
                    error_text = str(exc)

                    if (
                        "503" in error_text
                        or "UNAVAILABLE" in error_text
                    ):
                        if attempt < 2:
                            time.sleep(3 * (attempt + 1))
                            continue

                    raise

            if response is None:
                raise RuntimeError(
                    "Gemini service is temporarily unavailable."
                )

            content = response.text

            if not content:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return self._clean_text(content)

        except Exception as exc:
            raise RuntimeError(
                f"Failed to generate the legal document: {exc}"
            ) from exc

    @staticmethod
    def _clean_text(text: str) -> str:
        """
        Clean unnecessary whitespace from Gemini's response.
        """

        if not text:
            return ""

        lines = [line.rstrip() for line in text.splitlines()]

        cleaned_lines = []
        previous_blank = False

        for line in lines:
            if line.strip():
                cleaned_lines.append(line)
                previous_blank = False
            else:
                if not previous_blank:
                    cleaned_lines.append("")

                previous_blank = True

        return "\n".join(cleaned_lines).strip()