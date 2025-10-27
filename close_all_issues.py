from github import Github
from dotenv import load_dotenv
import os

load_dotenv()

# --- Configurações ---
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = os.getenv('REPO_NAME')
BACKLOG_FILE = os.getenv('BACKLOG_FILE', 'backlog.md')
INVALID_LABEL = "invalid"

def ensure_label(repo, label_name):
    """Verifica se o label existe, cria se não existir."""
    existing_labels = {label.name: label for label in repo.get_labels()}
    if label_name in existing_labels:
        return existing_labels[label_name]
    try:
        new_label = repo.create_label(name=label_name, color="FF0000", description="Issues inválidas")
        print(f"Label '{label_name}' criada.")
        return new_label
    except Exception as e:
        print(f"Erro ao criar label '{label_name}': {e}")
        return None

def delete_issues_from_backlog():
    if not GITHUB_TOKEN:
        print("Erro: GITHUB_TOKEN não configurado.")
        return

    if not os.path.exists(BACKLOG_FILE):
        print(f"Arquivo '{BACKLOG_FILE}' não encontrado.")
        return

    # Ler backlog e pegar títulos
    with open(BACKLOG_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    issue_titles = [line.replace('## ', '').strip() for line in lines if line.startswith('## ')]

    if not issue_titles:
        print("Nenhum título de issue encontrado no backlog.")
        return

    # Conectar ao GitHub
    g = Github(GITHUB_TOKEN)
    try:
        repo = g.get_repo(REPO_NAME)
    except Exception as e:
        print(f"Erro ao acessar o repositório: {e}")
        return

    # Garantir que o label "invalid" exista
    invalid_label = ensure_label(repo, INVALID_LABEL)

    # Buscar issues abertas
    existing_issues = list(repo.get_issues(state='open'))

    count_closed = 0
    for title in issue_titles:
        issue = next((i for i in existing_issues if i.title == title), None)
        if issue:
            try:
                # Adicionar label invalid
                labels = [lbl.name for lbl in issue.labels]
                if INVALID_LABEL not in labels:
                    labels.append(INVALID_LABEL)
                # Fechar issue com label
                issue.edit(state='closed', labels=labels)
                print(f"Issue '{title}' fechada com label '{INVALID_LABEL}': {issue.html_url}")
                count_closed += 1
            except Exception as e:
                print(f"Erro ao fechar issue '{title}': {e}")
        else:
            print(f"Issue '{title}' não encontrada no repositório.")

    print(f"{count_closed} issues fechadas com label '{INVALID_LABEL}' com base no backlog.")

if __name__ == "__main__":
    delete_issues_from_backlog()
