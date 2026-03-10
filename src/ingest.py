import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector

load_dotenv()

def check_environment_variables():
    print("Inicializando...", end="", flush=True)
    errors = []
    for k in ("OPENAI_API_KEY", "OPENAI_EMBEDDING_MODEL", "DATABASE_URL", "PG_VECTOR_COLLECTION_NAME", "PDF_PATH"):
        if not os.getenv(k):
            errors.append(f"Variável de ambiente {k} não está definida")
    
    is_ok = len(errors) == 0
    print("OK!" if is_ok else "Erro!")
    
    if (not is_ok):
        print("\n".join(f" - {error}" for error in errors) + "\n")
        exit()


def load_pdf():
    print("Carregando PDF...", end="", flush=True)
    current_directory = Path(__file__).parent.parent
    PDF_PATH = current_directory / os.getenv("PDF_PATH")
    
    doc = PyPDFLoader(str(PDF_PATH)).load()
    if not doc:
        raise SystemExit("Arquivo PDF não encontrado")
    
    print("OK!")
    return doc


def split_document(doc):
    print("Dividindo documento...", end="", flush=True)
    splits = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        add_start_index=False
    ).split_documents(doc)

    if not splits:
        raise SystemExit(0)

    print(f"OK!\nDocumento dividido em {len(splits)} chunks!")
    return splits


def enrich_documents(splits):
    print("Enriquecendo documentos...", end="", flush=True)
    enriched = [
        Document(
            page_content=d.page_content,
            metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
        )
        for d in splits
    ]
    print("OK!")
    return enriched


def ingest_documents(enriched_docs):
    print("Ingerindo documentos...")
    ids = [f"doc-{i}" for i in range(len(enriched_docs))]
    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"))

    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True
    )
    store.add_documents(documents=enriched_docs, ids=ids)
    print(f"OK!\nIngestão concluída com sucesso. {len(enriched_docs)} documentos ingeridos.")
    

def ingest_pdf():
    check_environment_variables()
    doc_file = load_pdf()
    splits = split_document(doc_file)
    enriched_docs = enrich_documents(splits)
    ingest_documents(enriched_docs)
    

if __name__ == "__main__":
    ingest_pdf()