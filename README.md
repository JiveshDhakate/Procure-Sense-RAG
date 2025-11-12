# Spear RAG – Multi-Agent RAG System for Supplier Quotation Analysis

**Spear RAG** is a modular, production-ready Retrieval-Augmented Generation (RAG) system built using:

- **FastAPI** (backend)
- **Streamlit** (frontend)
- **ChromaDB** (vector store)
- **LangChain + OpenAI** (LLM & agent logic)

The system enables flexible supplier offer analysis by uploading plain-text quotations, retrieving relevant chunks, scoring offers with custom heuristics, and generating LLM-based summaries.

---

### 🔧 Key Features

- Upload plain text quotations
- Perform semantic search with ChromaDB
- Multi-agent architecture (Extractor, Retriever, Evaluator, Summarizer)
- Score offers based on delivery time, unit price, and supplier risk
- Generate natural language summaries
- Accurate, explainable, and scalable decision-making for procurement teams


## 1. Installation and Setup

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (preferred for managing dependencies and virtual environments)
- Git (to clone the repository)
- Docker (optional, for containerized deployment)

---

### 1.1: Clone the Repository

```bash
git clone https://github.com/<your-username>/spear-rag.git
cd spear-rag
```
### 1.2 Set Up Python Environment with uv

```bash
uv venv
source .venv/bin/activate
uv add -r requirements.txt
```

This installs all required dependencies: FastAPI, LangChain, ChromaDB, OpenAI, etc.

---

### 1.3 Environment Variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your-openai-api-key
```

Add any other required environment variables if needed.

---

### 1.4 Start the Backend Server

```bash
uvicorn main:app --reload
```

Access FastAPI at: [http://localhost:8000](http://localhost:8000)

---

### 1.5 Start the Frontend (Streamlit)

```bash
cd frontend
streamlit run app.py
```

Access frontend UI at: [http://localhost:8501](http://localhost:8501)

---

### 1.6 Run via Docker Compose

Import `docker-compose.yml` file in the root folder:

```yaml
version: "3.9"

services:
  backend:
    build:
      context: ./app
      dockerfile: Dockerfile
    image: spear-rag-backend
    container_name: spear-rag-backend
    ports:
      - "8000:8000"
    env_file: .env
    restart: always
    volumes:
      - chromadb-data:/app/chroma_db  # Optional volume for persistence

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    image: spear-rag-frontend
    container_name: spear-rag-frontend
    ports:
      - "8501:8501"
    environment:
      - BACKEND_URL=http://backend:8000
    depends_on:
      - backend
    restart: always

volumes:
  chromadb-data:
```

Then run the full stack with:

```bash
docker-compose up --build
```


## 2. System Architecture and Data Flow

The Spear RAG system follows a clean, modular architecture with a multi-agent pipeline for processing supplier quotations.

---

### 2.1 High-Level Flow

1. **User uploads plain-text supplier quotations** via the Streamlit frontend (`/upload`).
2. **ExtractorAgent** parses and structures the raw text into offer records.
3. **Each offer is embedded and stored** in a ChromaDB vector store for semantic search.
4. **User submits a query** via the frontend (`/query`).
5. **RetrieverAgent** fetches relevant offers from ChromaDB using semantic similarity.
6. **EvaluatorAgent** ranks offers using a heuristic scoring strategy (unit price, delivery days, risk).
7. **SummarizerAgent** generates a natural language summary of the top results.
8. **Final output** (recommendation, reasoning, and evaluated offers) is returned to the frontend.

---

### 2.2 Agent Interaction Overview

```plaintext
[Streamlit UI]
     |
     | /upload
     v
[ExtractorAgent] ---> [ChromaDB Vector Store]
     |
     | /query
     v
[RetrieverAgent]
     |
     v
[EvaluatorAgent]
     |
     v
[SummarizerAgent]
     |
     v
