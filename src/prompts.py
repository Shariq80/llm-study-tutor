def build_prompt(context: str, question: str, mode: str = "default") -> str:
    """
    Builds a RAG prompt for the LLM.
    """
    if mode == "eli12":
        instruction = (
            "Explain the answer like I am 12 year old."
            "Use simple language, short sentences, and examples."
            )
    elif mode == "quiz":
        instruction = (
            "Create 3 3 quiz questions based on the context."
            "Provide the correct answer after each question."
            )
    elif mode == "summary":
        instruction = (
            "Summarize the context clearly in bullet points."
            "Focus on key ideas and definitions."
        )
    else:
        instruction = (
            "Answer the question using only the given context."
            "Be concise and accurate."
            )

    return f"""
You are a helpful AI study tutor.

Rules:
 - Use ONLY the information in the context
 - If the answer is not present, say "I don't know"
Context: {context}
Question: {question}
Instruction: {instruction}
Answer:
"""
