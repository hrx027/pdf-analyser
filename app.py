import streamlit as st
import tempfile
import os
from pdf_utils import extract_text_from_pdf, split_text_with_overlap, store_chunks_in_faiss, query_pdf_with_retrieval_qa
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

st.set_page_config(page_title="PDF RAG with LangChain & FAISS")
st.title("PDF ANALYZER")

# Main UI
uploaded_files = st.file_uploader("Upload one or more PDFs", type=["pdf"], accept_multiple_files=True)
question = st.text_input("Enter your question about the PDF(s):")
run_qa = st.button("Submit")

answer = None

if run_qa:
    if not uploaded_files:
        st.warning("Please upload at least one PDF file.")
    elif not question.strip():
        st.warning("Please enter a question.")
    elif not groq_api_key:
        st.warning("Please add your GROQ_API_KEY to the .env file.")
    else:
        with st.spinner("Processing PDFs and running Q&A..."):
            temp_paths = []
            try:
                # Save all uploaded files to temp locations and extract text
                all_text = ""
                for uploaded_file in uploaded_files:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                        tmp_file.write(uploaded_file.read())
                        tmp_path = tmp_file.name
                        temp_paths.append(tmp_path)
                    text = extract_text_from_pdf(tmp_path)
                    all_text += text + "\n"
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
                    os.remove(path)

if answer:
    st.markdown("### Answer:")
    st.write(answer) 