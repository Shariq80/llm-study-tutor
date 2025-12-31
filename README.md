# LLM-Powered Study Tutor (Offline, RAG-Based)

An offline-first AI study assistant that answers questions, generates summaries,
and creates quizzes from user-uploaded PDFs using Retrieval-Augmented Generation (RAG).

## Features
- Upload PDF study notes or textbooks
- Semantic search using FAISS
- Offline LLM inference using Ollama (Mistral 7B)
- Study modes:
  - Question Answering
  - Summaries
  - Explain Like I'm 12 (ELI12)
  - Quiz Generation
- Transparent source chunk display
- Runs fully locally (no paid APIs)


## System Architecture

1. PDF text is extracted and split into overlapping chunks
2. Each chunk is converted into an embedding using Sentence Transformers
3. Embeddings are stored in a FAISS vector database
4. User questions are embedded and used to retrieve relevant chunks
5. Retrieved chunks are injected into a prompt
6. A local LLM (Mistral 7B via Ollama) generates grounded responses

## Tech Stack
- Python
- Streamlit
- FAISS
- sentence-transformers
- Ollama (Mistral 7B)
- Requests


## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

 - Ensure Ollama is running and the Mistral model is pulled:
 
    ```bash 
    ollama pull mistral
    ```

## Ethical Design
 - No external API or data-sharing
 - Answers are grounded in user-provided documents
 - Model explicityly says "I don't know" if context is missing

## Learning Outcomes
 - Retrieval-AUgmented Generation (RAG)
 - Vector Databases
 - Prompt Engineering
 - Offline LLM Deployment
 - Stateful Application Design
