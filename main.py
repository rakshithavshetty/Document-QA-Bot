import streamlit as st

from utils.pdf_processor import (
    extract_text_from_pdf,
    create_document_chunks
)

from agents.search_agent import (
    create_search_index,
    upload_chunks,
    search_documents
)

from agents.answer_agent import (
    generate_answer
)


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(

    page_title="Document Q&A Bot",

    page_icon="📚",

    layout="wide"
)


# ==========================================
# TITLE
# ==========================================

st.title(
    "📚 Document Q&A Bot"
)

st.write(
    "Upload company policies, manuals, and guides "
    "and ask questions using natural language."
)


# ==========================================
# PDF UPLOAD
# ==========================================

st.subheader(
    "📄 Upload Document"
)


uploaded_file = st.file_uploader(

    "Choose a PDF file",

    type=["pdf"]
)


if uploaded_file is not None:

    st.success(
        f"{uploaded_file.name} uploaded successfully!"
    )

    # --------------------------------------
    # Extract PDF text
    # --------------------------------------

    pages = extract_text_from_pdf(
        uploaded_file
    )

    st.success(
        f"Successfully extracted "
        f"{len(pages)} pages."
    )

    # --------------------------------------
    # Create chunks
    # --------------------------------------

    document_chunks = create_document_chunks(

        pages,

        uploaded_file.name
    )

    st.info(
        f"Created {len(document_chunks)} "
        f"text chunks."
    )

    # --------------------------------------
    # View extracted text
    # --------------------------------------

    with st.expander(
        "View extracted document text"
    ):

        for page in pages:

            st.markdown(
                f"### Page {page['page']}"
            )

            st.write(
                page["text"]
            )

    # --------------------------------------
    # Index document
    # --------------------------------------

    if st.button(
        "📥 Upload & Index Document"
    ):

        try:

            with st.spinner(
                "Creating Azure AI Search index..."
            ):

                create_search_index()

            with st.spinner(
                "Uploading document..."
            ):

                success = upload_chunks(
                    document_chunks
                )

            if success:

                st.success(
                    f"{uploaded_file.name} "
                    "indexed successfully!"
                )

            else:

                st.error(
                    "The document could not "
                    "be indexed."
                )

        except Exception as e:

            st.error(
                f"Indexing error: {e}"
            )


# ==========================================
# QUESTION SECTION
# ==========================================

st.divider()

st.subheader(
    "💬 Ask a Question"
)


question = st.text_input(

    "Enter your question:",

    placeholder=(
        "Example: What are the benefits "
        "of the finance policy?"
    )
)


# ==========================================
# ASK BUTTON
# ==========================================

if st.button(
    "🔍 Ask Question"
):

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        try:

            # ------------------------------
            # Search Azure AI Search
            # ------------------------------

            with st.spinner(
                "Searching documents..."
            ):

                documents = search_documents(
                    question
                )

            if not documents:

                st.warning(
                    "I couldn't find relevant "
                    "information in the uploaded documents."
                )

            else:

                # --------------------------
                # Generate answer
                # --------------------------

                with st.spinner(
                    "Generating answer..."
                ):

                    answer = generate_answer(

                        question,

                        documents
                    )

                # --------------------------
                # Display answer
                # --------------------------

                st.subheader(
                    "🧠 Answer"
                )

                st.write(
                    answer
                )

                # --------------------------
                # Display sources
                # --------------------------

                st.subheader(
                    "📚 Sources"
                )

                shown_sources = set()

                for document in documents:

                    source_key = (

                        document["source"],

                        document["page"]

                    )

                    if source_key not in shown_sources:

                        st.write(

                            f"📄 "
                            f"{document['source']} "
                            f"— Page "
                            f"{document['page']}"

                        )

                        shown_sources.add(
                            source_key
                        )

        except Exception as e:

            st.error(
                f"Error: {e}"
            )