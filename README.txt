SISTEMA DE TRIAGE Y FLUJO DE SALA DE URGENCIAS

Archivos:
- app.py -> frontend en Streamlit
- backend.py -> lógica del sistema y estructuras de datos
- requirements.txt -> dependencia principal

Cómo ejecutarlo en Visual Studio Code:
1. Abre esta carpeta en VS Code.
2. Abre la terminal.
3. Instala Streamlit con:
   pip install -r requirements.txt
4. Ejecuta el proyecto con:
   streamlit run app.py

Estructuras de datos usadas:
- Array: camas UCI (15 posiciones fijas)
- Queue: sala de espera para triage 4 y 5
- Stack: deshacer última acción
- List: directorio dinámico de médicos
- Singly Linked List: historial de intervenciones del paciente
