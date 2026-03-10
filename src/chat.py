import os
from dotenv import load_dotenv
from search import search_prompt
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from functions import print_overwrite


def check_environment_variables():
    print("Inicializando chat...", end="", flush=True)
    for k in ["OPENAI_API_KEY"]:
        if not os.getenv(k):
            print("Erro!")
            raise RuntimeError(f"Variável de ambiente {k} não está definida")
    print("OK!")


def chat():
    EXIT_COMMAND = "sair"

    print("\n=============== Chat ===============")
    print("- Digite 'sair' para encerrar.")
    
    while True:
        query = input("\n\nPergunta: ")
        if query.lower() == EXIT_COMMAND:
            print("\nChat encerrado.\n")
            break

        if query.strip() == "":
            continue

        messages = search_prompt(query)
        
        print_overwrite("--- Aguardando OpenAI... ---")
        model = ChatOpenAI(model="gpt-5-nano", temperature=0)
        result = model.invoke(messages)

        print_overwrite(f"Resposta: {result.content}")


def main():
    load_dotenv()
    check_environment_variables()

    chain = search_prompt()
    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.\n")
        return

    chat()    


if __name__ == "__main__":
    main()