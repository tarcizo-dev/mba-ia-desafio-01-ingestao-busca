import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_core.prompts import ChatPromptTemplate
from functions import print_overwrite

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def check_environment_variables():
  print("Inicializando sistema de busca...", end="", flush=True)
  errors = []
  for k in ("OPENAI_API_KEY", "OPENAI_EMBEDDING_MODEL", "DATABASE_URL", "PG_VECTOR_COLLECTION_NAME"):
    if not os.getenv(k):
      errors.append(f"Variável de ambiente {k} não está definida")
  
  is_ok = len(errors) == 0
  print("OK!" if is_ok else "Erro!")
  
  if (not is_ok):
    print("\n".join(f" - {error}" for error in errors))

  return is_ok


def search_prompt(question=None):
  if question == None:
    return check_environment_variables()

  print_overwrite("--- Carregando embeddings... ---")
  embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"))

  print_overwrite("--- Carregando store... ---")
  store = PGVector(
    embeddings=embeddings,
    collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
    connection=os.getenv("DATABASE_URL"),
    use_jsonb=True
  )

  print_overwrite("--- Consultando com similarity search... ---")
  results = store.similarity_search_with_score(question, k=10)

  print_overwrite("--- Montando contexto... ---")
  context = "\n\n".join(doc.page_content.strip() for i, (doc, score) in enumerate(results, start=1))

  print_overwrite("--- Montando chat prompt template... ---")
  system_prompt_template = ("system", PROMPT_TEMPLATE)
  chat_prompt = ChatPromptTemplate([system_prompt_template])

  print_overwrite("--- Formatando mensagens... ---")
  messages = chat_prompt.format_messages(contexto=context, pergunta=question)
  
  return messages
  