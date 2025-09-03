# PDF RAG with LangChain, FAISS, PyPDF2, and Streamlit

This project allows you to upload PDF files, process them with LangChain, store and search embeddings using FAISS, and interact with the data through a Streamlit web interface.

## Setup Instructions

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone <your-repo-url>
   cd pdf_rag
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

## Project Structure
- `requirements.txt` — Python dependencies
- `app.py` — Main Streamlit application (to be created)

## Features
- Upload and process PDF files
- Generate embeddings with LangChain
- Store and search embeddings using FAISS
- Query your PDF data interactively via Streamlit

---

Feel free to extend this project with additional features or improvements! 