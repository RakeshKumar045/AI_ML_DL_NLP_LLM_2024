

#pip install azure-ai-formrecognizer openai azure-search-documents python-dotenv
# Azure RAG Pipeline with Document Intelligence and AI Search

import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex, SimpleField, SearchableField, VectorSearch, VectorSearchAlgorithmConfiguration, SearchFieldDataType
)
import openai
import uuid

# ENV SETUP
form_recognizer_key = os.environ["AZURE_FORM_KEY"]
form_recognizer_endpoint = os.environ["AZURE_FORM_ENDPOINT"]
search_key = os.environ["AZURE_SEARCH_KEY"]
search_endpoint = os.environ["AZURE_SEARCH_ENDPOINT"]
search_index_name = "docs-vector-index"
openai.api_key = os.environ["OPENAI_API_KEY"]






# STEP 1: Extract text from PDF
doc_url = "https://example.com/my-document.pdf"  # or use local file with appropriate upload method
form_client = DocumentAnalysisClient(form_recognizer_endpoint, AzureKeyCredential(form_recognizer_key))
poller = form_client.begin_analyze_document_from_url("prebuilt-read", doc_url)
result = poller.result()

full_text = "\n".join([line.content for page in result.pages for line in page.lines])




# STEP 2: Chunk text
def chunk_text(text, max_len=500):
    return [text[i:i+max_len] for i in range(0, len(text), max_len)]




chunks = chunk_text(full_text)





# STEP 3: Generate embeddings
embeddings = [ openai.Embedding.create(input=chunk, model="text-embedding-ada-002")["data"][0]["embedding"] for chunk in chunks ]






# STEP 4: Create Vector Index (if not exists)
index_client = SearchIndexClient(endpoint=search_endpoint, credential=AzureKeyCredential(search_key))


fields = [
    SimpleField(name="id", type=SearchFieldDataType.String, key=True),
    SearchableField(name="content", type=SearchFieldDataType.String),
    SimpleField(name="fileName", type=SearchFieldDataType.String, filterable=True),
    SimpleField(name="embedding", type="Collection(Edm.Single)")
]

vector_search = VectorSearch( algorithm_configurations=[VectorSearchAlgorithmConfiguration(name="default-hnsw", kind="hnsw")])



index = SearchIndex(name = search_index_name, fields = fields, vector_search=vector_search)

try:
    index_client.create_index(index)
except Exception as e:
    print(f"Index may already exist: {e}")





# STEP 5: Upload documents to Azure AI Search
search_client = SearchClient(endpoint=search_endpoint, index_name=search_index_name, credential=AzureKeyCredential(search_key))

docs = [
    {
        "id": str(uuid.uuid4()),
        "content": chunk,
        "embedding": vector,
        "fileName": "sample.pdf"
    }
    for chunk, vector in zip(chunks, embeddings)
]





result = search_client.upload_documents(documents=docs)
print("Upload result:", result)
