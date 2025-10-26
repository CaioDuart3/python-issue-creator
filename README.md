# 🤖 Backlog to Issues: Automação de Backlog no GitHub

## 📝 Descrição do Projeto

Este projeto consiste em um script Python simples, mas poderoso, que automatiza a criação de Issues (tarefas) no GitHub a partir de um arquivo de texto estruturado (backlog.md).

Ele transforma cada título marcado com `##` no Markdown em um título de issue e utiliza o conteúdo subsequente até o separador `---` como descrição da issue.

✨ Funcionalidades

* **Extração Inteligente:** Lê e processa um arquivo backlog.md estruturado com títulos e descrições.

* **Criação de Issues com Labels:** Permite adicionar labels para cada issue diretamente no .md usando a linha `Labels: bug, urgent` antes do separador `---`.

* **Autenticação Segura:** Utiliza um Personal Access Token (PAT) do GitHub, gerenciado por meio de um arquivo .env.

* **Compatível com qualquer repositório:** Cria issues em repositórios públicos ou privados sem depender de Projects Classic.


## ⚙️ Tecnologias Utilizadas

| Nome | Descrição |
| :--- | :--- |
| **Python** | Linguagem principal para o script de automação. |
| **PyGithub** | Biblioteca essencial para interagir com a API do GitHub. |
| **python-dotenv** | Biblioteca para gerenciar variáveis de ambiente de forma segura (`.env`). |
| **Markdown** | Utilizado para a estrutura do arquivo de backlog (`backlog.md`) e para formatar a descrição das Issues no GitHub. |

## 🚀 Como Executar o Projeto

Siga os passos abaixo para clonar, configurar e rodar o script na sua máquina.

### 1\. Pré-requisitos

  * Python 3.x instalado.
  * Uma conta no GitHub.
  * Um repositório GitHub (público ou privado) onde as issues serão criadas.

### 2\. Configuração do Ambiente

**A. Clone o Repositório:**

```bash
git clone https://github.com/CaioDuart3/python-issue-creator
cd python-issue-creator
```

**B. Instale as Dependências:**

Crie um ambiente virtual (opcional, mas recomendado) e instale as bibliotecas listadas no `requirements.txt`:

```bash
# Opcional: Criar e ativar um ambiente virtual
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate.bat # Windows

# Instalar dependências
pip install -r requirements.txt
```

**C. Crie o Arquivo `.env`:**

Na raiz do projeto, crie um arquivo chamado **`.env`** e preencha com suas credenciais conforme está sugerido no arquivo `.env-example`:

```env
GITHUB_TOKEN="<SEU_PERSONAL_ACCESS_TOKEN_AQUI>"
REPO_NAME="<SEU_USUARIO>/<SEU_REPOSITORIO>"
BACKLOG_FILE="backlog.md"
```

> 🔑 **Onde Obter o GITHUB\_TOKEN?**
> Você deve gerar um **Personal Access Token (PAT)** nas Configurações do seu GitHub: **Settings -\> Developer settings -\> Personal access tokens (classic)**. Certifique-se de marcar o escopo **`repo`** para que o script possa criar issues.

### 3\. Crie o Backlog

Crie ou atualize o arquivo **`backlog.md`** na raiz do projeto, seguindo o formato dos título e descrições, separando cada Issue com `---`:

### 4\. Execute o Script

Basta rodar o script principal do Python:

```bash
python create_issues.py
```

O script lerá o `backlog.md` e criará as Issues correspondentes no seu repositório GitHub.
