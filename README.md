# RFP Document Information Extraction System

A Python-based system that extracts structured information from RFP (Request for Proposals) documents using RAG (Retrieval Augmented Generation) and Google's Gemini LLM.

## Features

- **Multi-format Support**: Parses PDF and HTML documents
- **RAG Implementation**: Uses FAISS vector search with sentence transformers for efficient information retrieval
- **LLM-powered Extraction**: Leverages Google Gemini for intelligent structured data extraction
- **Structured Output**: Generates JSON files with standardized bid information

## Architecture

```
Document → Parse (PDF/HTML) → Chunk Text → Index with FAISS →
RAG Retrieval → Gemini Extraction → Structured JSON Output
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Google API Key for Gemini

### Setup

1. **Clone or download the project**

2. **Create a virtual environment (recommended)**

```bash
python -m venv assignment
source assignment/bin/activate  # On Windows: assignment\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

Required packages:

```txt
google-generativeai>=0.3.0
sentence-transformers>=2.2.0
faiss-cpu>=1.7.4
pdfplumber>=0.10.0
beautifulsoup4>=4.12.0
pydantic>=2.0.0
python-dotenv>=1.0.0
numpy>=1.24.0
tqdm>=4.65.0
```

4. **Configure API Key**

Create a `.env` file in the project root:

```bash
GOOGLE_API_KEY=your_gemini_api_key_here
```

Or set as environment variable:

```bash
export GOOGLE_API_KEY="your_gemini_api_key_here"  # Linux/Mac
set GOOGLE_API_KEY=your_gemini_api_key_here      # Windows
```

## Project Structure

```
assignment/
├── main.py                    # Main execution script
├── src/
│   ├── ingest.py             # PDF/HTML parsing
│   ├── chunk_index.py        # Text chunking and FAISS indexing
│   ├── extract_gemini.py     # Gemini-based extraction with RAG
│   ├── schema.py             # Pydantic schema for validation
│   └── utils.py              # Utility functions
├── Bid1/                     # Input folder for first bid
│   ├── *.pdf
│   └── *.html
├── Bid2/                     # Input folder for second bid
│   ├── *.pdf
│   └── *.html
├── outputs/                  # Generated JSON outputs
│   ├── Bid1/
│   └── Bid2/
├── .env                      # API keys (not in git)
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## Usage

### Basic Usage

Place your RFP documents in `Bid1/` and `Bid2/` folders, then run:

```bash
python main.py
```

### Expected Input

Supported file formats:

- PDF files (`.pdf`)
- HTML files (`.html`, `.htm`)

### Output Format

Each processed document generates a JSON file with the following structure:

```json
{
  "bid_number": "JA-207652",
  "title": "Student and Staff Computing Devices",
  "due_date": "2024-07-09",
  "bid_submission_type": "Electronic submission",
  "term_of_bid": "Contract term details",
  "pre_bid_meeting": "Meeting details",
  "installation": "Installation requirements",
  "bid_bond_requirement": "Bond details",
  "delivery_date": "Expected delivery date",
  "payment_terms": "Payment terms and conditions",
  "additional_documentation_required": "Form 1295; W-9; Insurance proof",
  "mfg_for_registration": "Manufacturer requirements",
  "contract_or_cooperative_to_use": "Contract details",
  "model_no": "Device model number",
  "part_no": "Part number",
  "product": "Product description",
  "contact_info": "Name: John Doe; Email: john@example.com; Phone: 555-1234",
  "bid_summary": "Brief summary of the bid",
  "product_specification": "Technical specifications"
}
```

Fields set to `null` when information is not found in the document.

## How It Works

### 1. Document Parsing (`ingest.py`)

- **PDF**: Uses `pdfplumber` to extract text from all pages
- **HTML**: Uses `BeautifulSoup` to parse and extract clean text

### 2. Text Chunking & Indexing (`chunk_index.py`)

- Splits text into overlapping chunks (400 words, 80-word overlap)
- Uses `sentence-transformers/all-MiniLM-L6-v2` for embeddings
- Builds FAISS index for efficient similarity search
- Returns a retriever function for RAG

### 3. RAG-based Extraction (`extract_gemini.py`)

- Retrieves relevant chunks using targeted queries
- Combines context for comprehensive coverage
- Sends context to Gemini with structured prompt
- Parses and validates JSON output

### 4. Schema Validation (`schema.py`)

- Pydantic models ensure data consistency
- Automatic type conversion (dict/list → string)
- Handles missing or malf
# assignment
# assignment
# assignment
# assignment
# assignment
