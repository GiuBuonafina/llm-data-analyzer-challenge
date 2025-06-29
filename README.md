# LLM Data Analyzer Challenge 🤖

[![Assista à demonstração no YouTube](https://img.youtube.com/vi/KVm4WVmwNno/maxresdefault.jpg)](https://www.youtube.com/watch?v=KVm4WVmwNno)

> 🎥 **Clique na imagem acima para ver a demonstração completa no YouTube!**

Este projeto foi desenvolvido como parte do processo seletivo da **Neurotech**.  
Seu objetivo é demonstrar a construção de um sistema de análise de dados conversacional, onde o usuário pode interagir via terminal **ou via interface web (Streamlit)** em linguagem natural e obter respostas baseadas em consultas SQL geradas automaticamente por uma LLM (Large Language Model).

---

## Propósito

Permitir que qualquer pessoa, mesmo sem conhecimento técnico em SQL, possa consultar e analisar dados de um banco relacional apenas conversando em linguagem natural.  
O sistema interpreta a intenção do usuário, gera a consulta SQL adequada, executa no banco e retorna a resposta de forma clara e amigável.

---

## Organização do Projeto

A estrutura foi pensada para **extensibilidade**, **clareza** e **facilidade de manutenção**:

```
llm-data-analyzer-challenge/
│
├── main.py                      # Interface terminal
├── config.py                    # Carregamento de variáveis de ambiente
├── requirements.txt             # Dependências do projeto
│
├── core/                        # Lógica principal desacoplada
│   ├── __init__.py
│   ├── db_utils.py              # Funções para interação com banco de dados
│   ├── llm_utils.py             # Funções para interação com LLM (OpenAI/Azure)
│   └── prompt_utils.py          # Utilitários para prompts e leitura de recursos
│
├── resources/                   # Arquivos de apoio facilmente editáveis
│   ├── sintax.txt               # Regras de sintaxe SQL (desacoplado do código)
│   └── data_dictionary.txt      # Dicionário de dados (desacoplado do código)
│
├── webapp/                      # Interface web (Streamlit)
│   ├── page_home.py             # Página inicial do Streamlit
│   └── pages/
│       └── page_chatbot.py      # Página do chatbot no Streamlit
│
├── assets/                      # Imagens e logos
│   └── neurotech.png
│   └── profile.jpeg
│
├── tests/                       # Testes unitários com pytest
│   ├── __init__.py
│   ├── test_db_utils.py
│   └── test_llm_utils.py
│
├── Configuration.env.example    # Exemplo de configuração de ambiente
├── .gitignore
└── README.md
```

**Principais escolhas de design:**
- **Modularização:** Cada responsabilidade em um arquivo/módulo.
- **Recursos desacoplados:** Sintaxe SQL e dicionário de dados ficam em arquivos `.txt` na pasta `resources/`, facilitando manutenção e extensão para outros bancos ou domínios.
- **Testabilidade:** Testes unitários para funções críticas, garantindo robustez.
- **Histórico de conversa:** Todo o histórico é mantido e passado para as funções de LLM, permitindo contexto conversacional.
- **Interface multiplataforma:** O usuário pode escolher entre terminal ou webapp (Streamlit) para interagir.

---

## 🗄️ Base de Dados

A base de dados utilizada neste projeto pode ser encontrada em:  
[https://github.com/Neurolake/challenge-data-scientist/blob/main/datasets/credit_01/train.gz](https://github.com/Neurolake/challenge-data-scientist/blob/main/datasets/credit_01/train.gz)

---

## 🖥️ Como executar localmente

### 1. Clone o repositório

```sh
git clone https://github.com/GiuBuonafina/llm-data-analyzer-challenge.git
cd llm-data-analyzer-challenge
```

### 2. Crie e ative um ambiente virtual

```sh
python -m venv venv
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
```

### 3. Instale as dependências

```sh
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Copie o arquivo `Configuration.env.example` para `Configuration.env` e preencha com seus dados de conexão e credenciais antes de rodar o projeto.  
O arquivo real `Configuration.env` está no `.gitignore` e **não deve ser versionado**.

---

### 5. Execute a interface terminal

```sh
python main.py
```
Você verá o prompt do assistente no terminal. Basta digitar suas perguntas!

---

### 6. Execute a interface web (Streamlit)

```sh
streamlit run webapp/page_home.py
```
Acesse o endereço exibido no terminal (geralmente http://localhost:8501) para usar a interface web, que inclui:
- Página inicial com detalhes do projeto e da desenvolvedora
- Página de chatbot com histórico, sugestões e visual de chat moderno
- **Geração automática de gráficos com IA:** após uma consulta bem-sucedida, você pode clicar em "Gerar gráfico com IA" e o sistema utiliza uma LLM para criar e exibir um gráfico relevante com base nos dados retornados.

---

## Rodando os testes

```sh
pytest
```

---

## 💡 Como foi construído

- **Backend desacoplado:** Toda a lógica de banco, LLM e prompts está desacoplada da interface, permitindo fácil manutenção e extensão.
- **Webapp moderno:** A interface Streamlit foi customizada para simular um chat real, com sugestões, histórico e visual limpo.
- **Terminal funcional:** O projeto pode ser usado totalmente via terminal, útil para ambientes sem interface gráfica.
- **Testes unitários:** Cobrem funções críticas de banco e LLM.
- **Configuração segura:** Uso de `.env` para segredos e exemplos para facilitar onboarding.
- **Geração de gráficos com IA:** O usuário pode solicitar que a IA gere automaticamente um gráfico relevante a partir dos dados retornados pela consulta SQL, tornando a análise ainda mais visual e intuitiva.

---

## 🚧 Desafios enfrentados

- **Conexão com Azure SQL Database:** O banco em nuvem pode demorar para responder (especialmente em modo serverless), exigindo aumento de timeout e tratamento de tentativas de conexão.
- **Construção de chatbot funcional no Streamlit:** Adaptar a experiência de chat para o Streamlit exigiu criatividade, já que a ferramenta não foi projetada originalmente para fluxos conversacionais dinâmicos. Foi necessário contornar limitações de estado, atualização de interface e controle de histórico para garantir uma experiência fluida e intuitiva ao usuário.
---

**Desenvolvido como parte do processo seletivo da Neurotech.**
