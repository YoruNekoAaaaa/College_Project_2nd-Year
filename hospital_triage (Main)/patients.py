import customtkinter as ctk
from tkinter import messagebox
import uuid
from datetime import datetime


# =========================================================
# APP THEME
# =========================================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# =========================================================
# COLORS
# =========================================================
BG = "#0B1220"

CARD = "#111827"
CARD2 = "#1E293B"

TEXT = "#E5E7EB"
MUTED = "#94A3B8"

BLUE = "#3B82F6"
GREEN = "#22C55E"
YELLOW = "#FACC15"
RED = "#EF4444"


# =========================================================
# PATIENT CLASS
# =========================================================
class Patient:

    def __init__(
        self,
        name,
        age,
        symptoms,
        pain_level,
        priority=9,
        pid=None
    ):

        self.id = pid if pid else str(uuid.uuid4())[:8]

        self.name = name
        self.age = int(age)

        self.symptoms = symptoms

        self.pain_level = int(pain_level)

        self.priority = priority

        self.created_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def __repr__(self):

        return (
            f"{self.id} | "
            f"{self.name} | "
            f"Age:{self.age} | "
            f"Pain:{self.pain_level} | "
            f"Priority:{self.priority}"
        )


# =========================================================
# TRIAGE PRIORITY SYSTEM
# =========================================================
def calculate_priority(patient):

    pain = patient.pain_level

    # lower number = more urgent
    if pain >= 9:
        return 1

    elif pain >= 7:
        return 3

    elif pain >= 5:
        return 5

    elif pain >= 3:
        return 7

    return 9


# =========================================================
# SYSTEM MANAGER
# =========================================================
class Systems:

    def __init__(self):

        self.patients = {}

    # =====================================================
    # ADD PATIENT
    # =====================================================
    def add_patient(self, patient, username):

        if username not in self.patients:

            self.patients[username] = []

        self.patients[username].append(patient)

    # =====================================================
    # LOAD USER PATIENTS
    # =====================================================
    def load_from_db(self, username):

        return self.patients.get(username, [])

    # =====================================================
    # TOTAL PATIENTS
    # =====================================================
    def total_patients(self, username):

        return len(
            self.patients.get(username, [])
        )


