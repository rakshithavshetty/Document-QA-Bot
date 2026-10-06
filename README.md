# 📚 Document Q&A Bot

A simple AI-powered **Document Question & Answer application** built with **Python, Streamlit, Azure AI Search, and Azure OpenAI**.

The application allows users to upload PDF documents such as company policies, manuals, and guides. The PDF text is extracted, divided into smaller chunks, indexed in Azure AI Search, and then retrieved when the user asks a question. Azure OpenAI generates the final answer using only the retrieved document content.

## ✨ Features

- 📄 Upload PDF documents through a Streamlit interface
- 🔍 Extract text from PDF pages
- ✂️ Split documents into searchable text chunks
- ☁️ Store and search document chunks using Azure AI Search
- 🤖 Generate answers using Azure OpenAI
- 💬 Ask questions using natural language
- 📑 Display document source and page information
- 🔐 Keep Azure credentials in a local `.env` file

## 🏗️ Architecture

```text
                  ┌──────────────────────┐
                  │      User uploads     │
                  │        PDF file       │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │   PDF Text Extraction│
                  │        pypdf         │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │   Text Chunking      │
                  │  800 chars / overlap │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │   Azure AI Search    │
                  │   Document Index     │
                  └──────────┬───────────┘
                             │
                      User asks question
                             │
                             ▼
                  ┌──────────────────────┐
                  │   Azure AI Search    │
                  │ Retrieve top results │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │     Azure OpenAI     │
                  │ Generate grounded    │
                  │       answer        │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │      Answer shown    │
                  │     in Streamlit     │
                  └──────────────────────┘
```

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| Streamlit | Web user interface |
| pypdf | PDF text extraction |
| Azure AI Search | Document indexing and search |
| Azure OpenAI | Natural-language answer generation |
| OpenAI Python SDK | Azure OpenAI API communication |
| python-dotenv | Loading environment variables |

## 📁 Project Structure

```text
Document-QA-Bot/
│
├── agents/
│   ├── answer_agent.py       # Generates answers with Azure OpenAI
│   └── search_agent.py       # Creates index, uploads and searches documents
│
├── utils/
│   └── pdf_processor.py      # Extracts and chunks PDF text
│
├── main.py                   # Streamlit application
├── requirements.txt          # Python dependencies
├── .env                      # Azure configuration - DO NOT COMMIT
├── .gitignore                # Git ignore rules
└── README.md                 # Project documentation
```

## ⚙️ Prerequisites

Before running the project, install or configure:

1. Python 3.10 or later
2. An Azure subscription
3. An Azure OpenAI resource/deployment
4. An Azure AI Search service
5. An Azure AI Search **admin API key**

## 🚀 Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Document-QA-Bot
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 🔐 Environment Variables

Create a `.env` file in the project root.

```env
AZURE_OPENAI_ENDPOINT=https://YOUR-AZURE-OPENAI-RESOURCE.openai.azure.com
AZURE_OPENAI_KEY=YOUR_AZURE_OPENAI_KEY
AZURE_OPENAI_DEPLOYMENT=YOUR_MODEL_DEPLOYMENT_NAME

AZURE_SEARCH_ENDPOINT=https://YOUR-SEARCH-SERVICE.search.windows.net
AZURE_SEARCH_KEY=YOUR_AZURE_SEARCH_ADMIN_KEY
AZURE_SEARCH_INDEX=internpdfs
```

### Important

Never commit `.env` to GitHub. The `.gitignore` file already contains:

```text
.env
```

If an Azure API key has accidentally been exposed, regenerate/rotate the key in Azure and update your `.env` file.

## ▶️ Run the Application

Start Streamlit with:

```bash
streamlit run main.py
```

The application will open in your browser.

If the browser does not open automatically, Streamlit normally displays a local address such as:

```text
http://localhost:8501
```

## 📄 How to Use

### Step 1 — Upload a PDF

Select a PDF such as:

```text
HR_Policy.pdf
```

The application extracts the text from the PDF.

### Step 2 — Create chunks

The extracted text is divided into smaller overlapping chunks so that Azure AI Search can efficiently index and retrieve relevant content.

The current chunking configuration is approximately:

```text
Chunk size: 800 characters
Overlap:     100 characters
```

### Step 3 — Index the document

Click:

```text
📥 Upload & Index Document
```

The application creates or updates the Azure AI Search index and uploads the document chunks.

### Step 4 — Ask a question

Enter a question such as:

