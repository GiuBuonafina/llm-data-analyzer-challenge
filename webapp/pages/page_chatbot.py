import streamlit as st
import sys
import os

# Ajusta o sys.path para importar módulos do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

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

st.set_page_config(page_title="LLM Data Analyzer", page_icon="🎲")

st.sidebar.image(r".\assets/neurotech.png")
with st.sidebar:
    st.page_link('page_home.py', label="Página Inicial", icon="🏠")
    st.page_link('pages/page_chatbot.py', label="Chatbot", icon="🤖")

# Sugestões de mensagens iniciais
sugestoes = [
    "Qual a média de idade por UF?",
    "Qual a taxa de inadimplência média por UF?",
    "Quantos clientes estão inadimplentes?",
    "Qual a classe social com maior número de clientes?"
]

def inicializar_sessao():
    if "history" not in st.session_state:
        st.session_state.history = [
            ("assistant", "Olá! 👋 Eu sou o assistente de análise de dados da Neurotech. Como posso te ajudar hoje?")
        ]
    if "engine" not in st.session_state:
        config = load_config()
        st.session_state.config = config
        st.session_state.engine = create_db_engine(config["SQLALCHEMY_DATABASE_URI"])
        st.session_state.schema = get_schema(st.session_state.engine, schema_name="dbo")
        st.session_state.sintax = load_resource("resources/sintax.txt")
        st.session_state.data_dictionary = load_resource("resources/data_dictionary.txt")

def exibir_chat():
    st.markdown(
        "<h2 style='color:#1a237e; text-align:center;'>Chatbot de Análise de Dados</h2>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align:center; color:#b71c1c;'>Converse em linguagem natural e obtenha respostas inteligentes sobre os dados!</p>",
        unsafe_allow_html=True
    )

    # Sugestões de mensagem
    with st.expander("Sugestões de perguntas", expanded=False):
        for s in sugestoes:
            st.markdown(f"- {s}")

    # Exibe o histórico do chat
    for role, msg in st.session_state.history:
        if role == "user":
            st.chat_message("user").write(msg)
        else:
            st.chat_message("assistant").write(msg)

    # Campo de entrada do usuário
    user_message = st.chat_input("Digite sua pergunta ou mensagem...")

    if user_message:
        st.session_state.history.append(("user", user_message))
        st.session_state.pending_response = user_message
        st.rerun()
# 
    if "pending_response" in st.session_state:
        user_message = st.session_state.pending_response
        config = st.session_state.config
        engine = st.session_state.engine
        schema = st.session_state.schema
        sintax = st.session_state.sintax
        data_dictionary = st.session_state.data_dictionary
        history = st.session_state.history

        tipo = classificar_mensagem(user_message, config, history)


        if tipo == "casual_interaction":
            resposta = responder_casual_interaction(history, user_message, config)
            st.session_state.history.append(("assistant", resposta))
            st.chat_message("assistant").write(resposta)
        elif tipo == "sql_request":
            resposta_llm = gerar_sql_llm_chat(user_message, schema, config, sintax, data_dictionary, history)
            try:
                consulta_sql = extrair_sql_da_resposta(resposta_llm)
                df_resultado = executar_sql(engine, consulta_sql)
                resposta = gerar_resposta_natural(df_resultado, user_message, consulta_sql, config, history)
                st.session_state.history.append(("assistant", resposta))
                st.chat_message("assistant").write(resposta)
            except Exception as e:
                erro_msg = f"Desculpe, não pude processar seu pedido. Error: {str(e)}"
                st.session_state.history.append(("assistant", erro_msg))
                st.chat_message("assistant").write(erro_msg)
        else:
            erro_msg = "Desculpe, não pude entender sua mensagem. Por favor, tente novamente."
            st.session_state.history.append(("assistant", erro_msg))
            st.chat_message("assistant").write(erro_msg)
            del st.session_state.pending_response

if __name__ == "__main__" or True:
    inicializar_sessao()
    exibir_chat()