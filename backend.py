from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Patient:
    patient_id: str
    name: str
    age: int
    triage_level: int
    reason: str
    status: str = "Registrado"
    bed_index: Optional[int] = None
    assigned_doctor: str = "Sin asignar"
    last_vitals: dict = field(
        default_factory=lambda: {
            "temperature": None,
            "heart_rate": None,
            "oxygen": None,
        }
    )


class HistoryNode:
    def __init__(self, procedure: str):
        self.procedure = procedure
        self.next: Optional[HistoryNode] = None


class SinglyLinkedList:
    def __init__(self):
        self.head: Optional[HistoryNode] = None

    def append(self, procedure: str) -> None:
        new_node = HistoryNode(procedure)
        if self.head is None:
            self.head = new_node
            return

        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_node

    def to_list(self) -> list[str]:
        items: list[str] = []
        current = self.head
        while current is not None:
            items.append(current.procedure)
            current = current.next
        return items


class HospitalSystem:
    def __init__(self, total_beds: int = 15):
        self.total_beds = total_beds
        self.beds: list[Optional[str]] = [None] * total_beds  # Array fijo
        self.waiting_queue: deque[str] = deque()  # Queue
        self.undo_stack: list[dict] = []  # Stack
        self.doctors: list[str] = []  # Lista nativa
        self.patients: dict[str, Patient] = {}
        self.histories: dict[str, SinglyLinkedList] = {}
        self.action_log: list[str] = []
        self.patient_counter = 1

    def _next_patient_id(self) -> str:
        patient_id = f"P{self.patient_counter:03d}"
        self.patient_counter += 1
        return patient_id

    def _remove_from_queue_if_present(self, patient_id: str) -> bool:
        try:
            self.waiting_queue.remove(patient_id)
            return True
        except ValueError:
            return False

    def add_doctor(self, name: str) -> str:
        clean_name = name.strip()
        if not clean_name:
            return "Escribe un nombre válido."
        if clean_name in self.doctors:
            return "Ese doctor ya está en turno."
        self.doctors.append(clean_name)
        self.action_log.append(f"Doctor agregado al turno: {clean_name}")
        return "Doctor agregado correctamente."

    def remove_doctor(self, name: str) -> str:
        if name in self.doctors:
            self.doctors.remove(name)
            self.action_log.append(f"Doctor retirado del turno: {name}")
            return "Doctor eliminado del turno."
        return "No se encontró ese doctor."

    def search_doctor(self, text: str) -> list[str]:
        query = text.lower().strip()
        return [doctor for doctor in self.doctors if query in doctor.lower()]

    def register_patient(self, name: str, age: int, triage_level: int, reason: str) -> Patient:
        patient_id = self._next_patient_id()
        patient = Patient(patient_id, name.strip(), age, triage_level, reason.strip())
        self.patients[patient_id] = patient
        self.histories[patient_id] = SinglyLinkedList()
        self.histories[patient_id].append("Triage")

        if triage_level in (4, 5):
            patient.status = "En sala de espera"
            self.waiting_queue.append(patient_id)
            self.action_log.append(
                f"Paciente {patient.name} ({patient_id}) agregado a la cola de espera."
            )
        else:
            patient.status = "Pendiente de cama"
            self.action_log.append(
                f"Paciente {patient.name} ({patient_id}) registrado con prioridad alta."
            )

        return patient

    def assign_bed(self, patient_id: str, bed_index: int, doctor_name: str = "Sin asignar") -> tuple[bool, str]:
        if patient_id not in self.patients:
            return False, "Paciente no encontrado."
        if not (0 <= bed_index < self.total_beds):
            return False, "Índice de cama inválido."
        if self.beds[bed_index] is not None:
            return False, "La cama ya está ocupada."

        patient = self.patients[patient_id]
        previous_bed = patient.bed_index
        removed_from_queue = self._remove_from_queue_if_present(patient_id)

        self.beds[bed_index] = patient_id
        patient.bed_index = bed_index
        patient.assigned_doctor = doctor_name
        patient.status = "En atención"

        self.undo_stack.append(
            {
                "type": "assign_bed",
                "patient_id": patient_id,
                "bed_index": bed_index,
                "previous_bed": previous_bed,
                "removed_from_queue": removed_from_queue,
                "previous_status": "En sala de espera" if removed_from_queue else "Pendiente de cama",
                "previous_doctor": "Sin asignar",
            }
        )

        self.action_log.append(
            f"Paciente {patient.name} ({patient_id}) asignado a cama {bed_index + 1}."
        )
        return True, "Cama asignada correctamente."

    def attend_next_from_queue(self, bed_index: int, doctor_name: str = "Sin asignar") -> tuple[bool, str]:
        if not self.waiting_queue:
            return False, "No hay pacientes en cola."
        next_patient_id = self.waiting_queue[0]
        success, message = self.assign_bed(next_patient_id, bed_index, doctor_name)
        return success, message

    def discharge_patient(self, patient_id: str) -> tuple[bool, str]:
        if patient_id not in self.patients:
            return False, "Paciente no encontrado."

        patient = self.patients[patient_id]
        if patient.status == "Alta médica":
            return False, "El paciente ya fue dado de alta."

        bed_index = patient.bed_index
        was_in_queue = self._remove_from_queue_if_present(patient_id)
        old_status = patient.status
        old_doctor = patient.assigned_doctor

        if bed_index is not None:
            self.beds[bed_index] = None

        patient.bed_index = None
        patient.status = "Alta médica"
        patient.assigned_doctor = "Sin asignar"

        self.undo_stack.append(
            {
                "type": "discharge",
                "patient_id": patient_id,
                "bed_index": bed_index,
                "old_status": old_status,
                "old_doctor": old_doctor,
                "was_in_queue": was_in_queue,
            }
        )

        self.action_log.append(f"Paciente {patient.name} ({patient_id}) dado de alta.")
        return True, "Alta registrada correctamente."

    def update_vitals(self, patient_id: str, temperature: float, heart_rate: int, oxygen: int) -> tuple[bool, str]:
        if patient_id not in self.patients:
            return False, "Paciente no encontrado."

        patient = self.patients[patient_id]
        previous_vitals = dict(patient.last_vitals)
        patient.last_vitals = {
            "temperature": temperature,
            "heart_rate": heart_rate,
            "oxygen": oxygen,
        }

        self.undo_stack.append(
            {
                "type": "vitals",
                "patient_id": patient_id,
                "previous_vitals": previous_vitals,
            }
        )

        self.action_log.append(
            f"Signos vitales actualizados para {patient.name} ({patient_id})."
        )
        return True, "Signos vitales registrados."

    def add_intervention(self, patient_id: str, procedure: str) -> tuple[bool, str]:
        if patient_id not in self.patients:
            return False, "Paciente no encontrado."
        if not procedure.strip():
            return False, "Escribe una intervención válida."

        self.histories[patient_id].append(procedure.strip())
        self.action_log.append(
            f"Intervención agregada a {patient_id}: {procedure.strip()}"
        )
        return True, "Intervención agregada al historial."

    def undo_last_action(self) -> tuple[bool, str]:
        if not self.undo_stack:
            return False, "No hay acciones para deshacer."

        action = self.undo_stack.pop()
        action_type = action["type"]
        patient = self.patients[action["patient_id"]]

        if action_type == "assign_bed":
            bed_index = action["bed_index"]
            self.beds[bed_index] = None
            patient.bed_index = action["previous_bed"]
            patient.status = action["previous_status"]
            patient.assigned_doctor = action["previous_doctor"]
            if action["removed_from_queue"]:
                self.waiting_queue.appendleft(patient.patient_id)
            self.action_log.append(
                f"Se deshizo la asignación de cama de {patient.name} ({patient.patient_id})."
            )
            return True, "Se deshizo la última asignación de cama."

        if action_type == "discharge":
            bed_index = action["bed_index"]
            if bed_index is not None:
                self.beds[bed_index] = patient.patient_id
            patient.bed_index = bed_index
            patient.status = action["old_status"]
            patient.assigned_doctor = action["old_doctor"]
            if action["was_in_queue"]:
                self.waiting_queue.appendleft(patient.patient_id)
            self.action_log.append(
                f"Se deshizo el alta médica de {patient.name} ({patient.patient_id})."
            )
            return True, "Se deshizo la última alta médica."

        if action_type == "vitals":
            patient.last_vitals = action["previous_vitals"]
            self.action_log.append(
                f"Se deshizo la actualización de signos vitales de {patient.name} ({patient.patient_id})."
            )
            return True, "Se deshizo el último cambio de signos vitales."

        return False, "No fue posible deshacer la acción."

    def available_beds(self) -> int:
        return sum(1 for bed in self.beds if bed is None)

    def active_patients(self) -> int:
        return sum(1 for patient in self.patients.values() if patient.status != "Alta médica")

    def get_waiting_patients(self) -> list[Patient]:
        return [self.patients[patient_id] for patient_id in self.waiting_queue]

    def get_patient_history(self, patient_id: str) -> list[str]:
        history = self.histories.get(patient_id)
        return history.to_list() if history else []

    def seed_demo_data(self) -> None:
        if self.patients:
            return

        self.add_doctor("Dra. Camila Rojas")
        self.add_doctor("Dr. Mateo Muñoz")
        self.add_doctor("Dra. Laura Gómez")

        p1 = self.register_patient("Ana López", 29, 4, "Dolor abdominal")
        p2 = self.register_patient("Luis Pérez", 52, 2, "Dolor torácico")
        p3 = self.register_patient("Sara Torres", 40, 5, "Control general")

        self.assign_bed(p2.patient_id, 0, "Dra. Camila Rojas")
        self.update_vitals(p2.patient_id, 37.4, 98, 95)
        self.add_intervention(p2.patient_id, "Electrocardiograma")
        self.add_intervention(p2.patient_id, "Monitoreo continuo")
        self.add_intervention(p1.patient_id, "Valoración inicial")
        self.action_log.append("Datos de demostración cargados.")
