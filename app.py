import os
import streamlit as st

# Configuração da Página (Título na aba do navegador)
st.set_page_config(page_title="EduTrack AI", page_icon="🎓", layout="wide")

# Inicialização de Estado da Sessão para Disciplinas
if "subjects" not in st.session_state:
    st.session_state.subjects = [
        {
            "id": 1,
            "name": "Estruturas de Dados",
            "code": "CC201",
            "professor": "Prof. Carlos Silva",
            "workload_hours": 80,
            "semester": "2026.1",
            "color": "#3B82F6",
            "status": "active"
        },
        {
            "id": 2,
            "name": "Engenharia de Software",
            "code": "ES302",
            "professor": "Profa. Mariana Costa",
            "workload_hours": 60,
            "semester": "2026.1",
            "color": "#10B981",
            "status": "active"
        }
    ]

# Título Principal
st.title("🎓 EduTrack AI")

# Sidebar (Menu Lateral)
st.sidebar.header("Menu")
menu_option = st.sidebar.radio("Navegar", ["Dashboard", "Disciplinas", "Tarefas"])

# Cálculos de Métricas
active_subjects = [s for s in st.session_state.subjects if s.get("status") == "active"]
completed_subjects = [s for s in st.session_state.subjects if s.get("status") == "completed"]

# Conteúdo Dinâmico
if menu_option == "Dashboard":
    st.write("Bem-vindo ao seu assistente acadêmico!")
    st.info("💡 Backend Xano configurável via endpoint REST de Disciplinas (`/subjects`).")
    
    # Métricas Visuais Dinâmicas
    col1, col2, col3 = st.columns(3)
    col1.metric("Disciplinas Ativas", len(active_subjects))
    col2.metric("Disciplinas Concluídas", len(completed_subjects))
    col3.metric("Tarefas Pendentes", "0")

    if active_subjects:
        st.subheader("📚 Suas Disciplinas Ativas")
        cols = st.columns(min(len(active_subjects), 3))
        for idx, subj in enumerate(active_subjects):
            with cols[idx % len(cols)]:
                st.markdown(
                    f"""
                    <div style="border-left: 5px solid {subj.get('color', '#3B82F6')}; padding: 12px; background-color: #f8fafc; border-radius: 6px; margin-bottom: 10px;">
                        <h4 style="margin: 0; color: #1e293b;">{subj['name']} ({subj.get('code', 'N/A')})</h4>
                        <p style="margin: 4px 0; color: #64748b; font-size: 0.9em;">👨‍🏫 {subj.get('professor', 'Não informado')}</p>
                        <p style="margin: 2px 0; color: #64748b; font-size: 0.85em;">⏱️ {subj.get('workload_hours', 0)}h | 📅 {subj.get('semester', 'Semestre Atual')}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

elif menu_option == "Disciplinas":
    st.subheader("Minhas Disciplinas")
    st.write("Gerencie suas matérias acadêmicas, cargas horárias e professores.")

    # Filtros e Formulário de Adição
    tab_list, tab_add = st.tabs(["📋 Lista de Disciplinas", "➕ Nova Disciplina"])

    with tab_list:
        status_filter = st.selectbox("Filtrar por status", ["Todas", "Ativas", "Concluídas"])
        filtered_subjects = st.session_state.subjects
        if status_filter == "Ativas":
            filtered_subjects = active_subjects
        elif status_filter == "Concluídas":
            filtered_subjects = completed_subjects

        if not filtered_subjects:
            st.info("Nenhuma disciplina encontrada para este filtro.")
        else:
            for s in filtered_subjects:
                with st.expander(f"{s['name']} ({s.get('code', 'S/ Código')}) - Status: {s.get('status').title()}", expanded=True):
                    c1, c2, c3 = st.columns(3)
                    c1.write(f"**Professor:** {s.get('professor', 'Não informado')}")
                    c2.write(f"**Carga Horária:** {s.get('workload_hours', 0)} horas")
                    c3.write(f"**Semestre:** {s.get('semester', 'N/A')}")
                    
                    btn_col1, btn_col2 = st.columns([1, 1])
                    with btn_col1:
                        if s.get("status") == "active":
                            if st.button("Marcar como Concluída", key=f"finish_{s['id']}"):
                                s["status"] = "completed"
                                st.rerun()
                        else:
                            if st.button("Reativar Disciplina", key=f"reactivate_{s['id']}"):
                                s["status"] = "active"
                                st.rerun()
                    with btn_col2:
                        if st.button("Excluir Disciplina", key=f"del_{s['id']}", type="secondary"):
                            st.session_state.subjects = [item for item in st.session_state.subjects if item["id"] != s["id"]]
                            st.rerun()

    with tab_add:
        st.write("Preencha os dados abaixo para cadastrar uma nova disciplina:")
        with st.form("new_subject_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            with col_a:
                sub_name = st.text_input("Nome da Disciplina *", placeholder="Ex: Cálculo I")
                sub_code = st.text_input("Código da Matéria", placeholder="Ex: MAT101")
                sub_prof = st.text_input("Nome do Professor", placeholder="Ex: Dr. Roberto Mendes")
            with col_b:
                sub_workload = st.number_input("Carga Horária (horas)", min_value=0, max_value=400, value=60, step=10)
                sub_semester = st.text_input("Semestre / Período", placeholder="Ex: 2026.1")
                sub_color = st.color_picker("Cor de Identificação", value="#4F46E5")

            submit_btn = st.form_submit_button("Cadastrar Disciplina")
            if submit_btn:
                if not sub_name.strip():
                    st.error("O nome da disciplina é obrigatório.")
                else:
                    new_id = max([item["id"] for item in st.session_state.subjects], default=0) + 1
                    st.session_state.subjects.append({
                        "id": new_id,
                        "name": sub_name.strip(),
                        "code": sub_code.strip() if sub_code else None,
                        "professor": sub_prof.strip() if sub_prof else None,
                        "workload_hours": int(sub_workload),
                        "semester": sub_semester.strip() if sub_semester else None,
                        "color": sub_color,
                        "status": "active"
                    })
                    st.success(f"Disciplina '{sub_name}' cadastrada com sucesso!")
                    st.rerun()

elif menu_option == "Tarefas":
    st.subheader("Gerenciamento de Tarefas")
    st.checkbox("Exemplo: Estudar Streamlit")