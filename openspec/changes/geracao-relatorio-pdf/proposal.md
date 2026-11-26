# Proposal: Geração de Relatório de Desempenho em PDF

## Why

Atualmente, os alunos do EduTrack AI conseguem visualizar suas disciplinas e tarefas na interface interativa, mas não possuem uma forma padronizada de exportar, compartilhar ou arquivar um documento formal consolidando seu progresso acadêmico. A geração de um relatório em PDF com o desempenho acadêmico e um endpoint no Xano para download desse arquivo proporcionará aos estudantes um registro portátil e oficial de suas matérias, tarefas e status de conclusão.

## What Changes

- **Script Python de Geração de PDF**: Criação de um utilitário isolado em Python (`reports/generate_report.py`) que compila dados do aluno (nome, disciplinas matriculadas, tarefas pendentes, tarefas concluídas e métricas de progresso) e gera um relatório formatado em PDF com `fpdf2`.
- **Integração no Streamlit**: Adição da seção de geração de relatório na página `pages/3_👤_Perfil.py` com o botão `"📄 Gerar Relatório PDF"`, busca dos dados do aluno via Xano e disponibilização do arquivo via `st.download_button`.
- **Endpoint no Xano para Dados do Relatório**: Criação de um endpoint de API autenticado no Xano (`GET /reports/download`) que retorna o JSON consolidado do aluno (`student`, `subjects`, `tasks`) para o relatório.

## Capabilities

### New Capabilities
- `student-reports`: Geração de relatório em PDF contendo o desempenho acadêmico do aluno, integração no Streamlit para geração/download e endpoint autenticado no Xano para obtenção dos dados.

### Modified Capabilities

## Impact

- **Frontend (Streamlit)**: Atualização de `pages/3_👤_Perfil.py` com botão de geração e download do PDF para usuários autenticados.
- **Backend (Xano)**: Novo endpoint no XanoScript (`api/reports/download_GET.xs`) para retornar os dados consolidados do relatório sob autenticação do aluno (`user_id`).
- **Python / Scripts**: Script `reports/generate_report.py` utilizando `fpdf2`.
- **Dependências**: Inclusão de `fpdf2>=2.8.0` em `requirements.txt`.
