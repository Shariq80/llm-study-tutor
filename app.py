import streamlit as st
import os
import hashlib

from src.pdf_loader import extract_text_from_pdf
from src.text_splitter import split_text
from src.embeddings import load_embedding_model, create_embeddings
from src.vector_store import create_faiss_index, search_index
from src.prompts import build_prompt
from src.rag import generate_answer

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ---------- Utilities ----------
def file_hash(file_bytes):
    return hashlib.md5(file_bytes).hexdigest()


# ---------- Session State Init ----------
if "embed_model" not in st.session_state:
    st.session_state.embed_model = None

if "faiss_index" not in st.session_state:
    st.session_state.faiss_index = None

if "chunks" not in st.session_state:
    st.session_state.chunks = None

if "file_hash" not in st.session_state:
    st.session_state.file_hash = None


# ---------- UI ----------
st.title("LLM-Powered Study Tutor")
uploaded_file = st.file_uploader("Upload your study PDF", type=["pdf"])


# ---------- Load Embedding Model Once ----------
if st.session_state.embed_model is None:
    st.session_state.embed_model = load_embedding_model()

embed_model = st.session_state.embed_model


# ---------- PDF Handling ----------
if uploaded_file is not None:
    file_bytes = uploaded_file.getvalue()
    current_hash = file_hash(file_bytes)

    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(file_bytes)

    # Rebuild index only if new file
    if st.session_state.file_hash != current_hash:
        with st.spinner("Processing document..."):
            extracted_text = extract_text_from_pdf(file_path)
            chunks = split_text(extracted_text)
            embeddings = create_embeddings(embed_model, chunks)
            index = create_faiss_index(embeddings)

        st.session_state.chunks = chunks
        st.session_state.faiss_index = index
        st.session_state.file_hash = current_hash

        st.success("Document indexed successfully!")
    else:
        chunks = st.session_state.chunks
        index = st.session_state.faiss_index

    st.write(f"Total chunks: {len(chunks)}")

    # ---------- Question Answering ----------
    st.subheader("Ask a question")
    question = st.text_input("Enter your question")

    mode = st.selectbox(
        "Study mode",
        ["default", "summary", "eli12", "quiz"]
    )

    if question.strip():
        query_embedding = embed_model.encode(question)
        top_indices = search_index(index, query_embedding, k=3)
        retrieved_chunks = [chunks[i] for i in top_indices]

        if not retrieved_chunks:
            st.error("No relevant content found in the document.")
            st.stop()

        context = "\n\n".join(retrieved_chunks)
        prompt = build_prompt(context, question, mode)

        with st.spinner("Thinking..."):
            answer = generate_answer(prompt)

        st.markdown("### Answer")
        st.write(answer)

        with st.expander("Retrieved Study Chunks"):
            for i, chunk in enumerate(retrieved_chunks, 1):
                st.markdown(f"**Chunk {i}:**")
                st.write(chunk[:500] + "...")
