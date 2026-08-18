import customtkinter as ctk
from tkinter import messagebox

from patients import Patient
from triage import calculate_priority


# =========================================================
# ADD PATIENT PAGE
# =========================================================
def add_patient_page(frame, systems, username):

    # =====================================================
    # COLORS
    # =====================================================
    BG = "#0B1220"
    CARD = "#111827"
    MUTED = "#94A3B8"
    BORDER = "#1F2937"
    SUCCESS = "#22C55E"
    ERROR = "#EF4444"

    # =====================================================
    # VALIDATION
    # =====================================================
    if not systems:
        raise ValueError("System is not initialized")

    if not username:
        raise ValueError("Username is missing")

    # =====================================================
    # PAGE CONFIG
    # =====================================================
    frame.configure(fg_color=BG)

    # =====================================================
    # MAIN CONTAINER
    # =====================================================
    container = ctk.CTkScrollableFrame(
        frame,
        fg_color=BG,
        scrollbar_button_color=BORDER,
        scrollbar_button_hover_color=MUTED
    )

    container.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )
    # =====================================================
    # TITLE
    # =====================================================
    ctk.CTkLabel(
        container,
        text="➕ Add New Patient",
        font=("Segoe UI", 30, "bold"),
        text_color="white"
    ).pack(anchor="w", pady=(10, 5))

    ctk.CTkLabel(
        container,
        text="Register and prioritize incoming emergency patients",
        font=("Segoe UI", 14),
        text_color=MUTED
    ).pack(anchor="w", pady=(0, 20))

    # =====================================================
    # CARD
    # =====================================================
    card = ctk.CTkFrame(
        container,
        fg_color=CARD,
        corner_radius=18
    )

    card.pack(fill="x", padx=10, pady=10)

    # =====================================================
    # STATUS LABEL
    # =====================================================
    status = ctk.CTkLabel(
        card,
        text="Ready",
        text_color=MUTED,
        font=("Segoe UI", 13)
    )

    status.pack(pady=(15, 10))

    # =====================================================
    # STATUS FUNCTION
    # =====================================================
    def set_status(message, color=MUTED):

        status.configure(
            text=message,
            text_color=color
        )

    # =====================================================
    # INPUT CREATOR
    # =====================================================
    def create_input(label_text, placeholder):

        wrapper = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        wrapper.pack(
            fill="x",
            padx=20,
            pady=8
        )

        ctk.CTkLabel(
            wrapper,
            text=label_text,
            font=("Segoe UI", 13, "bold"),
            text_color="white"
        ).pack(anchor="w", pady=(0, 5))

        entry = ctk.CTkEntry(
            wrapper,
            placeholder_text=placeholder,
            height=42,
            corner_radius=10
        )

        entry.pack(fill="x")

        return entry

    # =====================================================
    # INPUT FIELDS
    # =====================================================
    name = create_input(
        "Patient Name",
        "Enter patient name"
    )

    age = create_input(
        "Age",
        "Enter patient age"
    )

    symptom = create_input(
        "Symptoms",
        "Enter symptoms"
    )

    pain = create_input(
        "Pain Level (0-10)",
        "Enter pain level"
    )

    # =====================================================
    # PRIORITY DISPLAY
    # =====================================================
    priority_label = ctk.CTkLabel(
        card,
        text="Priority: Not Calculated",
        font=("Segoe UI", 15, "bold"),
        text_color="#FBBF24"
    )

    priority_label.pack(pady=15)

    # =====================================================
    # SUBMIT FUNCTION
    # =====================================================
    def submit():

        try:

            # =============================================
            # GET VALUES
            # =============================================
            name_val = name.get().strip()
            age_val = age.get().strip()
            symptom_val = symptom.get().strip()
            pain_val = pain.get().strip()

            # =============================================
            # VALIDATION
            # =============================================
            if not all([
                name_val,
                age_val,
                symptom_val,
                pain_val
            ]):
                raise ValueError(
                    "All fields are required."
                )

            age_int = int(age_val)
            pain_int = int(pain_val)

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
                name_val,
                age_int,
                symptom_val,
                pain_int
            )

            # =============================================
            # CALCULATE PRIORITY
            # =============================================
            patient.priority = calculate_priority(patient)

            # =============================================
            # PRIORITY COLOR
            # =============================================
            if patient.priority == "Critical":
                priority_color = "#EF4444"

            elif patient.priority == "Urgent":
                priority_color = "#F59E0B"

            else:
                priority_color = "#22C55E"

            priority_label.configure(
                text=f"Priority: {patient.priority}",
                text_color=priority_color
            )

            # =============================================
            # SAVE PATIENT
            # =============================================
            systems.add_patient(
                patient,
                username
            )

            # =============================================
            # SUCCESS
            # =============================================
            set_status(
                "Patient added successfully!",
                SUCCESS
            )

            messagebox.showinfo(
                "Success",
                f"""
Patient Registered Successfully

Patient ID: {patient.id}
Priority: {patient.priority}
                """
            )

            # =============================================
            # CLEAR FIELDS
            # =============================================
            name.delete(0, "end")
            age.delete(0, "end")
            symptom.delete(0, "end")
            pain.delete(0, "end")

        # =================================================
        # VALIDATION ERROR
        # =================================================
        except ValueError as ve:

            set_status(
                str(ve),
                ERROR
            )

            messagebox.showerror(
                "Validation Error",
                str(ve)
            )

        # =================================================
        # GENERAL ERROR
        # =================================================
        except Exception as e:

            set_status(
                "Unexpected system error occurred",
                ERROR
            )

            messagebox.showerror(
                "System Error",
                str(e)
            )

    # =====================================================
    # BUTTON FRAME
    # =====================================================
    button_frame = ctk.CTkFrame(
        card,
        fg_color="transparent"
    )

    button_frame.pack(
        fill="x",
        padx=20,
        pady=20
    )

    # =====================================================
    # ADD BUTTON
    # =====================================================
    ctk.CTkButton(
        button_frame,
        text="➕ Add Patient",
        height=40,
        corner_radius=12,
        fg_color="#2563EB",
        hover_color="#1D4ED8",
        font=("Segoe UI", 14, "bold"),
        command=submit
    ).pack(side="left", padx=(0, 10))

    # =====================================================
    # CLEAR BUTTON
    # =====================================================
    def clear_fields():

        name.delete(0, "end")
        age.delete(0, "end")
        symptom.delete(0, "end")
        pain.delete(0, "end")

        priority_label.configure(
            text="Priority: Not Calculated",
            text_color="#FBBF24"
        )

        set_status("Cleared")

    ctk.CTkButton(
        button_frame,
        text="🗑 Clear",
        height=40,
        corner_radius=12,
        fg_color="#374151",
        hover_color="#4B5563",
        font=("Segoe UI", 14, "bold"),
        command=clear_fields
    ).pack(side="left")