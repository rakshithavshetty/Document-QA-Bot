from pypdf import PdfReader


def extract_text_from_pdf(uploaded_file):
    """
    Extract text from every page of the uploaded PDF.
    """

    reader = PdfReader(uploaded_file)

    pages = []

    for page_number, page in enumerate(
        reader.pages,
        start=1
    ):

        text = page.extract_text()

        if text and text.strip():

            pages.append({
                "page": page_number,
                "text": text.strip()
            })

    return pages


def chunk_text(
    text,
    chunk_size=800,
    overlap=100
):
    """
    Split text into smaller overlapping chunks.
    """

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def create_document_chunks(
    pages,
    filename
):
    """
    Create searchable chunks.

    Azure AI Search document IDs cannot contain
    characters such as '.' so we remove the
    file extension from the ID.
    """

    document_chunks = []

    # Remove .pdf from filename

    clean_filename = filename

    if clean_filename.lower().endswith(".pdf"):

        clean_filename = clean_filename[:-4]

    # Replace unsafe characters

    clean_filename = (
        clean_filename
        .replace(" ", "_")
        .replace(".", "_")
        .replace("/", "_")
        .replace("\\", "_")
    )

    chunk_number = 1

    for page in pages:

        chunks = chunk_text(
            page["text"]
        )

        for chunk in chunks:

            document_chunks.append({

                "id": (
                    f"{clean_filename}_"
                    f"{chunk_number}"
                ),

                "content": chunk,

                "source": filename,

                "page": page["page"]
            })

            chunk_number += 1

    return document_chunks