from github import Github
from dotenv import load_dotenv
import os

load_dotenv()

# --- Configurações ---
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = os.getenv('REPO_NAME')
BACKLOG_FILE = os.getenv('BACKLOG_FILE')
ISSUE_SEPARATOR = '---'
DEFAULT_LABELS = []  # Labels padrão caso o bloco não especifique

def create_github_issues_from_backlog():
    if not GITHUB_TOKEN:
        print("Erro: GITHUB_TOKEN não configurado.")
        return

    print(f"Conectando ao GitHub para o repositório: {REPO_NAME}")
    g = Github(GITHUB_TOKEN)
    
    try:
        repo = g.get_repo(REPO_NAME)
    except Exception as e:
        print(f"Erro ao acessar o repositório: {e}")
        return

    # Ler backlog
    try:
        with open(BACKLOG_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Arquivo '{BACKLOG_FILE}' não encontrado.")
        return

    issue_blocks = content.strip().split(ISSUE_SEPARATOR)
    issues_to_create = []

    for block in issue_blocks:
        block = block.strip()
        if not block:
            continue
        lines = block.split('\n')
        title_line = next((line for line in lines if line.startswith('## ')), None)
        if title_line:
            title = title_line.replace('## ', '').strip()
            # Procurar linha de Labels
            label_line = next((line for line in lines if line.lower().startswith('labels:')), "")
            labels = [lbl.strip() for lbl in label_line.replace('Labels:', '').split(',')] if label_line else DEFAULT_LABELS
            # Corpo da issue
            body = '\n'.join([line for line in lines if line != title_line and line != label_line]).strip()
            issues_to_create.append({'title': title, 'body': body, 'labels': labels})
        else:
            print(f"Aviso: Bloco ignorado sem título: {block[:50]}...")

    if not issues_to_create:
        print("Nenhuma issue válida encontrada.")
        return

    print(f"{len(issues_to_create)} issues encontradas. Criando...")

    for i, issue_data in enumerate(issues_to_create):
        title = issue_data['title']
        body = issue_data['body']
        labels = issue_data['labels']

        try:
            new_issue = repo.create_issue(title=title, body=body, labels=labels)
            print(f"Issue '{title}' criada: {new_issue.html_url}")
        except Exception as e:
            print(f"Erro ao criar issue '{title}': {e}")


if __name__ == "__main__":
    create_github_issues_from_backlog()
