import streamlit as st
import requests

# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="LegalEaseAI",
    page_icon="⚖️",
    layout="wide",
)

# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown(
    """
    <style>
        .main-title {
            font-size: 42px;
            font-weight: 700;
            text-align: center;
            margin-bottom: 5px;
        }

        .subtitle {
            text-align: center;
            font-size: 18px;
            margin-bottom: 30px;
        }

        .section-title {
            font-size: 24px;
            font-weight: 600;
            margin-top: 10px;
            margin-bottom: 15px;
        }

        .disclaimer {
            padding: 15px;
            border-radius: 8px;
            margin-top: 25px;
            font-size: 14px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    '<div class="main-title">⚖️ LegalEaseAI</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">AI-Powered Legal Document Draft Generator</div>',
    unsafe_allow_html=True,
)

st.divider()

# --------------------------------------------------
# Document form
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Create Your Legal Document</div>',
    unsafe_allow_html=True,
)

document_type = st.selectbox(
    "Document Type",
    [
        "Rental Agreement",
        "Leave and License Agreement",
        "Affidavit",
        "Non-Disclosure Agreement",
        "Employment Agreement",
        "Sale Agreement",
        "Legal Notice",
        "Power of Attorney",
        "Other",
    ],
)

parties = st.text_area(
    "Parties",
    placeholder="Example: Landlord: Arun Kumar; Tenant: Priya",
    height=100,
)

terms = st.text_area(
    "Terms and Conditions",
    placeholder="Enter the important terms and conditions...",
    height=180,
)

effective_date = st.date_input(
    "Effective Date",
)

# --------------------------------------------------
# Generate button
# --------------------------------------------------

if st.button(
    "Generate Legal Document",
    type="primary",
    use_container_width=True,
):

    if not parties.strip():
        st.error("Please enter the parties involved.")

    elif not terms.strip():
        st.error("Please enter the terms and conditions.")

    else:
        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "effective_date": effective_date.isoformat(),
        }

        backend_url = "http://127.0.0.1:8000/generate"

        with st.spinner("Generating your legal document..."):

            try:
                response = requests.post(
                    backend_url,
                    json=payload,
                    timeout=120,
                )

                if response.status_code == 200:

                    result = response.json()

                    st.success(
                        "Legal document generated successfully!"
                    )

                    st.session_state["document_type"] = result[
                        "document_type"
                    ]

                    st.session_state["document_content"] = result[
                        "content"
                    ]

                else:

                    try:
                        error_detail = response.json().get(
                            "detail",
                            "Unknown backend error.",
                        )
                    except Exception:
                        error_detail = response.text

                    st.error(
                        f"Backend error ({response.status_code}): "
                        f"{error_detail}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Could not connect to the LegalEaseAI backend. "
                    "Please make sure the FastAPI server is running."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "The document generation request timed out. "
                    "Please try again."
                )

            except Exception as exc:

                st.error(
                    f"Unexpected error: {exc}"
                )

# --------------------------------------------------
# Display generated document
# --------------------------------------------------

if "document_content" in st.session_state:

    st.divider()

    st.markdown(
        '<div class="section-title">Generated Document</div>',
        unsafe_allow_html=True,
    )

    document_content = st.session_state["document_content"]

    st.text_area(
        "Document Content",
        value=document_content,
        height=600,
    )

    # --------------------------------------------------
    # Download as TXT
    # --------------------------------------------------

    st.download_button(
        label="Download Document",
        data=document_content,
        file_name="LegalEaseAI_Document.txt",
        mime="text/plain",
        use_container_width=True,
    )

    st.info(
        "This document is an AI-generated draft. "
        "Please have it reviewed by a qualified legal professional "
        "before using it for legal purposes."
    )