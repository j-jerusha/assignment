---
# RFP Data Extraction Project

## Objective

## This project extracts structured information from Request for Proposal (RFP) documents in PDF and HTML formats. Using Language Models and vector search, it parses, interprets, and organizes RFP details into a predefined JSON structure.

## Features

- Supports multiple document formats: PDF and HTML
- Extracts structured data into JSON
- Uses LLMs (ChatGroq) with embeddings for context-aware information extraction
- Automatically handles missing or unspecified fields
- Saves output per RFP folder
---

## Predefined Fields

The program extracts the following fields:

- Bid Number
- Title
- Due Date
- Bid Submission Type
- Term of Bid
- Pre Bid Meeting
- Installation
- Bid Bond Requirement
- Delivery Date
- Payment Terms
- Any Additional Documentation Required
- MFG for Registration
- Contract or Cooperative to use
- Model_no
- Part_no
- Product
- contact_info (dict: Name, Email, Phone, Address)
- company_name
- Bid Summary
- Product Specification

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/j-jerusha/assignment.git
cd assignment
```

### 2. Create and activate virtual environment

#### For macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### For Windows

```bash
python3 -m venv .venv
.venv\Scripts\activate
```

---

### 3. Install dependencies

If you’re using **uv**:

```bash
uv sync
```

Or using **pip**:

```bash
pip install -r requirements.txt
```

### 4. Set environment variables

Create a `.env` file with the following:

```env
GROQ_API_KEY=<your_groq_api_key>
HF_TOKEN=<HF_access_token>
```

---

## Usage

1. Organize RFP documents into folders, e.g.:

```
assignment/
├─ Bid1/
│  ├─ document1.pdf
│  └─ document2.html
├─ Bid2/
│  └─ document3.pdf
```

2. Run the script:

```bash
python main.py
```

3. Extracted JSON files will be saved in the `output/` folder:

```
output/
├─ Bid1_extracted.json
├─ Bid2_extracted.json
```

---

## How It Works

1. **Load Documents:** PDFs and HTML files are loaded using `PyPDFLoader` and `UnstructuredHTMLLoader`.
2. **Vector Store Creation:** Documents are embedded using `HuggingFaceEmbeddings` and stored in FAISS for retrieval.
3. **Context Retrieval:** Relevant document sections are fetched with a retriever.
4. **LLM Extraction:** `ChatGroq` generates structured JSON based on the predefined fields.
5. **JSON Output:** Ensures all fields are present; missing data is marked as `"Not specified"`.

---

## Dependencies

- Python 3.10+
- `python-dotenv`
- `langchain_community`
- `langchain_huggingface`
- `langchain_groq`
- `FAISS` (CPU version recommended)

---

## Notes

- The system handles missing fields gracefully.
- Ensure API keys (GROQ) are correctly set in `.env`.
- Can be extended to additional document formats with minimal changes.

---

## Author

J Jerusha

---
