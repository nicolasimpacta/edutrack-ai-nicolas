# Proposal: Lógica de Cálculo de Progresso por Disciplina

## Why

Atualmente, o EduTrack AI permite cadastrar disciplinas e registrar tarefas acadêmicas, mas não possui um módulo dedicado e independente para computar o progresso percentual de conclusão por matéria a partir dos dados do backend. A criação de um script em `scripts/calculate_progress.py` que consulte as tarefas vinculadas a uma disciplina via endpoints CRUD, calcule o percentual de tarefas concluídas em relação ao total e retorne uma estrutura padronizada em JSON fornecerá uma base sólida e reutilizável para métricas, dashboards e relatórios.

## What Changes

- **Script de Cálculo de Progresso**: Criação do script `scripts/calculate_progress.py` com funções dedicadas para calcular o progresso de uma disciplina específica (e de todas as disciplinas de um aluno) com base em suas tarefas acadêmicas (`completed` vs `total`).
- **Retorno Padronizado em JSON**: Estruturação do resultado em formato JSON com campos como `subject_id`, `subject_name`, `total_tasks`, `completed_tasks`, `pending_tasks` e `progress_percentage`.
- **Consumo de Endpoints CRUD**: Utilização das rotas CRUD de disciplinas e tarefas acadêmicas (lendo a configuração de ambiente do `.env`).

## Capabilities

### New Capabilities
- `academic-progress`: Cálculo automatizado e estruturação em JSON da taxa de progresso e métricas de conclusão de tarefas vinculadas a disciplinas acadêmicas.

### Modified Capabilities

## Impact

- **Código**: Criação do diretório `scripts/` e do arquivo `scripts/calculate_progress.py`.
- **Integração**: Consumo dos endpoints CRUD configurados no `.env` (`XANO_API_BASE_URL`, `XANO_SUBJECTS_API_URL`, `XANO_TASKS_API_URL`).
