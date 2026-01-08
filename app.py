import streamlit as st
import tempfile
import os
from pdf_utils import extract_text_from_pdf, split_text_with_overlap, store_chunks_in_faiss, query_pdf_with_retrieval_qa
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

# Configure page settings
st.set_page_config(
    page_title="PDF Intelligent Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
with st.sidebar:
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
            <span class="material-symbols-rounded" style="font-size: 24px; color: #4F46E5;">tune</span>
            <h2 style="margin: 0; font-size: 20px;">Configuration</h2>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Theme Toggle
    theme_choice = st.radio("Appearance", ["Light", "Dark"], horizontal=True, label_visibility="collapsed")
    
    st.markdown("---")
    
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
            <span class="material-symbols-rounded" style="font-size: 20px;">cloud_upload</span>
            <span style="font-weight: 600;">Document Upload</span>
        </div>
        <p style="font-size: 14px; opacity: 0.8; margin-bottom: 15px;">Upload PDF documents to begin analysis.</p>
        """, 
        unsafe_allow_html=True
    )
    
    uploaded_files = st.file_uploader(
        "Choose PDF files", 
        type=["pdf"], 
        accept_multiple_files=True,
        help="Limit 200MB per file",
        label_visibility="collapsed"
    )
    
    if uploaded_files:
        st.markdown(
            f"""
            <div style="background-color: rgba(79, 70, 229, 0.1); color: #4F46E5; padding: 10px; border-radius: 6px; display: flex; align-items: center; gap: 8px; margin-top: 10px;">
                <span class="material-symbols-rounded" style="font-size: 18px;">check_circle</span>
                <span style="font-size: 14px; font-weight: 500;">{len(uploaded_files)} file(s) ready</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")
    
    st.markdown(
        """
        <div style="margin-top: 20px;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
                <span class="material-symbols-rounded" style="font-size: 20px;">support_agent</span>
                <span style="font-weight: 600;">Support</span>
            </div>
            <div style="background-color: rgba(0,0,0,0.05); padding: 12px; border-radius: 8px; border: 1px solid rgba(0,0,0,0.1);">
                <p style="font-size: 13px; margin: 0; opacity: 0.7;">Have questions?</p>
                <a href="mailto:hrgayle27@gmail.com" style="text-decoration: none; color: inherit; font-weight: 600; font-size: 14px; display: flex; align-items: center; gap: 5px; margin-top: 4px;">
                    <span class="material-symbols-rounded" style="font-size: 16px;">mail</span>
                    hrgayle27@gmail.com
                </a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Define CSS variables based on Theme
if theme_choice == "Light":
    # Professional Light Theme (Vercel/Linear inspired)
    bg_color = "#FFFFFF"
    text_color = "#111827"  # Gray 900
    secondary_text = "#6B7280" # Gray 500
    sidebar_bg = "#F9FAFB" # Gray 50
    card_bg = "#FFFFFF"
    border_color = "#E5E7EB" # Gray 200
    primary_color = "#000000" # Black primary buttons for high contrast professional look
    primary_text = "#FFFFFF"
    accent_color = "#4F46E5" # Indigo for icons
    input_bg = "#FFFFFF"
else:
    # Professional Dark Theme
    bg_color = "#0A0A0A" # Nearly black
    text_color = "#EDEDED"
    secondary_text = "#A1A1A1"
    sidebar_bg = "#000000"
    card_bg = "#171717"
    border_color = "#333333"
    primary_color = "#EDEDED" # White primary buttons
    primary_text = "#000000"
    accent_color = "#818CF8" # Indigo 400
    input_bg = "#171717"

# Inject Material Symbols & Custom CSS
st.markdown(
    f"""
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0" />
    <style>
    /* Global Font & Reset */
    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: {text_color};
    }}
    
    /* App Background */
    .stApp {{
        background-color: {bg_color};
    }}
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg};
        border-right: 1px solid {border_color};
    }}
    
    /* Headings */
    h1, h2, h3 {{
        color: {text_color} !important;
        font-weight: 600;
        letter-spacing: -0.02em;
    }}
    
    /* Text */
    p {{
        color: {text_color};
        line-height: 1.6;
    }}
    
    /* Buttons */
    .stButton > button {{
        background-color: {primary_color};
        color: {primary_text};
        border: 1px solid {primary_color};
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        transition: all 0.2s ease;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }}
    .stButton > button:hover {{
        opacity: 0.9;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-color: {primary_color};
        color: {primary_text};
    }}
    
    /* Input Fields */
    .stTextInput > div > div > input {{
        background-color: {input_bg};
        color: {text_color};
        border: 1px solid {border_color};
        border-radius: 8px;
        padding: 12px;
        transition: border-color 0.2s;
    }}
    .stTextInput > div > div > input:focus {{
        border-color: {accent_color};
        box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.2);
    }}
    
    /* Card/Answer Box */
    .result-card {{
        background-color: {card_bg};
        border: 1px solid {border_color};
        border-radius: 12px;
        padding: 24px;
        margin-top: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }}
    
    /* Material Icons */
    .material-symbols-rounded {{
        vertical-align: middle;
        user-select: none;
    }}
    
    /* Streamlit Components Adjustments */
    [data-testid="stFileUploader"] {{
        padding: 10px;
        border: 1px dashed {border_color};
        border-radius: 8px;
        background-color: {input_bg};
    }}
    
    hr {{
        margin: 20px 0;
        border-color: {border_color};
        opacity: 0.5;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Main Header
st.markdown(
    f"""
    <div style="text-align: center; margin-bottom: 40px; padding-top: 20px;">
        <div style="display: inline-flex; align-items: center; justify-content: center; width: 64px; height: 64px; background-color: {input_bg}; border: 1px solid {border_color}; border-radius: 16px; margin-bottom: 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
            <span class="material-symbols-rounded" style="font-size: 32px; color: {accent_color};">analytics</span>
        </div>
        <h1 style="margin-bottom: 10px; font-size: 2.5rem;">PDF Intelligent Analyzer</h1>
        <p style="color: {secondary_text}; font-size: 1.1rem; max-width: 600px; margin: 0 auto;">
            Unlock insights from your documents instantly. Upload a PDF and start asking questions.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns([1, 6])

with col2:
    # Input Section
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
            <span class="material-symbols-rounded" style="font-size: 20px; color: {accent_color};">search</span>
            <span style="font-weight: 500; color: {text_color};">Your Query</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    question = st.text_input(
        "Enter your query",
        placeholder="e.g., What are the key findings in the executive summary?",
        label_visibility="collapsed"
    )
    
    # Action Button with spacer
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    run_qa = st.button("Generate Analysis")

    answer = None

    if run_qa:
        if not uploaded_files:
            st.warning("⚠️ Please upload a PDF document in the sidebar first.")
        elif not question.strip():
            st.warning("⚠️ Please enter a valid question.")
        elif not groq_api_key:
            st.error("🚫 API Key is missing. Check your configuration.")
        else:
            with st.spinner("Analyzing document structure and content..."):
                temp_paths = []
                try:
                    all_text = ""
                    progress_bar = st.progress(0)
                    
                    for idx, uploaded_file in enumerate(uploaded_files):
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                            tmp_file.write(uploaded_file.read())
                            tmp_path = tmp_file.name
                            temp_paths.append(tmp_path)
                        text = extract_text_from_pdf(tmp_path)
                        all_text += text + "\n"
                        progress_bar.progress((idx + 1) / len(uploaded_files))
                    
                    if not all_text.strip():
                        st.error("❌ Could not extract text. The PDF might be scanned or empty.")
                    else:
                        chunks = split_text_with_overlap(all_text, chunk_size=500, overlap=100)
                        db = store_chunks_in_faiss(chunks)
                        answer = query_pdf_with_retrieval_qa(
                            question,
                            db,
                            groq_api_key=groq_api_key
                        )
                finally:
                    for path in temp_paths:
                        if os.path.exists(path):
                            os.remove(path)

    if answer:
        st.markdown(
            f"""
            <div class="result-card">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 16px; padding-bottom: 16px; border-bottom: 1px solid {border_color};">
                    <span class="material-symbols-rounded" style="font-size: 24px; color: {accent_color};">auto_awesome</span>
                    <h3 style="margin: 0; font-size: 18px;">Analysis Results</h3>
                </div>
                <div style="line-height: 1.7; font-size: 1.05rem;">
                    {answer}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
