import os

from dotenv import load_dotenv
from openai import OpenAI


# Load .env
load_dotenv()


AZURE_OPENAI_ENDPOINT = os.getenv(
    "AZURE_OPENAI_ENDPOINT"
)

AZURE_OPENAI_KEY = os.getenv(
    "AZURE_OPENAI_KEY"
)

AZURE_OPENAI_DEPLOYMENT = os.getenv(
    "AZURE_OPENAI_DEPLOYMENT"
)


# Debug checks
print("================================")
print("Azure OpenAI Configuration")
print("================================")

print(
    "Endpoint loaded:",
    bool(AZURE_OPENAI_ENDPOINT)
)

print(
    "API key loaded:",
    bool(AZURE_OPENAI_KEY)
)

print(
    "Deployment loaded:",
    bool(AZURE_OPENAI_DEPLOYMENT)
)

print("================================")


if not AZURE_OPENAI_ENDPOINT:
    raise ValueError(
        "AZURE_OPENAI_ENDPOINT is missing from .env"
    )


if not AZURE_OPENAI_KEY:
    raise ValueError(
        "AZURE_OPENAI_KEY is missing from .env"
    )


if not AZURE_OPENAI_DEPLOYMENT:
    raise ValueError(
        "AZURE_OPENAI_DEPLOYMENT is missing from .env"
    )


# Azure OpenAI v1 endpoint
client = OpenAI(

    api_key=AZURE_OPENAI_KEY,

    base_url=(
        AZURE_OPENAI_ENDPOINT.rstrip("/")
        + "/openai/v1/"
    )
)


def generate_answer(question, documents):

    if not documents:

        return (
            "I couldn't find this information "
            "in the uploaded documents."
        )


    context_parts = []


    for document in documents:

        context_parts.append(

            f"""
Source: {document['source']}
Page: {document['page']}

Content:
{document['content']}
"""
        )


    context = "\n\n".join(
        context_parts
    )


    prompt = f"""
You are an enterprise document
question-answering assistant.

Answer the question using ONLY the
information provided in the document context.

Do not use outside knowledge.
Do not invent information.

If the answer is not present in the
documents, say:

"I couldn't find this information
in the uploaded documents."

Question:

{question}

Document Context:

{context}
"""


    response = client.chat.completions.create(

        model=AZURE_OPENAI_DEPLOYMENT,

        messages=[

            {
                "role": "system",

                "content": (
                    "Answer questions using only "
                    "the provided documents."
                )
            },

            {
                "role": "user",

                "content": prompt
            }
        ],


    )


    return response.choices[0].message.content