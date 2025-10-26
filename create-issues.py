from github import Github
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# --- Configurações (Lidas do arquivo .env) ---

# 1. Seu Token de Acesso Pessoal (PAT)
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# 2. Nome do Repositório (Ex: 'seu_usuario/seu_repositorio')
REPO_NAME = os.getenv('REPO_NAME')

# 3. Nome do arquivo de backlog
BACKLOG_FILE = os.getenv('BACKLOG_FILE')

# Separador que divide as issues no arquivo backlog.md
ISSUE_SEPARATOR = '---'

# --- Função Principal ---

def create_github_issues_from_backlog():
    """
    Lê o arquivo de backlog e cria issues no GitHub.
    """
    if not GITHUB_TOKEN:
        print("Erro: A variável de ambiente GITHUB_TOKEN não está configurada.")
        print("Por favor, configure-a com o seu Personal Access Token.")
        return

    print(f"Iniciando a conexão com o GitHub para o repositório: {REPO_NAME}...")
    
    try:
        # 1. Autenticar no GitHub
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
    except Exception as e:
        print(f"Erro ao autenticar ou acessar o repositório. Verifique o token e o nome do repositório.")
        print(f"Detalhes do erro: {e}")
        return

    # 2. Ler o arquivo de backlog
    try:
        with open(BACKLOG_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{BACKLOG_FILE}' não encontrado.")
        return

    # 3. Processar o conteúdo para extrair as issues
    issue_blocks = content.strip().split(ISSUE_SEPARATOR)
    
    issues_to_create = []
    for block in issue_blocks:
        block = block.strip()
        if not block:
            continue
            
        # O título é a primeira linha que começa com '## ' (sintaxe Markdown de cabeçalho)
        lines = block.split('\n')
        title_line = next((line for line in lines if line.startswith('## ')), None)
        
        if title_line:
            title = title_line.replace('## ', '').strip()
            # O corpo é o resto do bloco, excluindo a linha do título
            body = '\n'.join([line for line in lines if line != title_line]).strip()
            
            issues_to_create.append({'title': title, 'body': body})
        else:
            print(f"Aviso: Bloco ignorado por não ter um título (##): \n{block[:50]}...")

    # 4. Criar as Issues no GitHub
    if not issues_to_create:
        print("Nenhuma issue válida encontrada no backlog para criar.")
        return

    print(f"\n{len(issues_to_create)} issues encontradas no backlog. Criando no GitHub...")
    
    for i, issue_data in enumerate(issues_to_create):
        title = issue_data['title']
        body = issue_data['body']
        
        try:
            # Criação da issue propriamente dita
            new_issue = repo.create_issue(title=title, body=body)
            print(f"Issue {i+1}/{len(issues_to_create)} criada: '{title}' (URL: {new_issue.html_url})")
        except Exception as e:
            print(f"ERRO ao criar a Issue '{title}'. Detalhes: {e}")

if __name__ == "__main__":
    create_github_issues_from_backlog()