from github import Github
from dotenv import load_dotenv
import os

load_dotenv()

# --- Configurações ---
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = os.getenv('REPO_NAME')
BACKLOG_FILE = os.getenv('BACKLOG_FILE', 'backlog.md')
ISSUE_SEPARATOR = '---'

def export_issues_to_backlog():
    option = int(input("Escolha uma opção(número):\n1. Pegar somente issues abertas.\n2. Pegar somentes issues fechadas.\n3. Pegar todas as issues (abertas e fechadas).\nOpção: "))
    if option != 1 and option != 2 and option != 3:
        print("Opção inválida.")
        return
    else:
        state = 'open' if option == 1 else 'closed' if option == 2 else 'all'
        
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

    # Buscar todas as issues abertas
    issues = repo.get_issues(state=state)

    backlog_lines = []

    for issue in issues:
        # Título
        backlog_lines.append(f"## {issue.title}")

        # Labels
        labels = [label.name for label in issue.labels]
        if labels:
            backlog_lines.append(f"Labels: {', '.join(labels)}")

        # Milestone
        if issue.milestone:
            backlog_lines.append(f"Milestone: {issue.milestone.title}")
            if issue.milestone.due_on:
                # Formato YYYY-MM-DD
                due_date = issue.milestone.due_on.strftime("%Y-%m-%d")
                backlog_lines.append(f"MilestoneDue: {due_date}")

        # Corpo da issue
        if issue.body:
            backlog_lines.append(issue.body.strip())

        # Separador
        backlog_lines.append(ISSUE_SEPARATOR)

    # Escrever no arquivo backlog.md
    try:
        with open(BACKLOG_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(backlog_lines))
        print(f"Backlog exportado para '{BACKLOG_FILE}' com {len(list(issues))} issues.")
    except Exception as e:
        print(f"Erro ao escrever o arquivo '{BACKLOG_FILE}': {e}")

if __name__ == "__main__":
    export_issues_to_backlog()
