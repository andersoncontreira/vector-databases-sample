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


def get_openai_embedding(text, open_ai_client, model="text-embedding-3-small"):
    response = open_ai_client.embeddings.create(input=[text], model=model)
    embedding = response.data[0].embedding
    return embedding
