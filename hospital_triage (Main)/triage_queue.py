import heapq
from datetime import datetime

from database import (
    get_patients,
    save_patient,
    mark_patient_treated,
    clear_waiting_patients
)

from patients import Patient


# =========================================================
# TRIAGE SYSTEM
# =========================================================
class TriageSystem:

    # =====================================================
    # INIT
    # =====================================================
    def __init__(self):
        self.heap = []  # waiting queue
        self.treated_log = []  # treated patients
        self.current_user = None
        self._counter = 0
    # =====================================================
    # ADD PATIENT
    # =====================================================
    def add_patient(self, patient, username=None):
        try:
            if username:
                save_patient(username, patient)

            self._counter += 1
            heapq.heappush(self.heap, (patient.priority, self._counter, patient))

            print(f"[ADDED] {patient.name} (Priority {patient.priority})")
            return True

        except Exception as e:
            print("Add Patient Error:", e)
            return False

    # =====================================================
    # TREAT NEXT PATIENT
    # =====================================================
    def treat(self):
        if not self.heap:
            print("Queue empty")
            return None

        try:
            _, _, patient = heapq.heappop(self.heap)
            self.treated_log.append(patient)
            mark_patient_treated(patient.id)

            print(f"[TREATED] {patient.name}")
            return patient

        except Exception as e:
            print("Treat Error:", e)
            return None

    # =====================================================
    # SEARCH BY ID
    # =====================================================
    def search_id(self, uid):
        uid = uid.strip()

        for _, _, patient in self.heap:
            if patient.id == uid:
                return patient

        for patient in self.treated_log:
            if patient.id == uid:
                return patient

        return None

    # =====================================================
    # SEARCH BY NAME
    # =====================================================
    def search_name(self, keyword):
        keyword = keyword.lower()
        results = []

        for _, _, patient in self.heap:
            if keyword in patient.name.lower():
                results.append(patient)

        for patient in self.treated_log:
            if keyword in patient.name.lower():
                results.append(patient)

        return results

    # =====================================================
    # LOAD FROM DATABASE
    # =====================================================
    def load_from_db(self, username=None):
        try:
            self.heap.clear()
            self.treated_log.clear()
            self.current_user = username

            rows = get_patients(username)

            if not rows:
                print("No patients found")
                return

            for row in rows:
                try:
                    patient = Patient(
                        name=row[2],
                        age=row[3],
                        symptoms=row[4],
                        pain_level=row[5],
                        priority=row[6],
                        pid=row[0]
                    )

                    status = row[7]

                    if status == "waiting":
                        heapq.heappush(self.heap, (patient.priority, patient.id, patient))
                    else:
                        self.treated_log.append(patient)

                except Exception as e:
                    print("Skipping bad row:", row, e)

            print(f"[LOADED] {len(self.heap)} waiting | {len(self.treated_log)} treated")

        except Exception as e:
            print("Database Load Error:", e)

    # =====================================================
    # CLEAR WAITING QUEUE
    # =====================================================
    def clear_queue(self):
        try:
            self.heap.clear()

            if self.current_user:
                clear_waiting_patients(self.current_user)

            print("Queue cleared")

        except Exception as e:
            print("Clear Queue Error:", e)

    # =====================================================
    # TOTAL WAITING / TREATED
    # =====================================================
    def total_waiting(self):
        return len(self.heap)

    def total_treated(self):
        return len(self.treated_log)

    # =====================================================
    # NEXT PATIENT
    # =====================================================
    def next_patient(self):
        if not self.heap:
            return None
        try:
            return self.heap[0][2]
        except:
            return None

    # =====================================================
    # COUNTS
    # =====================================================
    def critical_count(self):
        return sum(1 for _, _, p in self.heap if p.priority <= 3)

    def moderate_count(self):
        return sum(1 for _, _, p in self.heap if 4 <= p.priority <= 6)

    def stable_count(self):
        return sum(1 for _, _, p in self.heap if p.priority >= 7)

    # =====================================================
    # DASHBOARD
    # =====================================================
    def get_dashboard_data(self):
        next_patient = self.next_patient()

        return {
            "waiting": self.total_waiting(),
            "treated": self.total_treated(),
            "critical": self.critical_count(),
            "moderate": self.moderate_count(),
            "stable": self.stable_count(),
            "next_patient": next_patient.name if next_patient else "None"
        }

    # =====================================================
    # DEBUG VIEW
    # =====================================================
    def debug_print(self):
        print("\n==============================")
        print("WAITING PATIENTS")
        print("==============================")

        if not self.heap:
            print("No waiting patients")
        else:
            for _, _, patient in self.heap:
                print(patient)

        print("\n==============================")
        print("TREATED PATIENTS")
        print("==============================")

        if not self.treated_log:
            print("No treated patients")
        else:
            for patient in self.treated_log:
                print(patient)

        print("\n==============================")
        print(f"Waiting : {self.total_waiting()}")
        print(f"Treated : {self.total_treated()}")
        print("==============================")