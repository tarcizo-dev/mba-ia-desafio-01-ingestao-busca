##### MBA em Engenharia de Software com IA - Full Cycle
# Desafio 01 - Ingestão e Busca Semântica com LangChain e Postgres

## Configuração do Ambiente

Para configurar o ambiente e instalar as dependências do projeto, siga os passos abaixo:

1. **Criar e ativar um ambiente virtual (`venv`):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

2. **Instalar as dependências a partir do `requirements.txt`:**
   
   ```bash
   pip install -r requirements.txt
   ```


3. **Configurar as variáveis de ambiente:**

   - Duplique o arquivo `.env.example` e renomeie para `.env`
   - Abra o arquivo `.env` e substitua os valores pelas suas chaves de API reais


4. **Subir o banco de dados:**

    ```bash
    docker compose up -d
    ```

5. **Executar ingestão do PDF:**

    ```bash
    python src/ingest.py
    ```

6. **Rodar o chat:**

    ```bash
    python src/chat.py
    ```