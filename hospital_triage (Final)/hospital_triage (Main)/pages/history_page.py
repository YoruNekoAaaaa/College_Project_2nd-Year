import customtkinter as ctk
from tkinter import ttk


# =========================================================
# HISTORY PAGE
# =========================================================
def history_page(frame, systems):

    # =====================================================
    # COLORS
    # =====================================================
    BG = "#0B1220"
    CARD = "#111827"

    TEXT = "#E5E7EB"
    MUTED = "#94A3B8"

    BLUE = "#3B82F6"

    CRITICAL = "#EF4444"
    URGENT = "#F59E0B"
    STABLE = "#22C55E"

    BORDER = "#1F2937"

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
        text="📜 Patient Treatment History",
        font=("Segoe UI", 30, "bold"),
        text_color="white"
    ).pack(anchor="w", pady=(10, 5))

    ctk.CTkLabel(
        container,
        text="Complete history of treated emergency patients",
        font=("Segoe UI", 14),
        text_color=MUTED
    ).pack(anchor="w", pady=(0, 20))

    # =====================================================
    # STATS SECTION
    # =====================================================
    stats_frame = ctk.CTkFrame(
        container,
        fg_color=CARD,
        corner_radius=16,
        border_width=1,
        border_color=BORDER
    )

    stats_frame.pack(fill="x", pady=(0, 20))

    count_var = ctk.StringVar(value="0")

    ctk.CTkLabel(
        stats_frame,
        text="Total Treated Patients",
        font=("Segoe UI", 13),
        text_color=MUTED
    ).pack(pady=(15, 5))

    ctk.CTkLabel(
        stats_frame,
        textvariable=count_var,
        font=("Segoe UI", 34, "bold"),
        text_color=BLUE
    ).pack(pady=(0, 15))

    # =====================================================
    # TABLE CARD
    # =====================================================
    table_card = ctk.CTkFrame(
        container,
        fg_color=CARD,
        corner_radius=18,
        border_width=1,
        border_color=BORDER
    )

    table_card.pack(
        expand=True,
        fill="both"
    )

    # =====================================================
    # TABLE TITLE
    # =====================================================
    top_bar = ctk.CTkFrame(
        table_card,
        fg_color="transparent"
    )

    top_bar.pack(fill="x", padx=20, pady=(15, 5))

    ctk.CTkLabel(
        top_bar,
        text="Treatment Records",
        font=("Segoe UI", 18, "bold"),
        text_color="white"
    ).pack(side="left")

    # =====================================================
    # TABLE FRAME
    # =====================================================
    table_frame = ctk.CTkFrame(
        table_card,
        fg_color="transparent"
    )

    table_frame.pack(
        expand=True,
        fill="both",
        padx=15,
        pady=(0, 15)
    )

    # =====================================================
    # SCROLLBAR
    # =====================================================
    scrollbar = ttk.Scrollbar(table_frame)

    scrollbar.pack(
        side="right",
        fill="y"
    )

    # =====================================================
    # TABLE COLUMNS
    # =====================================================
    columns = (
        "Patient Name",
        "Priority",
        "Patient ID",
        "Symptoms"
    )

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        yscrollcommand=scrollbar.set
    )

    scrollbar.configure(command=tree.yview)

    # =====================================================
    # HEADINGS
    # =====================================================
    for col in columns:

        tree.heading(col, text=col)

        tree.column(
            col,
            anchor="center"
        )

    tree.column("Patient Name", width=220)
    tree.column("Priority", width=120)
    tree.column("Patient ID", width=140)
    tree.column("Symptoms", width=450)

    # =====================================================
    # TAG COLORS
    # =====================================================
    tree.tag_configure(
        "critical",
        background="#3A1F1F",
        foreground="white"
    )

    tree.tag_configure(
        "urgent",
        background="#3A2A1F",
        foreground="white"
    )

    tree.tag_configure(
        "stable",
        background="#1F3A2A",
        foreground="white"
    )

    # =====================================================
    # TABLE STYLE
    # =====================================================
    style = ttk.Style()

    style.theme_use("default")

    style.configure(
        "Treeview",
        rowheight=34,
        font=("Segoe UI", 10),
        background=CARD,
        fieldbackground=CARD,
        foreground=TEXT,
        borderwidth=0
    )

    style.configure(
        "Treeview.Heading",
        font=("Segoe UI", 11, "bold"),
        background="#0F172A",
        foreground="white",
        relief="flat"
    )

    style.map(
        "Treeview",
        background=[("selected", BLUE)],
        foreground=[("selected", "white")]
    )

    tree.pack(
        expand=True,
        fill="both"
    )

    # =====================================================
    # PERFORMANCE CACHE
    # =====================================================
    last_count = {"value": -1}

    # =====================================================
    # LOAD HISTORY
    # =====================================================
    def load_history():

        treated = getattr(
            systems,
            "treated_log",
            []
        )

        # =================================================
        # ONLY REFRESH IF DATA CHANGED
        # =================================================
        if len(treated) != last_count["value"]:

            last_count["value"] = len(treated)

            # =============================================
            # CLEAR TABLE
            # =============================================
            for item in tree.get_children():
                tree.delete(item)

            count_var.set(str(len(treated)))

            # =============================================
            # EMPTY STATE
            # =============================================
            if not treated:

                tree.insert(
                    "",
                    "end",
                    values=(
                        "No treated patients found",
                        "-",
                        "-",
                        "-"
                    )
                )

            # =============================================
            # LOAD DATA
            # =============================================
            else:

                for patient in treated:

                    # =====================================
                    # DETECT PRIORITY TYPE
                    # =====================================
                    priority = str(patient.priority)

                    if priority.lower() == "critical":
                        tag = "critical"

                    elif priority.lower() == "urgent":
                        tag = "urgent"

                    else:
                        tag = "stable"

                    # =====================================
                    # INSERT ROW
                    # =====================================
                    tree.insert(
                        "",
                        "end",
                        values=(
                            patient.name,
                            patient.priority,
                            patient.id,
                            patient.symptoms
                        ),
                        tags=(tag,)
                    )

        # =================================================
        # AUTO REFRESH
        # =================================================
        frame.after(1000, load_history)

    # =====================================================
    # INITIAL LOAD
    # =====================================================
    load_history()