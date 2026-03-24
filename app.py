import streamlit as st

from backend import HospitalSystem


st.set_page_config(
    page_title="Sistema de Triage y Flujo",
    layout="wide",
)


CSS = """
<style>
:root {
    --primary: #f97316;
    --primary-dark: #ea580c;
    --danger: #dc2626;
    --danger-soft: #fee2e2;
    --surface: #ffffff;
    --surface-alt: #fff7ed;
    --border: #fed7aa;
    --text: #1f2937;
    --muted: #6b7280;
}

.stApp {
    background: linear-gradient(180deg, #fff7ed 0%, #ffffff 18%, #fff1f2 100%);
    color: var(--text);
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 1.6rem;
    max-width: 1420px;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff 0%, #fff7ed 100%);
    border-right: 1px solid var(--border);
}

.main-title {
    background: linear-gradient(135deg, #ffffff 0%, #fff7ed 55%, #fee2e2 100%);
    border: 1px solid var(--border);
    border-radius: 22px;
    padding: 22px 24px;
    margin-bottom: 1rem;
    box-shadow: 0 10px 30px rgba(234, 88, 12, 0.08);
}

.section-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text);
    margin: 0 0 0.8rem 0;
}

.panel {
    background: rgba(255,255,255,0.92);
    border: 1px solid #fde3c3;
    border-radius: 20px;
    padding: 18px;
    box-shadow: 0 12px 30px rgba(15, 23, 42, 0.05);
    min-height: 100%;
}

.info-card {
    background: var(--surface);
    border: 1px solid #fde3c3;
    border-radius: 16px;
    padding: 14px;
    margin-bottom: 10px;
    box-shadow: 0 6px 14px rgba(15, 23, 42, 0.04);
}

.bed-card {
    background: var(--surface);
    border-radius: 16px;
    padding: 14px;
    min-height: 112px;
    border: 1px solid #fde3c3;
    box-shadow: 0 6px 14px rgba(15, 23, 42, 0.04);
}

.bed-free {
    border-top: 5px solid var(--primary);
    background: linear-gradient(180deg, #ffffff 0%, #fff7ed 100%);
}

.bed-busy {
    border-top: 5px solid var(--danger);
    background: linear-gradient(180deg, #ffffff 0%, #fff1f2 100%);
}

.label {
    color: var(--muted);
    font-size: 0.82rem;
    margin-bottom: 4px;
}

.value {
    color: var(--text);
    font-size: 1rem;
    font-weight: 600;
}

.log-item {
    background: #fffaf5;
    border: 1px solid #fde3c3;
    border-radius: 14px;
    padding: 10px 12px;
    margin-bottom: 8px;
    color: var(--text);
}

.patient-item {
    background: #ffffff;
    border: 1px solid #fde3c3;
    border-left: 5px solid var(--primary);
    border-radius: 14px;
    padding: 12px;
    margin-bottom: 10px;
}

.profile-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
    margin-bottom: 14px;
}

.profile-box {
    background: #fffaf5;
    border: 1px solid #fde3c3;
    border-radius: 14px;
    padding: 12px;
}

.stButton > button,
.stDownloadButton > button,
div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 600;
    box-shadow: 0 8px 18px rgba(234, 88, 12, 0.20);
}

.stButton > button:hover,
.stDownloadButton > button:hover,
div[data-testid="stFormSubmitButton"] > button:hover {
    background: linear-gradient(135deg, var(--primary-dark) 0%, #c2410c 100%);
}

div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.92);
    border: 1px solid #fde3c3;
    padding: 14px;
    border-radius: 18px;
    box-shadow: 0 8px 18px rgba(15, 23, 42, 0.04);
}

h1, h2, h3 {
    color: var(--text);
}

small, .muted {
    color: var(--muted);
}

label, .stSelectbox label, .stTextInput label, .stNumberInput label, .stTextArea label {
    color: #374151 !important;
    font-weight: 600 !important;
}

section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div {
    color: #1f2937;
}

section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea,
section[data-testid="stSidebar"] [data-baseweb="select"] > div,
section[data-testid="stSidebar"] [data-baseweb="input"] > div,
section[data-testid="stSidebar"] div[data-baseweb="base-input"] {
    background: #ffffff !important;
    color: #111827 !important;
    border: 1px solid #fdba74 !important;
    border-radius: 12px !important;
}

section[data-testid="stSidebar"] input::placeholder,
section[data-testid="stSidebar"] textarea::placeholder {
    color: #9ca3af !important;
}

section[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #111827 !important;
}

section[data-testid="stSidebar"] .stNumberInput button {
    background: #fff7ed !important;
    color: #9a3412 !important;
    border: 1px solid #fdba74 !important;
}

section[data-testid="stSidebar"] .stSuccess,
section[data-testid="stSidebar"] .stError,
section[data-testid="stSidebar"] .stWarning,
section[data-testid="stSidebar"] .stInfo {
    color: #111827 !important;
}

div[data-testid="stMetric"] label,
div[data-testid="stMetric"] div,
div[data-testid="stMetric"] p {
    color: #1f2937 !important;
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

if "hospital" not in st.session_state:
    st.session_state.hospital = HospitalSystem()

hospital: HospitalSystem = st.session_state.hospital


def patient_options():
    return list(hospital.patients.keys())


def patient_label(pid: str) -> str:
    patient = hospital.patients[pid]
    return f"{pid} - {patient.name}"


with st.sidebar:
    st.markdown("## Panel de control")
    st.caption("Gestión de pacientes, camas, cola y médicos")

    if st.button("Cargar datos de ejemplo", use_container_width=True):
        hospital.seed_demo_data()
        st.success("Se cargaron datos de ejemplo.")

    st.divider()
    st.markdown("### Registrar paciente")
    with st.form("form_register"):
        name = st.text_input("Nombre")
        age = st.number_input("Edad", min_value=0, max_value=120, value=25)
        triage = st.selectbox("Nivel de triage", [1, 2, 3, 4, 5], index=3)
        reason = st.text_input("Motivo de ingreso")
        submit_patient = st.form_submit_button("Registrar paciente", use_container_width=True)
        if submit_patient:
            if name.strip() and reason.strip():
                patient = hospital.register_patient(name, int(age), int(triage), reason)
                st.success(f"Paciente registrado: {patient.name} ({patient.patient_id})")
            else:
                st.error("Completa nombre y motivo de ingreso.")

    st.divider()
    st.markdown("### Asignar cama")
    options = patient_options()
    with st.form("form_bed"):
        selected_patient = (
            st.selectbox("Paciente", options, format_func=patient_label) if options else None
        )
        bed_number = st.number_input("Número de cama", min_value=1, max_value=hospital.total_beds, value=1)
        doctor_bed = st.selectbox("Doctor encargado", hospital.doctors if hospital.doctors else ["Sin asignar"])
        submit_bed = st.form_submit_button("Asignar cama", use_container_width=True)
        if submit_bed:
            if selected_patient is None:
                st.error("No hay pacientes registrados.")
            else:
                ok, message = hospital.assign_bed(selected_patient, int(bed_number) - 1, doctor_bed)
                (st.success if ok else st.error)(message)

    st.markdown("### Atender siguiente en cola")
    with st.form("form_next_queue"):
        queue_bed = st.number_input("Cama para el siguiente paciente", min_value=1, max_value=hospital.total_beds, value=2)
        queue_doctor = st.selectbox(
            "Doctor encargado de la atención",
            hospital.doctors if hospital.doctors else ["Sin asignar"],
            key="queue_doctor",
        )
        submit_next_queue = st.form_submit_button("Pasar siguiente", use_container_width=True)
        if submit_next_queue:
            ok, message = hospital.attend_next_from_queue(int(queue_bed) - 1, queue_doctor)
            (st.success if ok else st.error)(message)

    st.divider()
    st.markdown("### Actualizar signos vitales")
    with st.form("form_vitals"):
        options = patient_options()
        vitals_patient = (
            st.selectbox("Paciente", options, format_func=patient_label, key="vitals_patient") if options else None
        )
        temp = st.number_input("Temperatura", min_value=30.0, max_value=45.0, value=36.5, step=0.1)
        heart = st.number_input("Frecuencia cardiaca", min_value=20, max_value=220, value=80)
        oxygen = st.number_input("Saturación de oxígeno", min_value=50, max_value=100, value=98)
        submit_vitals = st.form_submit_button("Guardar signos vitales", use_container_width=True)
        if submit_vitals:
            if vitals_patient is None:
                st.error("No hay pacientes registrados.")
            else:
                ok, message = hospital.update_vitals(vitals_patient, float(temp), int(heart), int(oxygen))
                (st.success if ok else st.error)(message)

    st.divider()
    st.markdown("### Intervención del paciente")
    with st.form("form_intervention"):
        options = patient_options()
        history_patient = (
            st.selectbox("Paciente", options, format_func=patient_label, key="history_patient") if options else None
        )
        procedure = st.text_input("Procedimiento")
        submit_history = st.form_submit_button("Agregar intervención", use_container_width=True)
        if submit_history:
            if history_patient is None:
                st.error("No hay pacientes registrados.")
            else:
                ok, message = hospital.add_intervention(history_patient, procedure)
                (st.success if ok else st.error)(message)

    st.divider()
    st.markdown("### Dar alta")
    with st.form("form_discharge"):
        options = patient_options()
        discharge_patient = (
            st.selectbox("Paciente", options, format_func=patient_label, key="discharge_patient") if options else None
        )
        submit_discharge = st.form_submit_button("Dar alta", use_container_width=True)
        if submit_discharge:
            if discharge_patient is None:
                st.error("No hay pacientes registrados.")
            else:
                ok, message = hospital.discharge_patient(discharge_patient)
                (st.success if ok else st.error)(message)

    st.divider()
    st.markdown("### Médicos de turno")
    with st.form("form_doctor_add"):
        doctor_name = st.text_input("Agregar médico")
        submit_add_doctor = st.form_submit_button("Agregar médico", use_container_width=True)
        if submit_add_doctor:
            result = hospital.add_doctor(doctor_name)
            if "correctamente" in result:
                st.success(result)
            else:
                st.error(result)

    if hospital.doctors:
        doctor_remove = st.selectbox("Eliminar médico", hospital.doctors, key="doctor_remove")
        if st.button("Eliminar médico", use_container_width=True):
            result = hospital.remove_doctor(doctor_remove)
            st.info(result)

    search_text = st.text_input("Buscar médico")
    if search_text:
        results = hospital.search_doctor(search_text)
        if results:
            for doctor in results:
                st.write(f"• {doctor}")
        else:
            st.write("Sin resultados.")

    st.divider()
    if st.button("Deshacer última acción", use_container_width=True):
        ok, message = hospital.undo_last_action()
        (st.success if ok else st.warning)(message)


st.markdown(
    """
    <div class="main-title">
        <div style="font-size: 2rem; font-weight: 800; margin-bottom: 0.35rem;">Sistema de Triage y Flujo de Sala de Urgencias</div>
        <div class="muted" style="font-size: 1rem;">Panel clínico para registro, asignación de camas, cola de espera, signos vitales e historial de atención.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Pacientes activos", hospital.active_patients())