[Streamlit UI (Response Display)]
```
---

### 2.3 Component Breakdown

#### Frontend (Streamlit)
- Provides an interactive UI for uploading supplier quotations and submitting user queries.
- Communicates with the backend via HTTP POST requests.

#### FastAPI Backend
- `POST /upload`: Receives raw supplier texts and triggers extraction and vector storage.
- `POST /query`: Accepts a query string and orchestrates retrieval, evaluation, and summarization.

#### Agents

- **ExtractorAgent**  
  Converts supplier quotation text into structured offer dictionaries (item, price, supplier, delivery, risk).

- **RetrieverAgent**  
  Uses OpenAI Embeddings and ChromaDB to find semantically relevant offers based on user queries.

- **EvaluatorAgent**  
  Scores offers using heuristics like:
  - Lower price
  - Faster delivery
  - Lower supplier risk
  Returns a ranked list and reason for the best offer.

- **SummarizerAgent**  
  Uses an LLM to generate a concise, human-re
---
## 2.4 Model Configuration

The Spear RAG system uses **OpenAI models** via the `langchain-openai` integration for both reasoning and semantic embeddings.  
All parameters are tuned for **accuracy, determinism, and explainable supplier analysis**.

---

### Model Configuration Summary

| Component | Model | Temperature | Role | Description |
|------------|--------|--------------|------|--------------|
| **LLM (EvaluatorAgent)** | gpt-4o | 0.0 | Reasoning | Generates structured supplier evaluation and reasoning |
| **LLM (SummarizerAgent)** | gpt-4o | 0.0 | Summarization | Produces natural language summaries for top supplier offers |
| **Embedding Model** | text-embedding-3-small | – | Retrieval | Converts supplier offers and queries into semantic embeddings |
| **Vector Store** | ChromaDB | – | Storage | Stores embeddings with DuckDB and Parquet persistence |

---

### Language Model (LLM)

| Parameter | Value |
|------------|--------|
| **Model name** | `gpt-4o` *(default)* |
| **Temperature** | `0.0` *(ensures deterministic and fact-consistent reasoning)* |
| **Max tokens** | `1500` *(adjustable depending on prompt length)* |
| **Purpose** | Used by `EvaluatorAgent` and `SummarizerAgent` for scoring, ranking, and generating final summaries. |

**Example (EvaluatorAgent initialization):**
```python
from langchain_openai import ChatOpenAI

self.llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.0
)
```

- The **EvaluatorAgent** uses this LLM to generate structured JSON reasoning for supplier ranking.  
- The **SummarizerAgent** uses it to produce a natural-language summary of results.

---

### Embedding Model

| Parameter | Value |
|------------|--------|
| **Model name** | `text-embedding-3-small` |
| **Dimensions** | 1536 |
| **Purpose** | Converts supplier offers and user queries into semantic vector representations for ChromaDB retrieval. |

**Example (RetrieverAgent initialization):**
```python
from langchain_openai import OpenAIEmbeddings

