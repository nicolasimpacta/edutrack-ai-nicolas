# Proposal: Geração de Relatório de Desempenho em PDF

## Why

Atualmente, os alunos do EduTrack AI conseguem visualizar suas disciplinas e tarefas na interface interativa, mas não possuem uma forma padronizada de exportar, compartilhar ou arquivar um documento formal consolidando seu progresso acadêmico. A geração de um relatório em PDF com o desempenho acadêmico e um endpoint no Xano para download desse arquivo proporcionará aos estudantes um registro portátil e oficial de suas matérias, tarefas e status de conclusão.

## What Changes

- **Script Python de Geração de PDF**: Criação de um utilitário em Python (`reports/student_performance_report.py` ou integrado ao app) que compila dados do aluno (disciplinas matriculadas, tarefas pendentes, tarefas concluídas e métricas de progresso) e gera um relatório formatado em PDF.
- **Endpoint no Xano para Download de Relatório**: Criação de um endpoint de API autenticado no Xano (`GET /reports/performance` ou `/reports/download`) que disponibiliza o arquivo PDF gerado para download pelo aluno autenticado.

## Capabilities

### New Capabilities
- `student-reports`: Geração de relatório em PDF contendo o desempenho acadêmico do aluno e disponibilização via endpoint de API para download seguro.

### Modified Capabilities

## Impact

- **Backend (Xano)**: Novo endpoint no XanoScript para servir o arquivo/conteúdo do relatório PDF sob autenticação do aluno (`user_id`).
- **Python / Scripts**: Criação do script de geração de PDF utilizando bibliotecas padrão/Python (ex: `fpdf2` ou `reportlab`).
- **Dependências**: Adição da biblioteca de geração de PDF nas dependências do projeto.
