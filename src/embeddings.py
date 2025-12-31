from sentence_transformers import SentenceTransformer

def load_embedding_model():
    """
    Loads a lightweight embedding model.
    """
    return SentenceTransformer("all-MiniLM-L6-v2")

def create_embeddings(model, chunks: list):
    """
    Converts text chunks into embeddings.
    """
    return model.encode(chunks)