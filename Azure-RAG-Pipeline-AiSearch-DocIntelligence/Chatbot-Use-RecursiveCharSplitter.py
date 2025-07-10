from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from langchain.text_splitter import RecursiveCharacterTextSplitter
import openai

# Step 1: Extract full text from PDF
doc_url = "https://example.com/sample.pdf"
form_client = DocumentAnalysisClient(endpoint=FORM_ENDPOINT, credential=AzureKeyCredential(FORM_KEY))

poller = form_client.begin_analyze_document_from_url("prebuilt-read", doc_url)
result = poller.result()

# Combine all page text
full_text = "\n".join([line.content for page in result.pages for line in page.lines])

# Step 2: Chunk using RecursiveCharacterTextSplitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    separators=["\n\n", "\n", ".", " ", ""]
)

chunks = splitter.split_text(full_text)

# Step 3: Generate embeddings for each chunk
openai.api_key = "YOUR_OPENAI_KEY"
embeddings = [
    openai.Embedding.create(input=chunk, model="text-embedding-ada-002")["data"][0]["embedding"]
    for chunk in chunks
]

# Step 4: Store chunks + vectors in Azure AI Search
from azure.search.documents import SearchClient

docs_to_upload = [
    {
        "id": f"doc-chunk-{i}",
        "content": chunk,
        "embedding": vector,
        "fileName": "sample.pdf"
    }
    for i, (chunk, vector) in enumerate(zip(chunks, embeddings))
]

search_client = SearchClient(endpoint=SEARCH_ENDPOINT, index_name=INDEX_NAME, credential=AzureKeyCredential(SEARCH_KEY))
search_client.upload_documents(documents=docs_to_upload)