```text
What is the leave policy?
```

or:

```text
What are the benefits mentioned in the HR policy?
```

The application searches Azure AI Search for the most relevant chunks and sends those results to Azure OpenAI.

## 🔎 How Question Answering Works

The application follows a basic Retrieval-Augmented Generation (RAG) workflow:

1. User uploads a document.
2. PDF text is extracted.
3. Text is split into chunks.
4. Chunks are uploaded to Azure AI Search.
5. User asks a question.
6. Azure AI Search retrieves the most relevant chunks.
7. Retrieved content is passed to Azure OpenAI.
8. Azure OpenAI generates an answer based only on the retrieved document context.
9. The answer is displayed to the user.

## 🧩 Main Components

### `utils/pdf_processor.py`

Responsible for:

- Reading PDF files
- Extracting text from each page
- Splitting text into chunks
- Creating document records containing:
  - `id`
  - `content`
  - `source`
  - `page`

### `agents/search_agent.py`

Responsible for Azure AI Search operations:

- Creating the search index
- Uploading document chunks
- Searching indexed documents
- Returning relevant documents

### `agents/answer_agent.py`

Responsible for Azure OpenAI operations.

It receives:

```text
User Question + Retrieved Document Context
```

and generates an answer using the configured Azure OpenAI deployment.

### `main.py`

Provides the Streamlit user interface and connects all components together.

## ❗ Troubleshooting

### Error: API key doesn't match service's internal, primary or secondary keys

Example:

```text
The given API key doesn't match service's internal,
primary or secondary keys.
```

This normally means that `AZURE_SEARCH_KEY` is incorrect, expired/rotated, copied incorrectly, or belongs to a different Azure AI Search service.

Check:

```env
AZURE_SEARCH_ENDPOINT=https://YOUR-SEARCH-SERVICE.search.windows.net
AZURE_SEARCH_KEY=YOUR_CURRENT_ADMIN_KEY
```

In Azure Portal:

```text
Azure AI Search service
        ↓
Settings
        ↓
Keys
        ↓
Copy Primary or Secondary ADMIN key
```

Make sure the key belongs to the same Search service specified by `AZURE_SEARCH_ENDPOINT`.

After changing `.env`, stop and restart Streamlit:

```bash
Ctrl + C
streamlit run main.py
```

### Error: `AZURE_SEARCH_KEY is missing`

Make sure `.env` contains:

```env
AZURE_SEARCH_KEY=YOUR_KEY
```

Also make sure `.env` is located in the project root, next to `main.py`.

### Error: `AZURE_OPENAI_KEY is missing`

Add the Azure OpenAI credentials to `.env`:

```env
AZURE_OPENAI_ENDPOINT=YOUR_ENDPOINT
AZURE_OPENAI_KEY=YOUR_KEY
AZURE_OPENAI_DEPLOYMENT=YOUR_DEPLOYMENT_NAME
```

Then restart Streamlit.

### Search works but no answer is generated

Check:

- Azure OpenAI endpoint
- Azure OpenAI API key
- Deployment name
- Azure OpenAI model availability
- Internet connectivity

## 🔒 Security Best Practices

- Never upload `.env` to GitHub.
- Never place Azure API keys directly in Python source code.
- Use environment variables or a secure secret-management service.
- Rotate exposed API keys immediately.
- Use the minimum permissions necessary for production applications.
- Do not upload confidential company documents to public repositories.

## 📌 Example Questions

For an HR policy document, you can ask:

```text
What is the leave policy?
```

```text
How many days of annual leave are provided?
```

```text
What is the work-from-home policy?
```

```text
What benefits are available to employees?
```

```text
What is the company's notice period?
```

The answer should be based on the information retrieved from the uploaded document.

## 🎯 Project Objective

The goal of this project is to demonstrate how **Retrieval-Augmented Generation (RAG)** can be used to build an enterprise document assistant that allows users to search and ask questions about internal documents using natural language.

## 🔮 Future Improvements

Possible enhancements include:

- Multiple-document support
- Chat history
- Conversation memory
- Hybrid/vector search
- Semantic ranking
- Document deletion
- User authentication
- Role-based access control
- Citation links to document pages
- Support for DOCX and TXT files
- Azure Blob Storage integration
- Production deployment using Azure services
- Improved chunking and metadata filtering

## 👩‍💻 Author

**Rakshitha Shetty**

Computer Science Engineering Graduate

---

⭐ If you find this project useful, consider giving the repository a star.
