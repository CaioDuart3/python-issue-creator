from github import Github
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

# --- Configurações ---
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = os.getenv('REPO_NAME')
BACKLOG_FILE = os.getenv('BACKLOG_FILE', 'backlog.md')
ISSUE_SEPARATOR = '---'
DEFAULT_LABELS = []  # Labels padrão caso o bloco não especifique

def get_or_create_milestone(repo, milestone_title, due_date=None):
    if not milestone_title:
        return None  # Milestone opcional

    # Procurar milestone existente
    for ms in repo.get_milestones(state='open'):
        if ms.title == milestone_title:
            # Atualizar data de vencimento se fornecida
            if due_date:
                try:
                    new_due = datetime.strptime(due_date, "%Y-%m-%d")
                    if ms.due_on != new_due:
                        ms.edit(title=ms.title, state=ms.state, due_on=new_due)
                        print(f"Milestone '{milestone_title}' atualizada com vencimento {due_date}.")
                except ValueError:
                    print(f"Data de vencimento inválida para '{milestone_title}': {due_date}")
            return ms

    # Criar nova milestone se não existir
    due_on = None
    if due_date:
        try:
            due_on = datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            print(f"Data de vencimento inválida para '{milestone_title}': {due_date}")

    try:
        new_ms = repo.create_milestone(
            title=milestone_title,
            state="open",
            due_on=due_on
        )
        print(f"Milestone '{milestone_title}' criada com vencimento {due_date}.")
        return new_ms
    except Exception as e:
        print(f"Erro ao criar milestone '{milestone_title}': {e}")
        return None

def sync_github_issues_from_backlog():
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
    issues_to_process = []

    for block in issue_blocks:
        block = block.strip()
        if not block:
            continue
        lines = block.split('\n')
        title_line = next((line for line in lines if line.startswith('## ')), None)
        if title_line:
            title = title_line.replace('## ', '').strip()
            
            # Labels
            label_line = next((line for line in lines if line.lower().startswith('labels:')), "")
            labels = [lbl.strip() for lbl in label_line.replace('Labels:', '').split(',')] if label_line else DEFAULT_LABELS
            
            # Milestone (opcional)
            milestone_line = next((line for line in lines if line.lower().startswith('milestone:')), "")
            milestone_title = milestone_line.replace('Milestone:', '').strip() if milestone_line else None

            # MilestoneDue (opcional)
            due_line = next((line for line in lines if line.lower().startswith('milestonedue:')), "")
            milestone_due = due_line.replace('MilestoneDue:', '').strip() if due_line else None
            
            # Corpo da issue
            body = '\n'.join([line for line in lines if line not in [title_line, label_line, milestone_line, due_line]]).strip()
            
            issues_to_process.append({
                'title': title,
                'body': body,
                'labels': labels,
                'milestone': milestone_title,
                'milestone_due': milestone_due
            })
        else:
            print(f"Aviso: Bloco ignorado sem título: {block[:50]}...")

    if not issues_to_process:
        print("Nenhuma issue válida encontrada.")
        return

    print(f"{len(issues_to_process)} issues encontradas. Sincronizando...")

    # Buscar todas as issues (abertas e fechadas)
    existing_issues = list(repo.get_issues(state='all'))

    for issue_data in issues_to_process:
        title = issue_data['title']
        body = issue_data['body']
        labels = issue_data['labels']
        milestone_title = issue_data['milestone']
        milestone_due = issue_data['milestone_due']

        # Criar ou atualizar milestone apenas se fornecida
        milestone = get_or_create_milestone(repo, milestone_title, milestone_due) if milestone_title else None

        # Procurar issue existente pelo título
        issue_found = next((i for i in existing_issues if i.title == title), None)

        if issue_found:
            try:
                # Atualizar título, corpo, labels e milestone (pode ser None)
                issue_found.edit(title=title, body=body, labels=labels, milestone=milestone)
                # Reabrir se estiver fechada
                if issue_found.state == 'closed':
                    issue_found.edit(state='open')
                    print(f"Issue '{title}' reaberta e atualizada: {issue_found.html_url}")
                else:
                    print(f"Issue '{title}' atualizada: {issue_found.html_url}")
            except Exception as e:
                print(f"Erro ao editar issue '{title}': {e}")
        else:
            try:
                new_issue = repo.create_issue(title=title, body=body, labels=labels, milestone=milestone)
                print(f"Issue '{title}' criada: {new_issue.html_url}")
            except Exception as e:
                print(f"Erro ao criar issue '{title}': {e}")

if __name__ == "__main__":
    sync_github_issues_from_backlog()
