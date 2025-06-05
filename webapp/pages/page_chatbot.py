"""
Página do Chatbot para análise de dados conversacional usando Streamlit.

Funcionalidades:
- Interface de chat para perguntas em linguagem natural sobre os dados.
- Geração automática de SQL via LLM.
- Execução de consultas SQL e retorno em linguagem natural.
- Sugestão de perguntas.
- Geração automática de gráficos com IA (matplotlib/seaborn/plotly) a partir dos dados retornados.
- Limpeza e validação de código gerado pela LLM para segurança.
"""

import streamlit as st
import sys
import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Ajusta o sys.path para importar módulos do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from config import load_config
from core.db_utils import create_db_engine, get_schema, executar_sql
from core.llm_utils import (
    gerar_sql_llm_chat,
    extrair_sql_da_resposta,
    gerar_resposta_natural,
    classificar_mensagem,
    responder_casual_interaction,
    gerar_codigo_grafico_llm,
    is_safe_plot_code,
    limpar_codigo_plot,
)
from core.prompt_utils import load_resource

# Configuração da página Streamlit
st.set_page_config(page_title="LLM Data Analyzer", page_icon="🎲")

# Sidebar com logo e navegação
st.sidebar.image(r".\assets/neurotech.png")
with st.sidebar:
    st.page_link('page_home.py', label="Página Inicial", icon="🏠")
    st.page_link('pages/page_chatbot.py', label="Chatbot", icon="🤖")

# Sugestões de perguntas para o usuário
sugestoes = [
    "Qual a média de idade por UF?",
    "Quantos clientes estão inadimplentes?",
    "Qual o número de clientes por classe social?"
]

def inicializar_sessao():
    """
    Inicializa variáveis de sessão necessárias para o funcionamento do chatbot.
    """
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
    """
    Exibe a interface do chatbot, processa as mensagens do usuário,
    executa consultas SQL, gera respostas e gráficos com IA.
    """
    # Título e subtítulo
    st.markdown(
        "<h2 style='color:#1a237e; text-align:center;'>Chatbot de Análise de Dados</h2>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align:center; color:#b71c1c;'>Converse em linguagem natural e obtenha respostas inteligentes sobre os dados!</p>",
        unsafe_allow_html=True
    )

    # Sugestões de perguntas
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

    # Ao enviar mensagem, adiciona ao histórico e ativa processamento
    if user_message:
        st.session_state.history.append(("user", user_message))
        st.session_state.pending_response = user_message
        st.rerun()

    # Processa a mensagem pendente (se houver)
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
            # Responde interações casuais
            resposta = responder_casual_interaction(history, user_message, config)
            st.session_state.history.append(("assistant", resposta))
            st.chat_message("assistant").write(resposta)
            del st.session_state.pending_response
        elif tipo == "sql_request":
            # Gera SQL, executa consulta e responde
            resposta_llm = gerar_sql_llm_chat(user_message, schema, config, sintax, data_dictionary, history)
            try:
                consulta_sql = extrair_sql_da_resposta(resposta_llm)
                df_resultado = executar_sql(engine, consulta_sql)
                resposta = gerar_resposta_natural(df_resultado, user_message, consulta_sql, config, history)
                st.session_state.history.append(("assistant", resposta))
                st.chat_message("assistant").write(resposta)

                # Limpeza do DataFrame para gráficos
                if df_resultado is not None and not df_resultado.empty:
                    df_resultado = df_resultado.dropna()
                    st.session_state.df_para_grafico = df_resultado
                    st.session_state.pergunta_para_grafico = user_message
                else:
                    st.session_state.df_para_grafico = None
                    st.session_state.pergunta_para_grafico = None

                del st.session_state.pending_response
            except Exception as e:
                erro_msg = f"Desculpe, não pude processar seu pedido. Error: {str(e)}"
                st.session_state.history.append(("assistant", erro_msg))
                st.chat_message("assistant").write(erro_msg)
                del st.session_state.pending_response
        else:
            # Mensagem não compreendida
            erro_msg = "Desculpe, não pude entender sua mensagem. Por favor, tente novamente."
            st.session_state.history.append(("assistant", erro_msg))
            st.chat_message("assistant").write(erro_msg)
            del st.session_state.pending_response

    # Botão para gerar gráfico com IA (aparece apenas se houver dados)
    if (
        st.session_state.get("df_para_grafico") is not None
        and st.session_state.get("pergunta_para_grafico") is not None
        and not st.session_state.get("gerar_grafico", False)
    ):
        if st.button("Gerar gráfico com IA"):
            code = gerar_codigo_grafico_llm(
                st.session_state.df_para_grafico,
                st.session_state.pergunta_para_grafico,
                st.session_state.config
            )
            code_limpo = limpar_codigo_plot(code)
            if is_safe_plot_code(code_limpo):
                st.session_state.code_grafico = code_limpo
                st.session_state.gerar_grafico = True
            else:
                st.warning("O código gerado pela IA não foi considerado seguro para execução.")

    # Exibe o gráfico se a flag estiver ativa
    if st.session_state.get("gerar_grafico", False):
        st.code(st.session_state.code_grafico, language="python")
        local_vars = {"df": st.session_state.df_para_grafico}
        try:
            exec(
                st.session_state.code_grafico,
                {"plt": plt, "sns": sns, "px": px, "df": st.session_state.df_para_grafico},
                local_vars
            )
            st.pyplot(plt.gcf())
            plt.clf()
        except Exception as e:
            st.error(f"Erro ao executar o código gerado: {e}")
        # Limpa o estado para não duplicar
        st.session_state.gerar_grafico = False
        st.session_state.code_grafico = None
        st.session_state.df_para_grafico = None
        st.session_state.pergunta_para_grafico = None

if __name__ == "__main__" or True:
    inicializar_sessao()
    exibir_chat()