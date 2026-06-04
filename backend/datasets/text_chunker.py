def split_text_into_chunks(text, chunk_size=3000):

    chunks = []

    start = 0

    while start < len(text):

        chunk = text[start:start + chunk_size]

        chunks.append(chunk)

        start += chunk_size

    return chunks