self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
```

Embeddings are created during the `/upload` process and stored persistently in **ChromaDB** under `./chroma_db/`.  
These vectors are reused during `/query` calls for similarity-based retrieval.

---

### Determinism and Reproducibility

All agents use a **temperature of 0.0** and consistent parameters to maintain repeatable, traceable results.  
This ensures that supplier evaluations remain stable and explainable, a key requirement for enterprise-grade procurement systems.
---

## 3. Agents

### 3.1 ExtractorAgent

The `ExtractorAgent` is the first step in the backend pipeline. It is triggered when a user uploads raw supplier quotation text via the `/upload` route.

---

### Purpose

To extract structured offer information from unstructured supplier text input. Each extracted offer becomes a dictionary containing:

- Supplier name
- Item name or description
- Unit price
- Delivery days
- Risk assessment (if any)

---

### Key Logic

- Uses regular expressions and simple NLP parsing to detect offer-like patterns.
- Splits input text line-by-line and attempts to extract numeric and keyword cues (e.g., "unit price", "delivery", "risk", etc.).
- Returns a list of structured offers (as dictionaries) ready to be embedded and stored in ChromaDB.

---

### Example Output Format

```python
[
    {
        "supplier": "Premier Metals",
        "item": "10mm steel bolt (SB-10)",
        "unit_price": 0.7,
        "delivery_days": 8,
        "risk_assessment": "High Risk (Major quality issues last year)"
    },
    {
        "supplier": "QuickFix",
        "item": "10mm steel bolt (SB-10)",
        "unit_price": 0.75,
        "delivery_days": 10,
        "risk_assessment": "Low Risk (95% on-time delivery)"
    }
]
```
### Integration

Called inside the `/upload` endpoint.

Each extracted offer is then converted into a text chunk with metadata and sent to ChromaDB for vector storage.

---

### File Reference

File: `app/agents/extractor.py`  
Class: `ExtractorAgent`

---
### 3.2 RetrieverAgent

The `RetrieverAgent` is responsible for fetching the most relevant supplier offers based on the user's query. It performs semantic search using OpenAI embeddings and ChromaDB.

---

### Purpose

To retrieve top-k semantically similar offers from the ChromaDB vector store based on the user’s query input.

---

### Key Logic

- Converts the user query into an embedding using OpenAI's embedding model.
- Performs a similarity search against the stored offer chunks in ChromaDB.
- Returns the most relevant offers with associated metadata (supplier, price, etc.).

---

### Example Retrieval

Given a query like:

```text
Find the best supplier for 10mm steel bolts under 1 dollar
```

The agent will return the top-matching embedded offer records, such as:

```python
[
    {
        "supplier": "QuickFix",
        "item": "10mm steel bolt (SB-10)",
        "unit_price": 0.75,
        "delivery_days": 10,
        "risk_assessment": "Low Risk"
    },
    ...
]
```

---

### Integration

- Called inside the `/query` endpoint.
- Works after embedding the input query.
- Passes retrieved offers to the EvaluatorAgent for scoring.

---

### File Reference

File: `app/agents/retriever.py`  
Class: `RetrieverAgent`

---
### 3.3 EvaluatorAgent

The `EvaluatorAgent` ranks the retrieved supplier offers based on business-specific heuristics such as price, delivery time, and risk. It optionally uses an LLM to explain its decision in structured format.

---

### Purpose

To score, rank, and select the most suitable supplier offer based on:

- Lowest unit price
- Shortest delivery time
- Lowest risk level

It also generates a structured reasoning output using OpenAI's GPT model.

---

### Key Logic

- Applies custom scoring logic to each retrieved offer.
- Filters offers if specific constraints are mentioned (e.g., "10mm bolt").
- Uses a prompt template to pass top offers to the LLM.
- The LLM returns:
  - Recommended supplier
  - Reason for recommendation
  - Score explanation for other top offers
  - Breakdown of priorities considered

---

### Example LLM Output

```json
{
  "supplier": "QuickFix",
  "reason": "Best balance of price, delivery, and supplier reliability.",
  "score_explanation": "Premier Metals had a slightly lower price but higher risk. QuickFix offered a safer option.",
  "priority_breakdown": "Priority was given to risk level and delivery days over minor price differences."
}
```

---

### Integration

- Called inside the `/query` endpoint after retrieval is complete.
- Receives the top-k retrieved offers and the user’s original query.
- Passes its structured output to the SummarizerAgent.

---

### File Reference

File: `app/agents/evaluator.py`  
Class: `EvaluatorAgent`

---
### 3.4 SummarizerAgent

The `SummarizerAgent` generates a concise, natural-language explanation of the final supplier recommendation. It wraps up the pipeline by transforming structured evaluation data into a user-friendly summary.

---

### Purpose

To convert the evaluator's structured response into a clear summary that can be displayed in the frontend for non-technical decision makers.

---

### Key Logic

- Accepts structured fields from the `EvaluatorAgent`:
  - `supplier`
  - `reason`
  - `score_explanation`
  - `priority_breakdown`
- Constructs a system prompt and sends the content to the OpenAI LLM.
- Returns a single text string with a brief, human-readable summary.

---

### Example Output

```text
The selected supplier for the 10mm steel bolts is QuickFix Industries. They offer the product (Product ID: SB-10) at a unit price of $0.75 for orders of 1,000 units or more, with a delivery time of 10 business days. Their payment terms are Net 45. QuickFix Industries is noted as a reliable supplier with a strong history of quality and a 95% on-time delivery rate. Additionally, they are currently running a promotion on their specialty fastening components.
```

---

### Integration

- Called inside the `/query` endpoint.
- Takes the LLM-structured evaluation and creates a final natural-language summary.
- The output is included in the API response to the frontend.

---

### File Reference

File: `app/agents/summarizer.py`  
Class: `SummarizerAgent`

---
## 4. API Routes

The backend provides two main POST endpoints using FastAPI:

---

### 4.1 POST /upload

This route is used to upload plain-text supplier quotations. It runs the full extraction and embedding pipeline and persists the offers into ChromaDB for later retrieval.

---

#### Request Body

```json
{
  "text": "QuickFix offers 10mm steel bolts at $0.75 per unit. Delivery in 10 days. Risk: Low Risk.\nPremier Metals offers the same bolts at $0.70, but with a higher risk."
}
```

---

#### Internal Flow

- Passes input text to `ExtractorAgent`.
- Extracted offers are chunked and stored in ChromaDB with metadata.
- Embeddings are generated using OpenAI Embeddings via LangChain.
- Each chunk is stored in a persistent vector store for later retrieval.

---

#### Response

```json
{
  "message": "Successfully stored 2 offers in ChromaDB."
}
```

---

### 4.2 POST /query

This route accepts a user query and returns a ranked supplier recommendation with reasoning and summarized insight.

---

#### Request Body

```json
{
  "query": "Find best supplier for 10mm bolts under 1 dollar"
}
```

---

#### Internal Flow

- The query is embedded and passed to `RetrieverAgent`.
- Top matches from ChromaDB are scored using `EvaluatorAgent`.
- Structured reasoning is passed to `SummarizerAgent`.
- Final response includes:
  - Recommendation
  - Reasoning
  - All evaluated offers

---

#### Response

```json
{
  "recommendation": "QuickFix Industries",
  "reasoning": "The chosen supplier for 10mm bolts is QuickFix Industries, offering the 10mm steel bolt (Product ID: SB-10) at a unit price of $0.75 for orders of 1,000 units or more. They have a delivery timeframe of 10 business days and standard payment terms of Net 45. QuickFix Industries is noted as a reliable supplier with a strong history of quality and a 95% on-time delivery rate.",
  "offers_evaluated": [
    {
      "supplier": "QuickFix Industries",
      "item": "10mm steel bolt (SB-10)",
      "unit_price": 0.75,
      "delivery_days": 10,
      "risk_assessment": "Low Risk (Reliable supplier, consistent on-time delivery)"
    },
    {
      "supplier": "Premier Metals",
      "item": "10mm steel bolt (SB-10)",
      "unit_price": 0.7,
      "delivery_days": 8,
      "risk_assessment": "High Risk (Major quality issues last year, be cautious)"
    },
    {
      "supplier": "EcoFast Supplies",
      "item": "6 mm alloy steel bolt (AS-06)",
      "unit_price": 0.84,
      "delivery_days": 7,
      "risk_assessment": "Unknown Risk (Insufficient data)"
    },
    {
      "supplier": "SteelPro Industrial",
      "item": "10 mm galvanized bolt (GB-10)",
      "unit_price": 0.74,
      "delivery_days": 12,
      "risk_assessment": "Low Risk (Reliable supplier, consistent on-time delivery)"
    },
    {
      "supplier": "TitanWorks Engineering",
      "item": "9 mm high-tensile bolt (HT-09)",
      "unit_price": 0.9,
      "delivery_days": 6,
      "risk_assessment": "Unknown Risk (Insufficient data)"
    }
  ]
}
```

---

Each response is designed to be frontend-friendly, allowing clean display of both detailed breakdown and plain-language recommendation.

## 5. Frontend Overview

The frontend is built using [Streamlit](https://streamlit.io/) and serves as a simple, user-friendly interface to interact with the Spear RAG backend.

---

### 5.1 Features

- Text input field for uploading supplier quotation text
- Query input field to ask procurement-related questions
- Displays:
  - Final supplier recommendation
  - Reasoning summary
  - Full list of evaluated offers

---

### 5.2 Pages

The Streamlit app typically contains two main pages:

1. **Upload Offers**
   - POSTs supplier text to `/upload`
   - Shows a success message when offers are added

2. **Query Offers**
   - POSTs user query to `/query`
   - Displays:
     - Summary explanation from the LLM
     - Top recommended supplier
     - List of all offers evaluated

---

### 5.3 Configuration

- The frontend uses the following environment variable:

```python
os.getenv("BACKEND_URL", "http://localhost:8000")
```

- This allows seamless switching between local dev and Docker-based deployments.

---

### 5.4 File Structure

The main frontend file is:

```bash
frontend/app.py
```

It contains the logic for both form submissions and displaying results from the backend.

---

### 5.5 Launching Frontend

To run the Streamlit app locally:

```bash
cd frontend
streamlit run app.py
```

The UI will be available at `http://localhost:8501`.

