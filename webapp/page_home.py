import streamlit as st

st.set_page_config(page_title="LLM Data Analyzer", page_icon="🎲")

st.sidebar.image(r".\assets/neurotech.png")

with st.sidebar:
    st.page_link('page_home.py', label="Página Inicial", icon="🏠")
    st.page_link('pages/page_chatbot.py', label="Chatbot", icon="🤖")

def pagina_principal():
    # Cores
    azul = "#1a237e"
    vermelho = "#b71c1c"

    # Container principal do projeto com borda
    with st.container(border=True):
        st.markdown(
            f"<h1 style='color:{azul}; text-align:center;'>LLM Data Analyzer Challenge 🤖</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<h4 style='color:{vermelho}; text-align:center;'>Análise de Dados Conversacional com IA</h4>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"""
**Este projeto foi desenvolvido como parte do processo seletivo da Neurotech, com o objetivo de transformar a maneira como interagimos com dados.  
A proposta é simples e poderosa: permitir que qualquer pessoa consulte e analise dados de forma natural e intuitiva, apenas conversando com um chatbot inteligente.**

---

### Visão Geral
O LLM Data Analyzer é uma aplicação de análise de dados conversacional que utiliza Inteligência Artificial Generativa para interpretar perguntas em linguagem natural, gerar automaticamente consultas SQL, executar essas consultas em um banco relacional na nuvem e retornar respostas claras e justificadas ao usuário.

### Funcionalidades Principais
- Chat inteligente com múltiplas perguntas por sessão
- Geração automática de SQL (GPT-4o mini - Azure OpenAI)
- Execução em banco relacional (Azure SQL Database)
- Respostas em linguagem natural com explicações
- Histórico de conversa persistente
- Criação automática de gráficos (matplotlib, seaborn ou plotly) com base nos resultados

### Tecnologias Utilizadas
- **Azure OpenAI** (modelo GPT-4o mini) para interpretação e geração de linguagem natural
- **LangChain** para orquestração dos fluxos conversacionais e integração com ferramentas externas
- **SQLAlchemy** para comunicação segura e eficiente com o banco de dados
- **Streamlit** para desenvolvimento de uma interface leve, interativa e web-friendly
- **Azure SQL Database**, onde o Neurotech Data Challenge Dataset foi carregado a partir de um arquivo CSV

### 📊 Dataset
A base de dados utilizada foi fornecida pela Neurotech, com informações carregadas na Azure Cloud via serviço SQL Database.  
**Link:** [Neurotech Data Challenge Dataset](https://github.com/Neurolake/challenge-data-scientist/blob/main/datasets/credit_01/train.gz)
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # Informações da desenvolvedora
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("assets/profile.jpeg", width=140, caption="Giulia Buonafina")
    with col2:
        st.markdown(
            f"""
**Giulia Buonafina**  
Cientista de Dados Júnior  
Estudante de Engenharia da Computação - Universidade de Pernambuco (UPE)  

📧 [giulia2210@hotmail.com](mailto:giulia2210@hotmail.com)  
💼 [linkedin.com/in/giulia-buonafina-019574260](https://www.linkedin.com/in/giulia-buonafina-019574260/)  
🐙 [github.com/GiuBuonafina](https://github.com/GiuBuonafina)
            """
        )

    st.markdown("---")
    st.info("Acesse a aba 'Chatbot' para conversar com o seu assistente de dados!")

if __name__ == "__main__":
    pagina_principal()