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

# Custom CSS for professional styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .css-1d391kg {
        padding-top: 2rem;
    }
    h1 {
        color: #1e1e1e;
        font-family: 'Helvetica Neue', sans-serif;
    }
    h2, h3 {
        color: #333;
    }
    .upload-text {
        font-size: 1.1rem;
        font-weight: 500;
        color: #555;
        margin-bottom: 10px;
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #ddd;
        padding: 10px;
    }
    .answer-box {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border-left: 5px solid #4CAF50;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>📄 PDF Intelligent Analyzer</h1>", unsafe_allow_html=True)

# Sidebar for File Upload
with st.sidebar:
    st.markdown("### 📂 Document Upload")
    st.markdown("<p class='upload-text'>Upload your PDF documents here to begin analysis.</p>", unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Choose PDF files", 
        type=["pdf"], 
        accept_multiple_files=True,
        help="Limit 200MB per file"
    )
    
    st.markdown("---")

    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded")

# Main Content Area
col1, col2 = st.columns([1, 6])

with col2:
    st.markdown("### 💬 Ask a Question")
    question = st.text_input(
        "What would you like to know about your documents?",
        placeholder="e.g., What are the key findings in this report?"
    )
    
    run_qa = st.button("🔍 Analyze & Answer")

    answer = None

    if run_qa:
        if not uploaded_files:
            st.warning("⚠️ Please upload at least one PDF file in the sidebar to proceed.")
        elif not question.strip():
            st.warning("⚠️ Please enter a valid question.")
        elif not groq_api_key:
            st.error("🚫 GROQ_API_KEY is missing. Please check your .env file.")
        else:
            with st.spinner("🔄 Processing documents and generating answer..."):
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
                        st.error("❌ No extractable text found in the uploaded PDF(s).")
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
                        os.remove(path)

    if answer:
        st.markdown("---")
        st.markdown("### 💡 AI Response")
        st.markdown(f"<div class='answer-box'>{answer}</div>", unsafe_allow_html=True)