# =========================================================
# ADD PATIENT PAGE
# =========================================================
def add_patient_page(frame, systems, username):

    frame.configure(
        fg_color=BG
    )

    # =====================================================
    # HEADER
    # =====================================================
    header = ctk.CTkFrame(
        frame,
        fg_color="transparent"
    )

    header.pack(
        fill="x",
        padx=25,
        pady=(20, 10)
    )

    ctk.CTkLabel(
        header,
        text="➕ Add Patient",
        font=("Segoe UI", 30, "bold"),
        text_color="white"
    ).pack(anchor="w")

    ctk.CTkLabel(
        header,
        text="Register new patient into triage queue",
        font=("Segoe UI", 12),
        text_color=MUTED
    ).pack(anchor="w")

    # =====================================================
    # MAIN CARD
    # =====================================================
    card = ctk.CTkFrame(
        frame,
        fg_color=CARD,
        corner_radius=18,
        border_width=1,
        border_color=CARD2
    )

    card.pack(
        padx=25,
        pady=15,
        fill="both",
        expand=True
    )

    # =====================================================
    # STATUS LABEL
    # =====================================================
    status = ctk.CTkLabel(
        card,
        text="System Ready",
        text_color=MUTED,
        font=("Segoe UI", 12)
    )

    status.pack(pady=(20, 10))

    # =====================================================
    # HELPER FUNCTION
    # =====================================================
    def make_entry(label, placeholder=""):

        wrapper = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        wrapper.pack(
            fill="x",
            padx=25,
            pady=10
        )

        ctk.CTkLabel(
            wrapper,
            text=label,
            text_color=TEXT,
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", pady=(0, 5))

        entry = ctk.CTkEntry(
            wrapper,
            placeholder_text=placeholder,
            height=42,
            corner_radius=10,
            font=("Segoe UI", 12)
        )

        entry.pack(fill="x")

        return entry

    # =====================================================
    # INPUTS
    # =====================================================
    name_entry = make_entry(
        "Patient Name",
        "Enter full name"
    )

    age_entry = make_entry(
        "Age",
        "Enter age"
    )

    symptom_entry = make_entry(
        "Symptoms",
        "Describe symptoms"
    )

    pain_entry = make_entry(
        "Pain Level (0-10)",
        "Enter pain level"
    )

    # =====================================================
    # LIVE PATIENT COUNT
    # =====================================================
    count_var = ctk.StringVar(
        value=f"Patients Added: {systems.total_patients(username)}"
    )

    ctk.CTkLabel(
        card,
        textvariable=count_var,
        text_color=BLUE,
        font=("Segoe UI", 12, "bold")
    ).pack(pady=(10, 5))

    # =====================================================
    # SUBMIT FUNCTION
    # =====================================================
    def submit():

        try:

            name = name_entry.get().strip()

            age = age_entry.get().strip()

            symptoms = symptom_entry.get().strip()

            pain = pain_entry.get().strip()

            # =============================================
            # VALIDATION
            # =============================================
            if not all([name, age, symptoms, pain]):

                raise ValueError(
                    "All fields are required."
                )

            age_int = int(age)

            pain_int = int(pain)

            if age_int <= 0:

                raise ValueError(
                    "Age must be greater than 0."
                )

            if pain_int < 0 or pain_int > 10:

                raise ValueError(
                    "Pain level must be between 0 and 10."
                )

            # =============================================
            # CREATE PATIENT
            # =============================================
            patient = Patient(
                name,
                age_int,
                symptoms,
                pain_int
            )

            # =============================================
            # CALCULATE PRIORITY
            # =============================================
            patient.priority = calculate_priority(
                patient
            )

            # =============================================
            # SAVE PATIENT
            # =============================================
            systems.add_patient(
                patient,
                username
            )

            # =============================================
            # PRIORITY STATUS
            # =============================================
            if patient.priority <= 3:

                level = "CRITICAL 🔴"

            elif patient.priority <= 5:

                level = "MODERATE 🟠"

            else:

                level = "STABLE 🟢"

            # =============================================
            # UPDATE STATUS
            # =============================================
            status.configure(
                text=f"Patient Added Successfully • {level}",
                text_color=GREEN
            )

            # =============================================
            # UPDATE COUNT
            # =============================================
            count_var.set(
                f"Patients Added: {systems.total_patients(username)}"
            )

            # =============================================
            # SUCCESS MESSAGE
            # =============================================
            messagebox.showinfo(
                "Patient Added",
                f"""
Patient Registered Successfully

Patient ID: {patient.id}

Priority Level: {patient.priority}

Status: {level}
                """
            )

            # =============================================
            # CLEAR INPUTS
            # =============================================
            name_entry.delete(0, "end")

            age_entry.delete(0, "end")

            symptom_entry.delete(0, "end")

            pain_entry.delete(0, "end")

        # =================================================
        # VALIDATION ERROR
        # =================================================
        except ValueError as e:

            status.configure(
                text=str(e),
                text_color=RED
            )

            messagebox.showerror(
                "Validation Error",
                str(e)
            )

        # =================================================
        # UNKNOWN ERROR
        # =================================================
        except Exception as e:

            status.configure(
                text="Unexpected system error",
                text_color=RED
            )

            messagebox.showerror(
                "System Error",
                str(e)
            )

    # =====================================================
    # ADD BUTTON
    # =====================================================
    ctk.CTkButton(
        card,
        text="➕ Add Patient",
        command=submit,
        height=48,
        corner_radius=12,
        fg_color=BLUE,
        hover_color="#2563EB",
        font=("Segoe UI", 14, "bold")
    ).pack(
        padx=25,
        pady=25,
        fill="x"
    )


# =========================================================
# MAIN APP
# =========================================================
if __name__ == "__main__":

    root = ctk.CTk()

    root.title(
        "Hospital Triage System"
    )

    root.geometry(
        "700x750"
    )

    root.configure(
        fg_color=BG
    )

    systems = Systems()

    username = "admin"

    add_patient_page(
        root,
        systems,
        username
    )

    root.mainloop()