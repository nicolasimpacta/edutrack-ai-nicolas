# Tasks: Geração de Relatório de Desempenho em PDF

## 1. Script Python de Geração do Relatório PDF

- [x] 1.1 Adicionar `fpdf2` no arquivo `requirements.txt`
- [x] 1.2 Implementar script Python `reports/generate_report.py` para gerar PDF com nome do aluno, disciplinas, tarefas pendentes e tarefas concluídas

## 2. Endpoint no Xano para Dados do Relatório

- [x] 2.1 Criar arquivo XanoScript `api/reports/download_GET.xs` (`GET /reports/download`) com `auth = "user"` e filtro por `$auth.id`

## 3. Integração no Streamlit

- [x] 3.1 Adicionar botão `"📄 Gerar Relatório PDF"` em `pages/3_👤_Perfil.py` buscando dados do aluno no Xano e gerando o PDF com `reports/generate_report.py`
- [x] 3.2 Disponibilizar o PDF gerado para download via `st.download_button`
