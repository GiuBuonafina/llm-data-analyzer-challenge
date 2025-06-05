# LLM Data Analyzer Challenge 🤖

Este projeto foi desenvolvido como parte do processo seletivo da **Neurotech**.  
Seu objetivo é demonstrar a construção de um sistema de análise de dados conversacional, onde o usuário pode interagir via terminal em linguagem natural e obter respostas baseadas em consultas SQL geradas automaticamente por uma LLM (Large Language Model).

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
├── main.py                  # Ponto de entrada do sistema (interface terminal, até o momento)
├── config.py                # Carregamento de variáveis de ambiente
├── requirements.txt         # Dependências do projeto
│
├── core/                    # Lógica principal desacoplada
│   ├── __init__.py
│   ├── db_utils.py          # Funções para interação com banco de dados
│   ├── llm_utils.py         # Funções para interação com LLM (OpenAI/Azure)
│   └── prompt_utils.py      # Utilitários para prompts e leitura de recursos
│
├── resources/               # Arquivos de apoio facilmente editáveis
│   ├── sintax.txt           # Regras de sintaxe SQL (desacoplado do código)
│   └── data_dictionary.txt  # Dicionário de dados (desacoplado do código)
│
├── tests/                   # Testes unitários com pytest
│   ├── __init__.py
│   ├── test_db_utils.py
│   └── test_llm_utils.py
│
└── __init__.py
```

**Principais escolhas de design:**
- **Modularização:** Cada responsabilidade em um arquivo/módulo.
- **Recursos desacoplados:** Sintaxe SQL e dicionário de dados ficam em arquivos `.txt` na pasta `resources/`, facilitando manutenção e extensão para outros bancos ou domínios.
- **Testabilidade:** Testes unitários para funções críticas, garantindo robustez.
- **Histórico de conversa:** Todo o histórico é mantido e passado para as funções de LLM, permitindo contexto conversacional.

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


### 5. Execute o sistema

```sh
python main.py
```

Você verá o prompt do assistente no terminal. Basta digitar suas perguntas!

---

## Rodando os testes

```sh
pytest
```

---


**Desenvolvido como parte do processo seletivo da Neurotech.**