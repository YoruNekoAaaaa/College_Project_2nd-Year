import customtkinter as ctk


# =========================================================
# HOME PAGE
# =========================================================
def home_page(frame, systems):

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
    header = ctk.CTkFrame(
        container,
        fg_color="transparent"
    )

    header.pack(fill="x", pady=(10, 20))

    # =====================================================
    # TITLE
    # =====================================================
    left = ctk.CTkFrame(
        header,
        fg_color="transparent"
    )

    left.pack(side="left")

    ctk.CTkLabel(
        left,
        text="🏥 Hospital Triage Dashboard",
        font=("Segoe UI", 30, "bold"),
        text_color="white"
    ).pack(anchor="w")

    ctk.CTkLabel(
        left,
        text="Manage emergency patients efficiently in real time",
        font=("Segoe UI", 14),
        text_color=MUTED
    ).pack(anchor="w", pady=(5, 0))

    # =====================================================
    # PROFILE BUTTON
    # =====================================================
    def open_profile():

        from pages.profile_page import profile_page

        for widget in frame.winfo_children():
            widget.destroy()

        profile_page(
            frame,
            systems,
            getattr(
                systems,
                "current_user",
                "Doctor"
            )
        )

    ctk.CTkButton(
        header,
        text="👤 Profile",
        width=130,
        height=42,
        corner_radius=12,
        fg_color=CARD,
        hover_color="#1E293B",
        text_color=TEXT,
        command=open_profile
    ).pack(side="right")

    # =====================================================
    # STATS SECTION
    # =====================================================
    stats_frame = ctk.CTkFrame(
        container,
        fg_color="transparent"
    )

    stats_frame.pack(fill="x", pady=10)

    # =====================================================
    # VARIABLES
    # =====================================================
    treating_var = ctk.StringVar(value="None")
    waiting_var = ctk.StringVar(value="0")
    today_var = ctk.StringVar(value="0")
    treated_var = ctk.StringVar(value="0")

    # =====================================================
    # CARD CREATOR
    # =====================================================
    def create_card(title, variable, color):

        card = ctk.CTkFrame(
            stats_frame,
            fg_color=CARD,
            corner_radius=18,
            border_width=1,
            border_color=BORDER,
            width=250,
            height=140
        )

        card.pack(
            side="left",
            padx=10,
            expand=True,
            fill="both"
        )

        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 13),
            text_color=MUTED
        ).pack(pady=(25, 5))

        ctk.CTkLabel(
            card,
            textvariable=variable,
            font=("Segoe UI", 30, "bold"),
            text_color=color
        ).pack()

        return card

    # =====================================================
    # DASHBOARD CARDS
    # =====================================================
    create_card(
        "Treating Next",
        treating_var,
        BLUE
    )

    create_card(
        "Waiting Patients",
        waiting_var,
        YELLOW
    )

    create_card(
        "Patients Today",
        today_var,
        GREEN
    )

    create_card(
        "Total Treated",
        treated_var,
        RED
    )

    # =====================================================
    # LIVE ACTIVITY SECTION
    # =====================================================
    activity_card = ctk.CTkFrame(
        container,
        fg_color=CARD,
        corner_radius=18,
        border_width=1,
        border_color=BORDER
    )

    activity_card.pack(
        fill="both",
        expand=True,
        pady=25
    )

    ctk.CTkLabel(
        activity_card,
        text="📡 Live System Activity",
        font=("Segoe UI", 20, "bold"),
        text_color="white"
    ).pack(anchor="w", padx=20, pady=(20, 10))

    activity_box = ctk.CTkTextbox(
        activity_card,
        height=250,
        corner_radius=12,
        fg_color="#0F172A",
        border_width=0,
        font=("Consolas", 13)
    )

    activity_box.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=(0, 20)
    )

    activity_box.insert(
        "end",
        "System Started Successfully...\n"
    )

    activity_box.configure(state="disabled")

    # =====================================================
    # UPDATE FUNCTION
    # =====================================================
    def update_dashboard():

        try:

            heap = getattr(
                systems,
                "heap",
                []
            )

            treated = getattr(
                systems,
                "treated_log",
                []
            )

            # =============================================
            # CURRENT PATIENT
            # =============================================
            if heap:

                patient = heap[0]

                if isinstance(patient, tuple):
                    patient = patient[-1]

                treating_var.set(
                    getattr(patient, "name", "Unknown")
                )

            else:
                treating_var.set("None")

            # =============================================
            # STATS
            # =============================================
            waiting_var.set(str(len(heap)))
            today_var.set(str(len(treated)))
            treated_var.set(str(len(treated)))

            # =============================================
            # UPDATE ACTIVITY LOG
            # =============================================
            activity_box.configure(state="normal")

            activity_box.delete("1.0", "end")

            activity_box.insert(
                "end",
                f"🟢 System Status: ACTIVE\n\n"
            )

            activity_box.insert(
                "end",
                f"👨‍⚕ Waiting Patients: {len(heap)}\n"
            )

            activity_box.insert(
                "end",
                f"✅ Treated Patients: {len(treated)}\n"
            )

            if heap:

                next_patient = heap[0]

                if isinstance(next_patient, tuple):
                    next_patient = next_patient[-1]

                activity_box.insert(
                    "end",
                    f"\n🚑 Next Patient: {next_patient.name}"
                )

            activity_box.configure(state="disabled")

        except Exception as e:

            activity_box.configure(state="normal")

            activity_box.delete("1.0", "end")

            activity_box.insert(
                "end",
                f"System Error:\n{str(e)}"
            )

            activity_box.configure(state="disabled")

        # =================================================
        # AUTO REFRESH
        # =================================================
        frame.after(1000, update_dashboard)

    # =====================================================
    # INITIAL LOAD
    # =====================================================
    update_dashboard()

    # =====================================================
    # FOOTER
    # =====================================================
    footer = ctk.CTkFrame(
        container,
        fg_color=CARD,
        corner_radius=14,
        border_width=1,
        border_color=BORDER
    )

    footer.pack(fill="x")

    ctk.CTkLabel(
        footer,
        text="🟢 System Status: ACTIVE • All hospital services operational",
        font=("Segoe UI", 12),
        text_color=MUTED
    ).pack(pady=18)