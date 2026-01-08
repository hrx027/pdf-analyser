# PDF Analyzer - RAG Application

A **Retrieval-Augmented Generation (RAG)** application that enables users to upload PDF documents and ask questions about their content using natural language. Built with LangChain, FAISS, and Streamlit, this tool demonstrates a complete end-to-end RAG pipeline for document Q&A.

## 🎯 Project Overview

This application implements a production-ready RAG system that:
- Extracts text from PDF documents
- Creates semantic embeddings and stores them in a vector database
- Retrieves relevant context based on user queries
- Generates accurate answers using a Large Language Model (LLM)

**Perfect for:** Document analysis, research assistance, knowledge base Q&A, and demonstrating RAG architecture in interviews.

## 🏗️ Architecture & Tech Stack

### Core Technologies
- **LangChain**: Orchestrates the RAG pipeline (text splitting, embeddings, retrieval, QA chain)
- **FAISS**: Vector database for efficient similarity search
- **HuggingFace Embeddings**: `sentence-transformers/all-MiniLM-L6-v2` for semantic embeddings
- **Groq LLM**: `llama3-70b-8192` for answer generation (fast inference API)
- **Streamlit**: Interactive web interface
- **PyPDF2**: PDF text extraction

### How It Works

```
PDF Upload → Text Extraction → Chunking (with overlap) → Embedding Generation 
→ FAISS Vector Store → Query Embedding → Similarity Search → Context Retrieval 
→ LLM Answer Generation → Display Result
```

1. **Document Processing**: PDFs are parsed and text is extracted from all pages
2. **Text Chunking**: Text is split into overlapping chunks (500 chars, 100 char overlap) to preserve context
3. **Embedding**: Each chunk is converted to a vector using HuggingFace sentence transformers
4. **Vector Storage**: Embeddings are stored in FAISS for fast similarity search
5. **Query Processing**: User questions are embedded and matched against stored vectors
6. **Retrieval**: Most relevant chunks are retrieved based on semantic similarity
7. **Generation**: LangChain's RetrievalQA chain uses retrieved context + LLM to generate answers

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Groq API key ([Get one here](https://console.groq.com/))

### Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd pdf-analyzer
   ```

2. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. **Run the application:**
   ```bash
   streamlit run app.py
   ```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
pdf-analyzer/
├── app.py              # Streamlit web application (UI & orchestration)
├── pdf_utils.py        # Core RAG functions (extraction, chunking, embedding, QA)
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## ✨ Key Features

- **Multi-PDF Support**: Upload and query multiple PDFs simultaneously
- **Semantic Search**: Uses vector embeddings for contextually relevant retrieval
- **Overlapping Chunks**: Preserves context across document boundaries
- **Fast Inference**: Leverages Groq's high-speed LLM API
- **Interactive UI**: Clean Streamlit interface for easy document Q&A
- **Production-Ready**: Error handling, temp file management, and user feedback

## 🔧 Technical Highlights

### Why This Architecture?

- **FAISS**: Industry-standard vector database for scalable similarity search
- **Overlapping Chunks**: Prevents information loss at chunk boundaries
- **RetrievalQA Chain**: LangChain's proven pattern for RAG applications
- **HuggingFace Embeddings**: Open-source, efficient, and well-supported
- **Groq LLM**: Fast inference with high-quality models (Llama3-70b)

### Design Decisions

- **Chunk Size (500)**: Balances context preservation with retrieval precision
- **Overlap (100)**: Ensures continuity between adjacent chunks
- **Temperature (0.0)**: Deterministic, factual responses for document Q&A
- **"Stuff" Chain Type**: Simple and effective for moderate document sizes

## 📝 Usage Example

1. Upload one or more PDF files using the file uploader
2. Enter your question in the text input (e.g., "What are the main findings?")
3. Click "Submit" to process
4. View the AI-generated answer based on your PDF content

## 🎓 Interview Talking Points

- **RAG Pipeline**: Demonstrates understanding of retrieval-augmented generation
- **Vector Databases**: Experience with FAISS and semantic search
- **LangChain**: Proficiency with LLM orchestration frameworks
- **End-to-End Development**: Full-stack implementation from PDF parsing to answer generation
- **Production Considerations**: Error handling, API key management, temp file cleanup

## 🔮 Potential Enhancements

- Support for additional file formats (DOCX, TXT, etc.)
- Persistent vector store (save/load FAISS indexes)
- Chat history and conversation context
- Multiple embedding model options
- Advanced retrieval strategies (reranking, hybrid search)
- User authentication and document management

---

**Built with ❤️ using LangChain, FAISS, and Streamlit** 