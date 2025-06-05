"""

Interface de linha de comando (terminal) para o LLM Data Analyzer Challenge.
Permite ao usuário interagir com o assistente de dados via terminal, fazendo perguntas em linguagem natural.
O sistema interpreta a intenção, gera SQL via LLM, executa a consulta e retorna respostas em linguagem natural.

Funcionalidades:
- Interação conversacional via terminal
- Geração automática de SQL com LLM
- Execução de consultas SQL em banco relacional
- Respostas explicativas em linguagem natural
- Histórico de conversa mantido durante a sessão
"""

from config import load_config
from core.db_utils import create_db_engine, get_schema, executar_sql
from core.llm_utils import (
    gerar_sql_llm_chat,
    extrair_sql_da_resposta,
    gerar_resposta_natural,
    classificar_mensagem,
    responder_casual_interaction
)
from core.prompt_utils import load_resource

def main():
    """
    Função principal que executa o loop de interação com o usuário no terminal.
    """
    # Carrega configurações e recursos
    config = load_config()
    engine = create_db_engine(config["SQLALCHEMY_DATABASE_URI"])
    schema = get_schema(engine, schema_name="dbo")
    sintax = load_resource("resources/sintax.txt")
    data_dictionary = load_resource("resources/data_dictionary.txt")

    print("Bem-vindo(a) ao LLM Data Analyzer Terminal!")
    print("Digite 'exit' ou 'quit' para sair a qualquer momento.\n")

    # Inicia o histórico de mensagens
    history = [] 
    while True:
        user_message = input("\nUser: ")
        if user_message.lower() in ["exit", "quit"]:
            print("Até a próxima!")
            break

        history.append(("user", user_message))

        # Classifica o tipo de mensagem do usuário
        tipo = classificar_mensagem(user_message, config, history)

        if tipo == "casual_interaction":
            # Responde perguntas casuais ou de interação
            resposta = responder_casual_interaction(history, user_message, config)
            print("Assistant:", resposta)
            history.append(("assistant", resposta)) 
        elif tipo == "sql_request":
            # Gera SQL, executa consulta e responde com base nos dados
            resposta_llm = gerar_sql_llm_chat(user_message, schema, config, sintax, data_dictionary, history)
            try:
                consulta_sql = extrair_sql_da_resposta(resposta_llm)
                df_resultado = executar_sql(engine, consulta_sql)
                resposta = gerar_resposta_natural(df_resultado, user_message, consulta_sql, config, history)
                print("Assistant:", resposta)
                history.append(("assistant", resposta))  # Adiciona resposta do assistente
            except Exception as e:
                erro_msg = f"Desculpe, não pude processar seu pedido. Error: {str(e)}"
                print("Assistant:", erro_msg)
                history.append(("assistant", erro_msg))
        else:
            # Se a classificação não for reconhecida, retorna uma mensagem de erro
            erro_msg = "Desculpe, não pude entender sua mensagem. Por favor, tente novamente."
            print("Assistant:", erro_msg)
            history.append(("assistant", erro_msg))


if __name__ == "__main__":
    main()