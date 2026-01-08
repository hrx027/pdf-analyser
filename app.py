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
    page_icon="graph",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
with st.sidebar:
    st.title("Settings")
    
    # Theme Toggle
    theme_choice = st.radio("Appearance Mode", ["Light", "Dark"], horizontal=True)
    
    st.divider()
    
    st.header("Document Upload")
    st.markdown("Upload your PDF documents here to begin analysis.")
    
    uploaded_files = st.file_uploader(
        "Choose PDF files", 
        type=["pdf"], 
        accept_multiple_files=True,
        help="Limit 200MB per file"
    )
    
    if uploaded_files:
        st.info(f"{len(uploaded_files)} file(s) uploaded successfully")

    st.divider()
    
    st.header("Contact & Feedback")
    st.markdown("For support or feedback, please reach out:")
    st.markdown("**hrgayle27@gmail.com**")

# Define CSS based on Theme
if theme_choice == "Light":
    primary_color = "#4F46E5"  # Indigo
    bg_color = "#FFFFFF"
    text_color = "#1F2937"  # Gray 800
    secondary_bg = "#F3F4F6" # Gray 100
    card_bg = "#FFFFFF"
    border_color = "#E5E7EB" # Gray 200
else:
    primary_color = "#6366F1" # Indigo 400
    bg_color = "#111827" # Gray 900
    text_color = "#F9FAFB" # Gray 50
    secondary_bg = "#1F2937" # Gray 800
    card_bg = "#1F2937"
    border_color = "#374151" # Gray 700

custom_css = f"""
    <style>
    /* Main Background */
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    
    /* Headings */
    h1, h2, h3, h4, h5, h6 {{
        color: {text_color} !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    /* Text */
    p, .stMarkdown, .stText {{
        color: {text_color} !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    /* Buttons */
    .stButton>button {{
        background-color: {primary_color};
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        width: 100%;
        transition: opacity 0.2s;
    }}
    .stButton>button:hover {{
        opacity: 0.9;
    }}
    
    /* Input Fields */
    .stTextInput>div>div>input {{
        background-color: {card_bg};
        color: {text_color};
        border: 1px solid {border_color};
        border-radius: 8px;
        padding: 10px;
    }}
    
    /* Answer Box */
    .answer-box {{
        background-color: {card_bg};
        border: 1px solid {border_color};
        border-radius: 12px;
        padding: 24px;
        margin-top: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        color: {text_color};
    }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {secondary_bg};
        border-right: 1px solid {border_color};
    }}
    
    /* Success/Warning Messages */
    .stAlert {{
        border-radius: 8px;
    }}
    </style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Main Content
st.markdown("<h1 style='text-align: center; margin-bottom: 1rem;'>PDF Intelligent Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-bottom: 3rem; opacity: 0.8;'>Upload documents and ask questions to extract insights instantly.</p>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 6])

with col2:
    st.subheader("Ask a Question")
    question = st.text_input(
        "Enter your query",
        placeholder="What are the key financial metrics mentioned?",
        label_visibility="collapsed"
    )
    
    run_qa = st.button("Analyze Document")

    answer = None

    if run_qa:
        if not uploaded_files:
            st.warning("Please upload at least one PDF file in the sidebar to proceed.")
        elif not question.strip():
            st.warning("Please enter a valid question.")
        elif not groq_api_key:
            st.error("API Key is missing. Please check your configuration.")
        else:
            with st.spinner("Analyzing documents..."):
                temp_paths = []
                try:
                    # Save all uploaded files to temp locations and extract text
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
                        st.error("No extractable text found in the uploaded PDF(s).")
                    else:
                        # Split into chunks
                        chunks = split_text_with_overlap(all_text, chunk_size=500, overlap=100)
                        # Store in FAISS
                        db = store_chunks_in_faiss(chunks)
                        # Run Q&A
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
        st.markdown("### Analysis Result")
        st.markdown(f"<div class='answer-box'>{answer}</div>", unsafe_allow_html=True)
