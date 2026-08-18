import customtkinter as ctk
from tkinter import ttk, messagebox


# =========================================================
# VIEW QUEUE PAGE
# =========================================================
def view_queue_page(frame, systems):

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

    header.pack(fill="x", pady=(10, 15))

    ctk.CTkLabel(
        header,
        text="📋 Patient Queue",
        font=("Segoe UI", 30, "bold"),
        text_color="white"
    ).pack(side="left")

    queue_var = ctk.StringVar(
        value="Patients Waiting: 0"
    )

    ctk.CTkLabel(
        header,
        textvariable=queue_var,
        font=("Segoe UI", 14, "bold"),
        text_color=BLUE
    ).pack(side="right")

    # =====================================================
    # SEARCH + BUTTON BAR
    # =====================================================
    top_bar = ctk.CTkFrame(
        container,
        fg_color="transparent"
    )

    top_bar.pack(fill="x", pady=(0, 15))

    # =====================================================
    # SEARCH ENTRY
    # =====================================================
    search_var = ctk.StringVar()

    search_entry = ctk.CTkEntry(
        top_bar,
        textvariable=search_var,
        placeholder_text="Search patient by name, ID, or symptoms...",
        height=42,
        width=350,
        corner_radius=12,
        font=("Segoe UI", 12)
    )

    search_entry.pack(side="left")

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
        pady=15
    )

    # =====================================================
    # SCROLLBAR
    # =====================================================
    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical"
    )

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
        "Symptoms",
        "Status"
    )

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        yscrollcommand=scrollbar.set
    )

    scrollbar.configure(
        command=tree.yview
    )

    # =====================================================
    # HEADERS
    # =====================================================
    for col in columns:

        tree.heading(
            col,
            text=col
        )

        tree.column(
            col,
            anchor="center"
        )

    tree.column("Patient Name", width=220)
    tree.column("Priority", width=120)
    tree.column("Patient ID", width=150)
    tree.column("Symptoms", width=350)
    tree.column("Status", width=150)

    # =====================================================
    # TABLE STYLE
    # =====================================================
    style = ttk.Style()

    style.theme_use("default")

    style.configure(
        "Treeview",
        rowheight=36,
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

    tree.pack(
        expand=True,
        fill="both"
    )

    # =====================================================
    # BUTTON BAR
    # =====================================================
    button_bar = ctk.CTkFrame(
        container,
        fg_color="transparent"
    )

    button_bar.pack(fill="x", pady=(15, 0))

    # =====================================================
    # REFRESH FUNCTION
    # =====================================================
    def refresh_queue():

        # =============================================
        # CLEAR TABLE
        # =============================================
        for item in tree.get_children():
            tree.delete(item)

        heap = getattr(
            systems,
            "heap",
            []
        )

        keyword = search_var.get().lower()

        filtered = []

        # =============================================
        # SORT QUEUE
        # =============================================
        try:

            sorted_heap = sorted(heap)

        except:
            sorted_heap = heap

        # =============================================
        # FILTER RESULTS
        # =============================================
        for item in sorted_heap:

            patient = item[-1] if isinstance(item, tuple) else item

            if (
                keyword in patient.name.lower()
                or keyword in patient.id.lower()
                or keyword in patient.symptoms.lower()
            ):
                filtered.append(patient)

        # =============================================
        # UPDATE COUNT
        # =============================================
        queue_var.set(
            f"Patients Waiting: {len(filtered)}"
        )

        # =============================================
        # EMPTY STATE
        # =============================================
        if not filtered:

            tree.insert(
                "",
                "end",
                values=(
                    "No Patients Found",
                    "-",
                    "-",
                    "-",
                    "-"
                )
            )

        # =============================================
        # INSERT DATA
        # =============================================
        else:

            for patient in filtered:

                priority = str(patient.priority)

                if priority.lower() == "critical":

                    tag = "critical"
                    status = "CRITICAL 🔴"

                elif priority.lower() == "urgent":

                    tag = "urgent"
                    status = "URGENT 🟠"

                else:

                    tag = "stable"
                    status = "STABLE 🟢"

                tree.insert(
                    "",
                    "end",
                    values=(
                        patient.name,
                        patient.priority,
                        patient.id,
                        patient.symptoms,
                        status
                    ),
                    tags=(tag,)
                )

        # =============================================
        # AUTO REFRESH
        # =============================================
        frame.after(
            1000,
            refresh_queue
        )

    # =====================================================
    # REFRESH BUTTON
    # =====================================================
    ctk.CTkButton(
        button_bar,
        text="🔄 Refresh",
        height=45,
        corner_radius=12,
        fg_color=BLUE,
        hover_color="#2563EB",
        font=("Segoe UI", 13, "bold"),
        command=refresh_queue
    ).pack(side="left")

    # =====================================================
    # CLEAR BUTTON
    # =====================================================
    # =======================
    # LIVE SEARCH
    # =====================================================
    search_var.trace_add(
        "write",
        lambda *args: refresh_queue()
    )

    # =====================================================
    # INITIAL LOAD
    # =====================================================
    refresh_queue()