---

The frontend communicates with the backend using standard HTTP POST requests, enabling full decoupling between interface and business logic.


## 6. ChromaDB Usage and Flexibility

ChromaDB is used as the core vector store for semantic retrieval in Spear RAG. It allows fast and persistent access to embedded supplier offers, enabling scalable and flexible RAG pipelines.

---

### 6.1 Why ChromaDB?

- **Lightweight and local**: Uses DuckDB and Parquet under the hood. No external database required.
- **Persistent**: All vectors and metadata are stored in the local file system, allowing reload across server restarts.
- **Integrated with LangChain**: Easily plugged into LangChain workflows for both document storage and retrieval.
- **Flexible schemas**: Supports arbitrary metadata per document, useful for attaching supplier names, prices, and risks.

---

### 6.2 Initialization

Inside the `RetrieverAgent`, ChromaDB is initialized with:

```python
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

self.vectorstore = Chroma(
    embedding_function=OpenAIEmbeddings(),
    persist_directory="./chroma_db",  # Directory for saving the vector store
    collection_name="supplier_offers"
)
```

- The `persist_directory` ensures data survives reloads.
- The `collection_name` logically separates different use-cases (e.g., multiple policies or projects).

---

### 6.3 Adding Data to ChromaDB

During the `/upload` process:

