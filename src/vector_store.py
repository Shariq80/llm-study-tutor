import faiss
import numpy as np

def create_faiss_index(embeddings):
    """
    Creates a FAISS index from embeddings.
    """
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype("float32"))
    return index

def search_index(index, query_embedding, k=5):
    """
    Searches the FAISS index.
    """
    distances, indices = index.search(
        np.array([query_embedding]).astype("float32"),
        k
    )
    return indices[0]