import os
import json
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, UnstructuredHTMLLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Target fields to extract
FIELDS = [
    "Bid Number", "Title", "Due Date", "Bid Submission Type", "Term of Bid",
    "Pre Bid Meeting", "Installation", "Bid Bond Requirement", "Delivery Date",
    "Payment Terms", "Any Additional Documentation Required", "MFG for Registration",
    "Contract or Cooperative to use", "Model_no", "Part_no", "Product",
    "contact_info", "company_name", "Bid Summary", "Product Specification"
]

# Initialize LLM and embeddings
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def load_documents(folder_path):
    """Load all PDF and HTML files from folder"""
    docs = []
    for file in os.listdir(folder_path):
        path = os.path.join(folder_path, file)
        try:
            if file.endswith('.pdf'):
                docs.extend(PyPDFLoader(path).load())
            elif file.endswith(('.html', '.htm')):
                docs.extend(UnstructuredHTMLLoader(path).load())
        except Exception as e:
            print(f"Error loading {file}: {e}")
    return docs


def extract_rfp_data(folder_path):
    """Extract structured RFP data from documents"""
    print(f"\nProcessing: {folder_path}")
    
    # Load documents and create vector store
    docs = load_documents(folder_path)
    if not docs:
        print("No documents found!")
        return None
    
    vector_store = FAISS.from_documents(docs, embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 10})
    
    # Get relevant context
    context_docs = retriever.invoke("bid RFP solicitation specifications requirements")
    context = "\n\n".join([d.page_content for d in context_docs])
    
    # Create extraction prompt
    prompt = f"""Extract RFP information from this document and return ONLY valid JSON with these exact fields:
{json.dumps(FIELDS, indent=2)}

Rules:
- Use exact field names listed above
- For missing data, use "Not specified"
- contact_info should be a dict with Name, Email, Phone, Address
- Product Specification should be detailed technical specs
- Return ONLY the JSON, no markdown or extra text

Document Content:
{context}

JSON Output:"""
    
    # Get LLM response
    try:
        response = llm.invoke(prompt)
        content = response.content.strip()
        
        # Clean markdown formatting if present
        if content.startswith("```"):
            content = content.split("\n", 1)[1].rsplit("\n", 1)[0]
            if content.startswith("json"):
                content = content[4:].strip()
        
        data = json.loads(content)
        
        # Ensure all fields present
        for field in FIELDS:
            if field not in data:
                data[field] = "Not specified"
        
        print(f"✓ Extracted {len(data)} fields")
        return data
        
    except Exception as e:
        print(f"Extraction error: {e}")
        return {field: "Extraction failed" for field in FIELDS}


def main():
    """Process folders and save results"""
    folders = ["Bid1", "Bid2"]  # Add your folder names here
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    for folder in folders:
        if not os.path.exists(folder):
            print(f"Folder not found: {folder}")
            continue
            
        data = extract_rfp_data(folder)
        if data:
            output_file = os.path.join(output_dir, f"{folder}_extracted.json")
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Saved: {output_file}\n")


if __name__ == "__main__":
    main()