1. Offers extracted by `ExtractorAgent` are converted to small text chunks.
2. Metadata (like supplier, price, delivery) is attached to each chunk.
3. Each chunk is embedded using `OpenAIEmbeddings` and stored in ChromaDB:

```python
vectorstore.add_documents(documents=docs)
vectorstore.persist()
```

---

### 6.4 Retrieving from ChromaDB

In the `/query` flow:

- The user query is embedded using the same embedding model.
- ChromaDB is queried for top-k similar vectors:

```python
retrieved_docs = vectorstore.similarity_search(query, k=3)
```

- Retrieved results include both content and metadata, which are passed to downstream agents.

### 6.5 Reusability, Independence, and Future Cloud Integration

---

#### Reusing the Same ChromaDB

- The vector store is persisted locally using `persist_directory="./chroma_db"`.
- This folder holds the DuckDB and Parquet files used by Chroma.
- On container or server restart, the same store is reused without needing to re-upload offers.

```python
self.vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=OpenAIEmbeddings(),
    collection_name="supplier_offers"
)
```

---

#### Volume Mounts in Docker for Persistence

To ensure ChromaDB persists across container restarts, we use a **Docker volume mount** in `docker-compose.yml`.

```yaml
services:
  backend:
    build:
      context: ./app
      dockerfile: Dockerfile
    image: spear-rag-backend
    container_name: spear-rag-backend
    ports:
      - "8000:8000"
    env_file: .env
    restart: always
    volumes:
      - chromadb-data:/app/chroma_db  # <--- Volume mount added

volumes:
  chromadb-data:
```

This creates a named volume (`chromadb-data`) and mounts it to the backend’s `./chroma_db` directory, ensuring:

- Chroma vector store is persisted independently of the container lifecycle
- The same vector data is available after container restart or rebuild

---

#### How It’s Made Independent

- All ChromaDB logic is encapsulated inside `RetrieverAgent` and the `/upload` route.
- The vector store is modular and does not rely on external services or databases.
- Each offer chunk includes rich metadata (supplier, price, etc.) so that it remains self-contained.

---

#### Future Cloud Deployment (e.g., AWS, GCP, Azure)

**Option 1: Mount Cloud Object Storage as a Volume**

- Use cloud-native FUSE tools to mount:
  - AWS S3 → `/mnt/chroma` via `s3fs`
  - Google Cloud Storage → `gcsfuse`
  - Azure Blob → `blobfuse`
- Change `persist_directory="/mnt/chroma"` in the code

**Option 2: Use External Vector DB**

Replace ChromaDB with a hosted vector store:
- Pinecone
- Weaviate
- Qdrant
- Milvus

LangChain supports these with minimal code changes via:

```python
from langchain.vectorstores import Pinecone
```

**Option 3: Hybrid Configuration via Environment Variables**

```env
VECTOR_STORE=chroma_local
# or
VECTOR_STORE=pinecone
```

In code:

```python
if VECTOR_STORE == "chroma_local":
    vectorstore = Chroma(...)
elif VECTOR_STORE == "pinecone":
    vectorstore = Pinecone(...)
```

---

This makes Spear RAG highly flexible for local dev, containerized deployments, and production-scale cloud RAG pipelines.
---
## 7. Project Folder Structure

The Spear RAG project is organized into modular folders for backend agents, route handlers, frontend UI, and unit tests. This supports clean development, maintainability, and extensibility.

