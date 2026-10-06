import os

from dotenv import load_dotenv

from azure.core.credentials import AzureKeyCredential

from azure.search.documents import SearchClient

from azure.search.documents.indexes import SearchIndexClient

from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField
)


load_dotenv()


def get_search_client():

    endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    key = os.getenv("AZURE_SEARCH_KEY")
    index_name = os.getenv("AZURE_SEARCH_INDEX")

    if not endpoint:
        raise ValueError(
            "AZURE_SEARCH_ENDPOINT is missing"
        )

    if not key:
        raise ValueError(
            "AZURE_SEARCH_KEY is missing"
        )

    if not index_name:
        raise ValueError(
            "AZURE_SEARCH_INDEX is missing"
        )

    return SearchClient(
        endpoint=endpoint,
        index_name=index_name,
        credential=AzureKeyCredential(key)
    )


def create_search_index():

    endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    key = os.getenv("AZURE_SEARCH_KEY")
    index_name = os.getenv("AZURE_SEARCH_INDEX")

    index_client = SearchIndexClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    fields = [

        SimpleField(
            name="id",
            type="Edm.String",
            key=True
        ),

        SearchableField(
            name="content",
            type="Edm.String"
        ),

        SimpleField(
            name="source",
            type="Edm.String",
            filterable=True
        ),

        SimpleField(
            name="page",
            type="Edm.Int32",
            filterable=True
        )
    ]

    index = SearchIndex(
        name=index_name,
        fields=fields
    )

    index_client.create_or_update_index(index)


def upload_chunks(chunks):

    search_client = get_search_client()

    if not chunks:
        return False

    results = search_client.upload_documents(
        documents=chunks
    )

    return all(
        result.succeeded
        for result in results
    )


def search_documents(question, top=5):

    search_client = get_search_client()

    results = search_client.search(
        search_text=question,
        top=top
    )

    documents = []

    for result in results:

        documents.append({

            "content": result.get(
                "content",
                ""
            ),

            "source": result.get(
                "source",
                "Unknown"
            ),

            "page": result.get(
                "page",
                0
            ),

            "score": result.get(
                "@search.score",
                0
            )
        })

    return documents