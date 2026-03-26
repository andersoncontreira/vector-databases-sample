import os

import pypdf


def read_pdf(file_path):
    content = []
    with open(file_path, 'rb') as file:
        # content = file.read()
        reader = pypdf.PdfReader(file)
        for page in reader.pages:
            content.append(page.extract_text())

    return "\n".join(content)


def load_data_from_directory(directory):
    # check if a directory exists
    if not os.path.exists(directory):
        raise ValueError(f"Directory '{directory}' does not exist.")

    data = []
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            file_path = os.path.join(directory, filename)
            # data.append((filename, read_pdf(file_path)))
            data.append({"id": filename, "text": read_pdf(file_path)})
        elif filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                data.append({"id": filename, "text": file.read()})
    return data

def split_text(text, chunk_size=1000, chunk_overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - chunk_overlap
    return chunks


def get_openai_embedding(text, openai_client, model="text-embedding-3-small"):
    response = openai_client.embeddings.create(input=[text], model=model)
    embedding = response.data[0].embedding
    return embedding


def generate_model_response(relevant_chunks, query, openai_client, model="gpt-5-nano"):
    # Isso ajuda a reduzir custo e ruído. Em RAG simples, muitas vezes mandar chunks demais piora a resposta em vez de melhorar.
    context = "\n\n".join(relevant_chunks[:5]).strip()

    if not context:
        return "I don't know based on the retrieved documents."

    system_prompt = (
        "You are a helpful assistant that answers questions only using the provided context. "
        "Do not invent facts. "
        "If the answer is not clearly supported by the context, say: "
        "'I don't know based on the retrieved documents.' "
        "Keep the answer concise, with a maximum of 3 sentences."
    )

    # improved prompt
    # system_prompt = (
    #     "You are a helpful assistant that answers questions using only the provided document context. "
    #     "The documents are articles about career development and IT topics. "
    #     "Do not add information that is not supported by the context. "
    #     "If the answer is incomplete or not present in the context, say: "
    #     "'I don't know based on the retrieved documents.' "
    #     "Be concise and answer in at most 3 sentences."
    # )

    user_prompt = (
        f"Question:\n{query}\n\n"
        f"Context:\n{context}\n\n"
        "Answer the question using only the context above."
    )

    # temperature=0.2 - Para esse caso, faz sentido uma saída mais estável e menos criativa. A API aceita parâmetros opcionais nesse endpoint, e controlar a variabilidade costuma ajudar em tarefas de resposta baseada em contexto.
    # openai.BadRequestError: Error code: 400 - {'error': {'message': "Unsupported value: 'temperature' does not support 0.2 with this model. Only the default (1) value is supported.", 'type': 'invalid_request_error', 'param': 'temperature', 'code': 'unsupported_value'}}
    response = openai_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        # temperature=0.2,
    )

    return response.choices[0].message.content


def generate_model_response_v2(relevant_chunks, query, openai_client, model="gpt-5-nano"):
    formatted_chunks = []
    for i, chunk in enumerate(relevant_chunks[:5], start=1):
        formatted_chunks.append(f"[Chunk {i}]\n{chunk}")

    context = "\n\n".join(formatted_chunks)

    system_prompt = (
        "You are a helpful assistant that answers questions using only the provided context. "
        "Do not invent facts. "
        "If the answer is not clearly supported, say: "
        "'I don't know based on the retrieved documents.' "
        "Keep the answer concise, with a maximum of 3 sentences. "
        "When possible, mention the chunk numbers that support the answer."
    )

    user_prompt = (
        f"Question:\n{query}\n\n"
        f"Context:\n{context}\n\n"
        "Answer using only the context above."
    )

    response = openai_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        # temperature=0.2,
    )

    return response.choices[0].message.content