```
spear-rag/
├── .venv/                         # Virtual environment (uv-based)
├── .env                           # Environment variables (e.g., OpenAI key)
├── .gitignore
├── .dockerignore
├── uv.lock
├── pyproject.toml
├── docker-compose.yml             # Dockerized backend + frontend orchestration
├── README.md                      # Full project documentation
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry point
│   ├── requirements.txt           # Backend dependencies
│   ├── Dockerfile                 # Backend-specific Dockerfile
│
│   ├── routes/                    # FastAPI endpoints
│   │   ├── __init__.py
│   │   ├── upload.py              # /upload route
│   │   ├── query.py               # /query route
│
│   ├── models/                    # Pydantic models and schemas
│   │   ├── models.py
│   │   └── schemas.py

├── chroma_db/                     # Vector store directory (ChromaDB)
│   └── chroma.sqlite3

├── frontend/
│   ├── Dockerfile                 # Frontend Docker container
│   ├── requirements.txt           # Streamlit dependencies
│   ├── Home.py                    # Streamlit Home Page
│   ├── pages/
│   │   ├── 1_Upload.py            # Upload form page
│   │   └── 2_Query.py             # Query form page

├── test/
│   ├── test_extractor.py
│   ├── test_evaluator.py
│   ├── test_retriver.py
│   ├── test_summarizer.py
```

---
### Key Design Principles

- `app/agents/`: Core logic for document extraction, retrieval, evaluation, and summarization
- `app/routes/`: Clean separation of upload/query API routes
- `chroma_db/`: Local persistent vector store for supplier embeddings
- `frontend/pages/`: Streamlit UI, modular by page (upload, query)
- `test/`: Agent-specific unit tests to ensure correctness

This structure supports clean modularization, reusabilit
                  # Environment variables (OpenAI key etc.)

---
## 8. Summary and Future Work

Spear RAG is a modular, end-to-end Retrieval-Augmented Generation (RAG) system designed for supplier quotation analysis. It integrates a multi-agent backend (Extractor, Retriever, Evaluator, Summarizer) with a simple Streamlit frontend and persistent ChromaDB-based vector storage.

---

### Highlights

- **Modular multi-agent architecture** for flexibility and scalability
- **FastAPI backend** for structured API development
- **Streamlit frontend** for easy interaction and testing
- **ChromaDB** for lightweight, persistent, and fast semantic search
- **LLM-powered reasoning** to explain supplier recommendations

---

### Future Improvements

1. **Agent Enhancements**
   - Use Named Entity Recognition (NER) for better extraction accuracy
   - Make Evaluator scoring customizable via config

2. **Vector Store Upgrades**
   - Add support for cloud-hosted vector DBs (Pinecone, Weaviate, etc.)
   - Enable per-project or per-user vector collections

3. **Frontend UI**
   - Add upload file support (.txt or .pdf)
   - Include per-offer highlights and comparison charts

4. **Security and Auth**
   - Add authentication to protect API routes
   - Store API keys securely via a secrets manager (e.g., AWS Secrets Manager)

5. **Deployment**
   - Deploy to AWS/GCP using Docker or serverless functions
   - Monitor latency and add caching for repeated queries

---
## 9. Examples Folder Overview

The `examples/` directory provides real-world demonstration files for testing and validating the Spear RAG system end-to-end.  
Each file corresponds to a specific phase of the pipeline — from ingestion to querying.

---

### Folder: `examples/`

```
examples/
├── 1_Ingest Quotations.md      # Sample supplier quotation texts for ingestion via /upload
├── 2_Queries.md                # Example user queries and expected responses for /query endpoint
```

---

### Usage Guide

1. **Ingest Quotations**
   - Open `examples/1_Ingest Quotations.md`
   - Copy the provided supplier quotation samples
   - Paste them into the frontend **Upload Offers** page (or POST to `/upload`)
   - This populates ChromaDB with supplier offer embeddings

2. **Run Example Queries**
   - Open `examples/2_Queries.md`
   - Use the listed queries (e.g., “Find the best supplier for 6mm hex nuts under 1 dollar”)
   - Enter these in the frontend **Query Offers** page (or POST to `/query`)
   - Observe the model reasoning, evaluation, and final summarized recommendation

---

### File Purpose Summary

| File | Description |
|------|--------------|
| **1_Ingest Quotations.md** | Contains formatted supplier quotation samples for testing the extractor and embedding process. |
| **2_Queries.md** | Includes ready-to-use user queries for testing retrieval, evaluation, and summarization accuracy. |

---

### Notes
- These markdown files are structured for quick testing without requiring CSV or JSON uploads.  
- You can modify them to include new suppliers, products, or query types as your RAG pipeline evolves.

---

Spear RAG demonstrates a production-ready framework for real-world RAG systems. Its modularity allows easy adaptation to other domains such as insurance documents, legal contracts, healthcare records, or customer reviews.

