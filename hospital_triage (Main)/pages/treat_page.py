import customtkinter as ctk
from tkinter import messagebox


# =========================================================
# TREAT PAGE
# =========================================================
def treat_page(frame, systems):

    # =====================================================
    # COLORS
    # =====================================================
    BG = "#0B1220"

    CARD = "#111827"
    BORDER = "#1F2937"

    TEXT = "#E5E7EB"
    MUTED = "#94A3B8"

    BLUE = "#3B82F6"

    RED = "#EF4444"
    YELLOW = "#FACC15"
    GREEN = "#22C55E"

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
    # HEADER
    # =====================================================
    ctk.CTkLabel(
        container,
        text="⚕️ Treat Patients",
        font=("Segoe UI", 30, "bold"),
        text_color="white"
    ).pack(anchor="w", pady=(10, 5))

    ctk.CTkLabel(
        container,
        text="Select a patient from the queue and treat them",
        font=("Segoe UI", 14),
        text_color=MUTED
    ).pack(anchor="w", pady=(0, 20))

    # =====================================================
    # QUEUE LIST CARD
    # =====================================================
    queue_card = ctk.CTkFrame(
        container,
        fg_color=CARD,
        corner_radius=20,
        border_width=1,
        border_color=BORDER
    )

    queue_card.pack(
        fill="both",
        expand=True,
        pady=(0, 20)
    )

    ctk.CTkLabel(
        queue_card,
        text="📋 Waiting Patients",
        font=("Segoe UI", 22, "bold"),
        text_color="white"
    ).pack(anchor="w", padx=20, pady=(20, 10))

    # =====================================================
    # SCROLLABLE LIST
    # =====================================================
    patient_list = ctk.CTkScrollableFrame(
        queue_card,
        fg_color="#0F172A",
        corner_radius=15
    )

    patient_list.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=(0, 20)
    )

    # =====================================================
    # REFRESH FUNCTION
    # =====================================================
    def refresh():

        # clear old widgets
        for widget in patient_list.winfo_children():
            widget.destroy()

        heap = getattr(systems, "heap", [])

        # =================================================
        # EMPTY QUEUE
        # =================================================
        if not heap:

            ctk.CTkLabel(
                patient_list,
                text="No patients waiting.",
                font=("Segoe UI", 16),
                text_color=MUTED
            ).pack(pady=30)

            return

        # =================================================
        # SHOW PATIENTS
        # =================================================
        sorted_patients = sorted(heap)

        for _, _, patient in sorted_patients:

            # =============================================
            # STATUS COLOR
            # =============================================
            if patient.priority <= 3:
                status = "CRITICAL 🔴"
                color = RED

            elif patient.priority <= 6:
                status = "URGENT 🟠"
                color = YELLOW

            else:
                status = "STABLE 🟢"
                color = GREEN

            # =============================================
            # PATIENT CARD
            # =============================================
            patient_card = ctk.CTkFrame(
                patient_list,
                fg_color="#111827",
                border_width=1,
                border_color=BORDER,
                corner_radius=15
            )

            patient_card.pack(
                fill="x",
                padx=10,
                pady=10
            )

            # =============================================
            # INFO
            # =============================================
            info = f"""
👤 Name: {patient.name}
🆔 ID: {patient.id}
⚠ Priority: {patient.priority}
📌 Status: {status}
🩺 Symptoms: {patient.symptoms}
            """

            ctk.CTkLabel(
                patient_card,
                text=info,
                justify="left",
                font=("Segoe UI", 14),
                text_color="white"
            ).pack(
                side="left",
                padx=20,
                pady=15
            )

            # =============================================
            # TREAT BUTTON
            # =============================================
            def treat_selected(p=patient):

                confirm = messagebox.askyesno(
                    "Confirm Treatment",
                    f"Treat patient {p.name}?"
                )

                if not confirm:
                    return

                try:

                    treated_patient = systems.treat()

                    if treated_patient:

                        messagebox.showinfo(
                            "Patient Treated",
                            f"""
Patient successfully treated.

👤 Name: {treated_patient.name}
🆔 ID: {treated_patient.id}

✅ Saved to history/database.
                            """
                        )

                        refresh()

                except Exception as e:

                    messagebox.showerror(
                        "System Error",
                        str(e)
                    )

            ctk.CTkButton(
                patient_card,
                text="💊 Treat",
                width=120,
                height=40,
                fg_color=color,
                hover_color="#2563EB",
                font=("Segoe UI", 14, "bold"),
                command=treat_selected
            ).pack(
                side="right",
                padx=20
            )

    # =====================================================
    # REFRESH BUTTON
    # =====================================================
    ctk.CTkButton(
        container,
        text="🔄 Refresh Queue",
        height=50,
        corner_radius=14,
        fg_color=BLUE,
        hover_color="#2563EB",
        font=("Segoe UI", 15, "bold"),
        command=refresh
    ).pack(fill="x")

    # =====================================================
    # INITIAL REFRESH
    # =====================================================
    refresh()