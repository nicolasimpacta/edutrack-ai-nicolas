# Design: Geração de Relatório de Desempenho em PDF

## Context

O EduTrack AI possui arquitetura composta por frontend em Streamlit e backend no Xano. Atualmente, os dados acadêmicos do aluno (tabelas `user`, `subjects` e `academic_tasks`) estão acessíveis via API REST com isolamento por usuário (`user_id == $auth.id`).
Veja a motivação detalhada em `proposal.md`.

## Goals / Non-Goals

**Goals:**
- Implementar script Python utilitário para compilar o desempenho acadêmico do aluno e exportar para arquivo PDF formatado.
- Definir endpoint no Xano (via XanoScript) para permitir o download do arquivo de relatório sob autenticação do usuário.

**Non-Goals:**
- Cálculos complexos de notas/avaliações que não constam no esquema atual do banco de dados.
- Disparo automatizado por e-mail ou agendamento em segundo plano (escopo estritamente de geração e download sob demanda).

## Decisions

### 1. Biblioteca de Geração de PDF em Python
- **Decisão**: Utilizar `fpdf2` para a construção do relatório em PDF.
- **Justificativa**: Biblioteca leve, sem dependências de sistema operacional/binários pesados, com suporte nativo a tabelas, cabeçalhos, rodapés e renderização de layouts acadêmicos limpos.
- **Alternativas consideradas**: `reportlab` (mais complexo e verboso) e `pdfkit`/`wkhtmltopdf` (exige binário externo instalado no SO).

### 2. Estrutura do Relatório de Desempenho
O documento PDF conterá:
- **Cabeçalho**: Identificação do EduTrack AI, nome do aluno, e-mail e data de emissão.
- **Sumário Executivo**: Métricas de disciplinas matriculadas, carga horária acumulada, total de tarefas, concluídas e pendentes.
- **Seção de Disciplinas**: Tabela listando nome, professor e carga horária.
- **Seção de Tarefas Acadêmicas**: Tabela com título, matéria vinculada, prazo e status (Pendente / Concluída).

### 3. Endpoint no Xano para Download
- **Decisão**: Definir endpoint `GET /reports/download` (ou `GET /reports/performance`) no grupo de API em XanoScript.
- **Segurança**: Exigir `auth = "user"` com filtro obrigatório por `$auth.id` para impedir acesso a dados de outros alunos.

## Risks / Trade-offs

- **[Campos nulos ou sem prazo]** → Mitigação: O gerador de PDF aplica fallbacks defensivos para campos opcionais como professor, descrição ou data limite.
- **[Tamanho do conteúdo]** → Mitigação: Quebra automática de páginas e paginação estruturada no PDF.