m2.metric("Camas disponibles", hospital.available_beds())
m3.metric("Pacientes en cola", len(hospital.waiting_queue))
m4.metric("Médicos de turno", len(hospital.doctors))

st.write("")
left, right = st.columns([1.3, 1])

with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Panel de camas UCI</div>', unsafe_allow_html=True)
    for row_start in range(0, hospital.total_beds, 5):
        cols = st.columns(5)
        for i in range(5):
            bed_index = row_start + i
            if bed_index >= hospital.total_beds:
                continue
            patient_id = hospital.beds[bed_index]
            if patient_id is None:
                html = f"""
                <div class="bed-card bed-free">
                    <div class="label">Cama</div>
                    <div class="value">{bed_index + 1}</div>
                    <div class="label" style="margin-top: 12px;">Estado</div>
                    <div class="value">Libre</div>
                </div>
                """
            else:
                patient = hospital.patients[patient_id]
                html = f"""
                <div class="bed-card bed-busy">
                    <div class="label">Cama</div>
                    <div class="value">{bed_index + 1}</div>
                    <div class="label" style="margin-top: 12px;">Paciente</div>
                    <div class="value">{patient.name}</div>
                    <div class="label">ID {patient.patient_id}</div>
                </div>
                """
            cols[i].markdown(html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Cola de espera</div>', unsafe_allow_html=True)
    waiting_patients = hospital.get_waiting_patients()
    if waiting_patients:
        for position, patient in enumerate(waiting_patients, start=1):
            st.markdown(
                f"""
                <div class="patient-item">
                    <div style="font-weight: 700; margin-bottom: 4px;">{position}. {patient.name}</div>
                    <div class="muted">ID: {patient.patient_id} | Triage: {patient.triage_level}</div>
                    <div style="margin-top: 6px;">Motivo: {patient.reason}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("No hay pacientes en la cola de espera.")
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")
bottom_left, bottom_right = st.columns([1, 1])

with bottom_left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Registro de acciones</div>', unsafe_allow_html=True)
    if hospital.action_log:
        for entry in reversed(hospital.action_log[-12:]):
            st.markdown(f'<div class="log-item">{entry}</div>', unsafe_allow_html=True)
    else:
        st.info("Aún no se registran acciones.")
    st.markdown("</div>", unsafe_allow_html=True)

with bottom_right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Perfil del paciente</div>', unsafe_allow_html=True)
    options = patient_options()
    if options:
        profile_patient_id = st.selectbox(
            "Selecciona un paciente",
            options,
            format_func=patient_label,
        )
        patient = hospital.patients[profile_patient_id]
        vitals = patient.last_vitals

        st.markdown(
            f"""
            <div class="profile-grid">
                <div class="profile-box"><div class="label">Nombre</div><div class="value">{patient.name}</div></div>
                <div class="profile-box"><div class="label">Edad</div><div class="value">{patient.age}</div></div>
                <div class="profile-box"><div class="label">Triage</div><div class="value">{patient.triage_level}</div></div>
                <div class="profile-box"><div class="label">Estado</div><div class="value">{patient.status}</div></div>
                <div class="profile-box"><div class="label">Médico</div><div class="value">{patient.assigned_doctor}</div></div>
                <div class="profile-box"><div class="label">Cama</div><div class="value">{'Sin asignar' if patient.bed_index is None else patient.bed_index + 1}</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="info-card"><div class="label">Motivo de ingreso</div><div class="value">{}</div></div>'.format(patient.reason), unsafe_allow_html=True)

        st.markdown("#### Signos vitales")
        st.markdown(
            f"""
            <div class="profile-grid">
                <div class="profile-box"><div class="label">Temperatura</div><div class="value">{vitals['temperature'] if vitals['temperature'] is not None else 'Sin registro'}</div></div>
                <div class="profile-box"><div class="label">Frecuencia cardiaca</div><div class="value">{vitals['heart_rate'] if vitals['heart_rate'] is not None else 'Sin registro'}</div></div>
                <div class="profile-box"><div class="label">Saturación de oxígeno</div><div class="value">{vitals['oxygen'] if vitals['oxygen'] is not None else 'Sin registro'}</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("#### Historial de intervenciones")
        history = hospital.get_patient_history(profile_patient_id)
        if history:
            for step_number, item in enumerate(history, start=1):
                st.markdown(
                    f'<div class="log-item">{step_number}. {item}</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.write("Sin intervenciones registradas.")
    else:
        st.info("Todavía no hay pacientes registrados.")
    st.markdown("</div>", unsafe_allow_html=True)
