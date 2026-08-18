import customtkinter as ctk
from tkinter import messagebox


# =========================================================
# SEARCH PAGE
# =========================================================
def search_page(frame, systems):

    # =====================================================
    # COLORS
    # =====================================================
    BG = "#0B1220"

    CARD = "#111827"
    BORDER = "#1F2937"

    TEXT = "#E5E7EB"
    MUTED = "#94A3B8"

    BLUE = "#3B82F6"

    GREEN = "#22C55E"
    YELLOW = "#FACC15"
    RED = "#EF4444"

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
        text="🔎 Patient Search System",
        font=("Segoe UI", 30, "bold"),
        text_color="white"
    ).pack(anchor="w", pady=(10, 5))

    ctk.CTkLabel(
        container,
        text="Search patient records instantly using Patient ID",
        font=("Segoe UI", 14),
        text_color=MUTED
    ).pack(anchor="w", pady=(0, 20))

    # =====================================================
    # SEARCH CARD
    # =====================================================
    search_card = ctk.CTkFrame(
        container,
        fg_color=CARD,
        corner_radius=18,
        border_width=1,
        border_color=BORDER
    )

    search_card.pack(
        fill="x",
        pady=(0, 20)
    )

    ctk.CTkLabel(
        search_card,
        text="Enter Patient ID",
        font=("Segoe UI", 14, "bold"),
        text_color="white"
    ).pack(anchor="w", padx=20, pady=(20, 8))

    # =====================================================
    # SEARCH INPUT
    # =====================================================
    entry = ctk.CTkEntry(
        search_card,
        placeholder_text="Example: a1b2c3",
        height=45,
        corner_radius=12,
        font=("Segoe UI", 13)
    )

    entry.pack(
        fill="x",
        padx=20,
        pady=(0, 20)
    )

    entry.focus()

    # =====================================================
    # RESULT CARD
    # =====================================================
    result_card = ctk.CTkFrame(
        container,
        fg_color=CARD,
        corner_radius=18,
        border_width=1,
        border_color=BORDER
    )

    result_card.pack(
        expand=True,
        fill="both"
    )

    # =====================================================
    # RESULT TITLE
    # =====================================================
    ctk.CTkLabel(
        result_card,
        text="📄 Search Result",
        font=("Segoe UI", 20, "bold"),
        text_color="white"
    ).pack(anchor="w", padx=20, pady=(20, 10))

    # =====================================================
    # RESULT BOX
    # =====================================================
    result_box = ctk.CTkTextbox(
        result_card,
        corner_radius=12,
        fg_color="#0F172A",
        border_width=0,
        font=("Consolas", 13)
    )

    result_box.pack(
        expand=True,
        fill="both",
        padx=20,
        pady=(0, 20)
    )

    result_box.insert(
        "end",
        "Search for a patient to display information..."
    )

    result_box.configure(state="disabled")

    # =====================================================
    # SEARCH FUNCTION
    # =====================================================
    def search():

        patient_id = entry.get().strip()

        # =================================================
        # VALIDATION
        # =================================================
        if not patient_id:

            messagebox.showwarning(
                "Missing Patient ID",
                "Please enter a Patient ID"
            )

            return

        # =================================================
        # SEARCH DATABASE
        # =================================================
        try:

            patient = systems.search_id(patient_id)

        except Exception as e:

            result_box.configure(state="normal")

            result_box.delete("1.0", "end")

            result_box.insert(
                "end",
                f"❌ System Error\n\n{str(e)}"
            )

            result_box.configure(state="disabled")

            return

        # =================================================
        # NOT FOUND
        # =================================================
        if not patient:

            result_box.configure(state="normal")

            result_box.delete("1.0", "end")

            result_box.insert(
                "end",
                "❌ No patient found with this Patient ID."
            )

            result_box.configure(state="disabled")

            return

        # =================================================
        # PRIORITY STATUS
        # =================================================
        priority = int(patient.priority)

        if priority <= 3:

            status = "CRITICAL 🔴"
            status_color = RED

        elif priority <= 6:

            status = "URGENT 🟠"
            status_color = YELLOW

        else:

            status = "STABLE 🟢"
            status_color = GREEN

        # =================================================
        # CHECK IF TREATED
        # =================================================
        treated = any(
            p.id == patient.id
            for p in systems.treated_log
        )

        treatment_status = (
            "TREATED ✅"
            if treated
            else "WAITING ⏳"
        )

        # =================================================
        # DISPLAY RESULT
        # =================================================
        result_box.configure(state="normal")

        result_box.delete("1.0", "end")

        result_box.insert(
            "end",
            f"""
✅ Patient Found

━━━━━━━━━━━━━━━━━━━━━━

👤 Name:
{patient.name}

🆔 Patient ID:
{patient.id}

🎂 Age:
{patient.age}

⚠ Priority:
{patient.priority}

📌 Condition:
{status}

🏥 Queue Status:
{treatment_status}

🩺 Symptoms:
{patient.symptoms}

💢 Pain Level:
{patient.pain_level}

━━━━━━━━━━━━━━━━━━━━━━
            """
        )

        result_box.configure(
            text_color=status_color
        )

        result_box.configure(state="disabled")

    # =====================================================
    # BUTTON FRAME
    # =====================================================
    button_frame = ctk.CTkFrame(
        container,
        fg_color="transparent"
    )

    button_frame.pack(
        fill="x",
        pady=(15, 0)
    )

    # =====================================================
    # SEARCH BUTTON
    # =====================================================
    ctk.CTkButton(
        button_frame,
        text="🔎 Search Patient",
        height=45,
        corner_radius=12,
        fg_color=BLUE,
        hover_color="#2563EB",
        font=("Segoe UI", 14, "bold"),
        command=search
    ).pack(side="left")

    # =====================================================
    # CLEAR FUNCTION
    # =====================================================
    def clear():

        entry.delete(0, "end")

        result_box.configure(state="normal")

        result_box.delete("1.0", "end")

        result_box.insert(
            "end",
            "Search for a patient to display information..."
        )

        result_box.configure(
            text_color=TEXT
        )

        result_box.configure(state="disabled")

    # =====================================================
    # CLEAR BUTTON
    # =====================================================
    ctk.CTkButton(
        button_frame,
        text="🗑 Clear",
        height=45,
        corner_radius=12,
        fg_color="#374151",
        hover_color="#4B5563",
        font=("Segoe UI", 14, "bold"),
        command=clear
    ).pack(side="left", padx=10)

    # =====================================================
    # ENTER KEY SUPPORT
    # =====================================================
    entry.bind(
        "<Return>",
        lambda e: search()
    )