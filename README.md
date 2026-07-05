# 🧠 MemoryOS — Personal AI Knowledge Base

**MemoryOS** is an AI-powered personal knowledge management system that allows users to upload documents, chat with their knowledge base, remember personal facts, and retrieve information using semantic search, keyword search, and conversational memory.

**🌐 Live Demo:** https://memory-os-delta.vercel.app/

> **Note:** The frontend is deployed permanently on Vercel. The backend runs locally and is exposed using **ngrok** for live demonstrations. If the backend is offline, the frontend will load but AI features will be unavailable.

---

# ✨ Features

* 📄 Upload PDF documents
* 🗑 Delete uploaded documents
* 🔍 Hybrid Search

  * Semantic Search (Sentence Transformers + ChromaDB)
  * BM25 Keyword Search
* 🧠 Personal Memory Engine

  * Remembers user facts
  * Retrieves relevant memories
* 💬 Multi-chat interface
* ⚡ Streaming AI responses
* 📝 Conversation summarization
* 📂 Document filtering
* 📚 Source citation support
* 🚀 Modern glassmorphism UI
* ☁ Frontend deployed on Vercel

---

# 🛠 Tech Stack

### Frontend

* Next.js 16
* React 19
* Tailwind CSS
* Framer Motion
* Axios

### Backend

* FastAPI
* Groq API (Llama 3.3 70B)
* Sentence Transformers
* ChromaDB
* BM25
* PyPDF
* Uvicorn

---

# 🏗 Architecture

```
User
   │
   ▼
Next.js Frontend
   │
   ▼
FastAPI Backend
   │
   ├── Memory Engine
   ├── Query Rewriter
   ├── Conversation Summary
   ├── Hybrid Search
   │      ├── ChromaDB
   │      └── BM25
   │
   ▼
Groq Llama-3.3-70B
```

---

# 🧠 AI Pipeline

1. User uploads PDFs.
2. Documents are parsed and chunked.
3. Chunks are embedded using Sentence Transformers.
4. Embeddings are stored in ChromaDB.
5. User asks a question.
6. Query is rewritten using conversation history.
7. Hybrid retrieval combines:

   * Semantic Search
   * BM25 Search
8. Personal memory is retrieved if relevant.
9. Conversation summary is injected.
10. Llama 3.3 generates the final response.
11. Sources are returned alongside the answer.

---

# 📂 Project Structure

```
backend/
│
├── app.py
├── ask_rag.py
├── vectorstore.py
├── hybrid_search.py
├── memory_store.py
├── ingest.py
├── document_loader.py
├── chunker.py
├── summary_store.py
├── uploads/
└── chroma_db/

frontend/
│
├── app/
├── components/
├── public/
└── package.json
```

---

# 🚀 Running Locally

### Clone Repository

```bash
git clone https://github.com/shubhbeniwal/ai-personal-knowledge-base.git

cd ai-personal-knowledge-base
```

---

## Backend

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

uvicorn app:app --reload
```

Backend runs on:

```
http://localhost:8000
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend runs on:

```
http://localhost:3000
```

---

# 🌍 Live Demo Setup

The frontend is hosted on **Vercel**.

For live demonstrations:

1. Start the FastAPI backend locally.
2. Expose it using ngrok:

```bash
ngrok http 8000
```

3. Replace the backend API URL in the frontend with the generated ngrok URL.

Example:

```
https://your-ngrok-url.ngrok-free.app
```

This allows the deployed frontend to communicate securely with the local backend.

---

# 📌 Current Capabilities

✅ PDF Upload

✅ Document Deletion

✅ Hybrid Search

✅ Semantic Search

✅ BM25 Retrieval

✅ Personal Memory

✅ Query Rewriting

✅ Conversation History

✅ Conversation Summarization

✅ Streaming Responses

✅ Multi-Chat Interface

✅ Source Citations

---

# 📈 Future Improvements

* User Authentication
* Cloud Database
* Persistent Online Backend
* Multi-user Support
* Image & OCR Support
* Voice Conversations
* RAG Evaluation Dashboard
* Agentic Tool Calling
* Dockerized Production Deployment
* Kubernetes Deployment
* CI/CD Pipeline

---

# 👨‍💻 About the Creator

**Shubh Beniwal**

AI Engineer | Software Developer

Passionate about AI, LLMs, NLP, Retrieval-Augmented Generation (RAG), and Intelligent Systems.

* Portfolio: https://shubhbeniwal.lovable.app/
* GitHub: https://github.com/shubhbeniwal
* LinkedIn: https://www.linkedin.com/in/shubh-beniwal/

---

# ⭐ If you found this project interesting, consider giving it a star!
