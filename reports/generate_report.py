import os
from datetime import datetime
from fpdf import FPDF
from fpdf.enums import XPos, YPos


class AcademicReportPDF(FPDF):
    """Custom PDF class for EduTrack AI Academic Performance Report."""

    def __init__(self, student_name: str = "Estudante"):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.student_name = student_name
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        # Header banner
        self.set_fill_color(30, 41, 59)  # Slate-800
        self.rect(0, 0, 210, 24, "F")

        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 13)
        self.set_xy(10, 6)
        self.cell(0, 7, "EduTrack AI - Relatorio de Desempenho Academico", new_x=XPos.RIGHT, new_y=YPos.TOP)

        self.set_font("Helvetica", "", 9)
        self.set_xy(10, 13)
        now_str = datetime.now().strftime("%d/%m/%Y as %H:%M")
        self.cell(0, 5, f"Emitido em: {now_str}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(148, 163, 184)  # Slate-400
        page_str = f"Pagina {self.page_no()}/{{nb}} - EduTrack AI"
        self.cell(0, 10, page_str, align="C")


def sanitize_text(text: str | None) -> str:
    """Normalize text replacing unsupported characters for standard PDF fonts."""
    if not text:
        return ""
    replacements = {
        "ã": "a", "á": "a", "à": "a", "â": "a", "ä": "a",
        "Ã": "A", "Á": "A", "À": "A", "Â": "A", "Ä": "A",
        "é": "e", "ê": "e", "è": "e", "É": "E", "Ê": "E",
        "í": "i", "î": "i", "Í": "I", "Î": "I",
        "õ": "o", "ó": "o", "ô": "o", "ö": "o",
        "Õ": "O", "Ó": "O", "Ô": "O", "Ö": "O",
        "ú": "u", "ü": "u", "Ú": "U", "Ü": "U",
        "ç": "c", "Ç": "C",
        "—": "-", "–": "-", "“": '"', "”": '"', "’": "'"
    }
    cleaned = str(text)
    for orig, rep in replacements.items():
        cleaned = cleaned.replace(orig, rep)
    return cleaned.encode("ascii", errors="replace").decode("ascii")


def format_due_date_br(date_val) -> str:
    """Format a due_date value (timestamp or ISO date string) to DD/MM/YYYY."""
    if not date_val:
        return "Sem prazo"
    try:
        if isinstance(date_val, (int, float)):
            ts = date_val / 1000 if date_val > 1e11 else date_val
            return datetime.fromtimestamp(ts).strftime("%d/%m/%Y")
        date_str = str(date_val).strip()
        if date_str.isdigit() and len(date_str) >= 10:
            ts_num = int(date_str)
            ts = ts_num / 1000 if ts_num > 1e11 else ts_num
            return datetime.fromtimestamp(ts).strftime("%d/%m/%Y")
        if len(date_str) >= 10 and date_str[4] == "-" and date_str[7] == "-":
            return datetime.strptime(date_str[:10], "%Y-%m-%d").strftime("%d/%m/%Y")
        return sanitize_text(date_str)
    except Exception:
        return sanitize_text(str(date_val))


def generate_performance_pdf(
    student_info: dict,
    subjects: list[dict],
    tasks: list[dict],
    output_path: str | None = None
) -> bytes:
    """
    Generate an academic performance report in PDF format.
    
    :param student_info: Dict containing 'name', 'email', 'id', 'role'
    :param subjects: List of subject dicts ('name', 'teacher', 'hours')
    :param tasks: List of task dicts ('title', 'description', 'due_date', 'status', 'subject_name')
    :param output_path: Optional file path to save PDF to disk
    :return: PDF content as bytes
    """
    student_name = sanitize_text(student_info.get("name", "Estudante"))
    student_email = sanitize_text(student_info.get("email", "Nao informado"))
    student_id = sanitize_text(str(student_info.get("id", "N/A")))

    pdf = AcademicReportPDF(student_name=student_name)
    pdf.alias_nb_pages()
    pdf.add_page()

    # 1. Student Info Section
    pdf.set_fill_color(248, 250, 252)  # Slate-50
    pdf.set_draw_color(226, 232, 240)  # Slate-200
    pdf.rect(10, 28, 190, 20, "DF")

    pdf.set_text_color(15, 23, 42)  # Slate-900
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_xy(14, 31)
    pdf.cell(90, 6, f"Aluno(a): {student_name}")
    pdf.set_xy(110, 31)
    pdf.cell(85, 6, f"Identificador (ID): {student_id}")

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(71, 85, 105)  # Slate-600
    pdf.set_xy(14, 38)
    pdf.cell(90, 6, f"E-mail: {student_email}")
    pdf.set_xy(110, 38)
    role_desc = sanitize_text(student_info.get("role", "member")).capitalize()
    pdf.cell(85, 6, f"Perfil: {role_desc}")

    pdf.ln(22)

    # 2. Executive Metrics Summary
    total_subjects = len(subjects)
    total_hours = sum(int(s.get("hours") or s.get("carga_horaria") or 0) for s in subjects)

    completed_tasks = sum(1 for t in tasks if str(t.get("status", "")).lower() in ["completed", "concluida", "concluída"])
    total_tasks = len(tasks)
    pending_tasks = total_tasks - completed_tasks
    completion_rate = int((completed_tasks / total_tasks * 100)) if total_tasks > 0 else 0

    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 6, "Resumo Academico", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1)

    # 4 Metric Cards
    card_width = 45
    card_height = 16
    spacing = 3.3
    x_start = 10
    y_pos = pdf.get_y()

    metrics = [
        ("Disciplinas", str(total_subjects), (59, 130, 246)),     # Blue
        ("Carga Horaria", f"{total_hours}h", (16, 185, 129)),     # Green
        ("Tarefas Feitas", f"{completed_tasks}/{total_tasks}", (139, 92, 246)),  # Purple
        ("Taxa Conclusao", f"{completion_rate}%", (245, 158, 11))  # Amber
    ]

    for i, (label, val, border_col) in enumerate(metrics):
        cx = x_start + i * (card_width + spacing)
        pdf.set_fill_color(248, 250, 252)
        pdf.set_draw_color(*border_col)
        pdf.rect(cx, y_pos, card_width, card_height, "DF")

        pdf.set_xy(cx + 2, y_pos + 2)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(card_width - 4, 4, label)

        pdf.set_xy(cx + 2, y_pos + 7)
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(card_width - 4, 7, val)

    pdf.set_y(y_pos + card_height + 6)

    # 3. Disciplinas Table
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 6, "Disciplinas Matriculadas", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1)

    # Table Header
    pdf.set_fill_color(241, 245, 249)
    pdf.set_draw_color(203, 213, 225)
    pdf.set_text_color(51, 65, 85)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(90, 7, "  Disciplina", border=1, fill=True)
    pdf.cell(65, 7, "  Professor(a)", border=1, fill=True)
    pdf.cell(35, 7, "  Carga Horaria", border=1, fill=True, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(30, 41, 59)

    if not subjects:
        pdf.cell(190, 7, "Nenhuma disciplina cadastrada.", border=1, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    else:
        for s in subjects:
            s_name = sanitize_text(s.get("name", "Sem Nome"))
            s_teacher = sanitize_text(s.get("teacher") or s.get("professor") or "Nao informado")
            s_hours = f"{s.get('hours') or s.get('carga_horaria') or 0} horas"

            pdf.cell(90, 6, f"  {s_name}", border=1)
            pdf.cell(65, 6, f"  {s_teacher}", border=1)
            pdf.cell(35, 6, s_hours, border=1, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(6)

    # 4. Tarefas Acadêmicas Table
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 6, "Obrigacoes e Tarefas Academicas", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1)

    # Table Header
    pdf.set_fill_color(241, 245, 249)
    pdf.set_draw_color(203, 213, 225)
    pdf.set_text_color(51, 65, 85)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(75, 7, "  Titulo da Tarefa", border=1, fill=True)
    pdf.cell(55, 7, "  Materia", border=1, fill=True)
    pdf.cell(32, 7, "  Prazo", border=1, fill=True, align="C")
    pdf.cell(28, 7, "  Status", border=1, fill=True, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(30, 41, 59)

    if not tasks:
        pdf.cell(190, 7, "Nenhuma tarefa academica registrada.", border=1, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    else:
        subjects_by_id = {
            s.get("id"): s.get("name")
            for s in subjects
            if isinstance(s, dict) and s.get("id") is not None
        }
        for t in tasks:
            t_title = sanitize_text(t.get("title", "Sem titulo"))
            raw_subject = t.get("subject_name") or subjects_by_id.get(t.get("subject_id")) or "Geral"
            t_subject = sanitize_text(raw_subject)
            t_date = format_due_date_br(t.get("due_date") or t.get("deadline"))
            t_status_raw = str(t.get("status", "pending")).lower()

            if t_status_raw in ["completed", "concluida", "concluída"]:
                status_label = "Concluida"
            else:
                status_label = "Pendente"

            if len(t_title) > 42:
                t_title = t_title[:39] + "..."
            if len(t_subject) > 28:
                t_subject = t_subject[:25] + "..."

            pdf.cell(75, 6, f"  {t_title}", border=1)
            pdf.cell(55, 6, f"  {t_subject}", border=1)
            pdf.cell(32, 6, t_date, border=1, align="C")

            if status_label == "Concluida":
                pdf.set_text_color(22, 101, 52)  # Green-800
            else:
                pdf.set_text_color(180, 83, 9)   # Amber-700
            pdf.cell(28, 6, status_label, border=1, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_text_color(30, 41, 59)

    pdf_bytes = bytes(pdf.output())

    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(pdf_bytes)

    return pdf_bytes


if __name__ == "__main__":
    sample_student = {
        "id": 1,
        "name": "Lucas Ferreira da Silva",
        "email": "lucas.silva@edutrack.ai",
        "role": "aluno"
    }
    sample_subjects = [
        {"id": 1, "name": "Estruturas de Dados", "teacher": "Prof. Carlos Silva", "hours": 80},
        {"id": 2, "name": "Engenharia de Software", "teacher": "Profa. Mariana Costa", "hours": 60},
        {"id": 3, "name": "Banco de Dados", "teacher": "Prof. Roberto Mendes", "hours": 80}
    ]
    sample_tasks = [
        {"id": 1, "title": "Implementar Arvore Binaria", "subject_name": "Estruturas de Dados", "due_date": "2026-11-20", "status": "completed"},
        {"id": 2, "title": "Diagrama de Casos de Uso", "subject_name": "Engenharia de Software", "due_date": "2026-11-25", "status": "pending"},
        {"id": 3, "title": "Normalizacao 3FN", "subject_name": "Banco de Dados", "due_date": "2026-11-28", "status": "completed"},
        {"id": 4, "title": "Relatorio Final de Projeto", "subject_name": "Engenharia de Software", "due_date": "2026-12-05", "status": "pending"}
    ]

    out_file = "sample_relatorio_desempenho.pdf"
    res_bytes = generate_performance_pdf(sample_student, sample_subjects, sample_tasks, output_path=out_file)
    print(f"Relatorio PDF gerado com sucesso! Tamanho: {len(res_bytes)} bytes em '{out_file}'")
