## Como usuário, eu quero me cadastrar e logar no aplicativo
Critérios de Aceitação:
* O sistema deve permitir o cadastro com e-mail e senha.
* O sistema deve validar se o e-mail é único.
* O usuário deve receber um erro se tentar logar com credenciais inválidas.
* Após o login, o usuário deve ser redirecionado para a tela principal (dashboard).

---

## Como usuário, eu quero criar uma nova tarefa
Critérios de Aceitação:
* Deve haver um botão "+" visível no dashboard.
* Ao clicar, deve-se abrir um modal/formulário.
* O formulário deve ter campos para: Título (obrigatório) e Descrição (opcional).
* A nova tarefa deve aparecer no topo da lista com o status "A Fazer".

---

## Como usuário, eu quero marcar uma tarefa como concluída
Critérios de Aceitação:
* Toda tarefa deve ter uma caixa de seleção/checkbox.
* Ao clicar no checkbox, o status da tarefa deve mudar para "Concluída".
* A tarefa concluída deve ser movida para a seção de "Concluídas" ou riscada e permanecer na lista.
* O usuário deve poder desmarcar a tarefa para reabri-la.

---

## Como usuário, eu quero visualizar minhas tarefas pendentes e concluídas separadamente
Critérios de Aceitação:
* O dashboard deve ter duas seções claras: "A Fazer" e "Concluídas".
* A seção "A Fazer" deve mostrar apenas tarefas com status pendente.
* A seção "Concluídas" deve mostrar tarefas com status concluído.

---

## Como usuário, eu quero editar o título e a descrição de uma tarefa
Critérios de Aceitação:
* Deve haver uma opção/ícone "Editar" em cada tarefa.
* Ao clicar em "Editar", o formulário de criação deve ser reaberto com os dados atuais.
* O usuário deve poder salvar as alterações, atualizando a tarefa imediatamente na lista.

---

## Como usuário, eu quero deletar uma tarefa
Critérios de Aceitação:
* Deve haver um ícone de lixeira ou "Deletar" em cada tarefa.
* O sistema deve pedir uma confirmação antes de deletar ("Tem certeza que deseja deletar a tarefa 'XYZ'?").
* A tarefa deve ser removida permanentemente da lista após a confirmação.