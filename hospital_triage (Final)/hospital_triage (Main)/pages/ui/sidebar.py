import customtkinter as ctk

# =========================================================
# COLORS
# =========================================================
BG = "#0B1220"
CARD = "#111827"
TEXT = "#E5E7EB"
HOVER = "#2563EB"
DANGER = "#DC2626"


# =========================================================
# SIDEBAR
# =========================================================
def create_sidebar(parent, systems, switch_page, current_user="Doctor"):

    # =====================================================
    # SIDEBAR FRAME
    # =====================================================
    sidebar = ctk.CTkFrame(
        parent,
        width=250,
        corner_radius=0,
        fg_color=CARD
    )

    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    # =====================================================
    # LOGO / TITLE
    # =====================================================
    ctk.CTkLabel(
        sidebar,
        text="🏥 TRIAGE",
        font=("Segoe UI", 28, "bold"),
        text_color="white"
    ).pack(pady=(30, 5))

    ctk.CTkLabel(
        sidebar,
        text="Emergency Management System",
        font=("Segoe UI", 12),
        text_color="#9CA3AF"
    ).pack(pady=(0, 25))

    # =====================================================
    # USER CARD
    # =====================================================
    user_card = ctk.CTkFrame(
        sidebar,
        fg_color="#1F2937",
        corner_radius=14
    )

    user_card.pack(fill="x", padx=15, pady=(0, 25))

    ctk.CTkLabel(
        user_card,
        text="👤 Logged In",
        font=("Segoe UI", 12),
        text_color="#9CA3AF"
    ).pack(pady=(10, 0))

    ctk.CTkLabel(
        user_card,
        text=current_user,
        font=("Segoe UI", 16, "bold"),
        text_color="white"
    ).pack(pady=(0, 10))

    # =====================================================
    # ACTIVE BUTTON SYSTEM
    # =====================================================
    buttons = []

    def activate_button(active_btn):

        for btn in buttons:
            btn.configure(fg_color=CARD)

        active_btn.configure(fg_color=HOVER)

    # =====================================================
    # BUTTON CREATOR
    # =====================================================
    def create_button(text, page_name):

        btn = ctk.CTkButton(
            sidebar,
            text=text,
            height=45,
            corner_radius=12,
            fg_color=CARD,
            hover_color=HOVER,
            text_color=TEXT,
            anchor="w",
            font=("Segoe UI", 14, "bold"),

            command=lambda: [
                activate_button(btn),
                switch_page(page_name)
            ]
        )

        btn.pack(
            fill="x",
            padx=15,
            pady=6
        )

        buttons.append(btn)

        return btn

    # =====================================================
    # NAVIGATION
    # =====================================================
    home_btn = create_button("🏠  Home", "home")

    create_button("➕  Add Patient", "add")
    create_button("⚕  Treat Patient", "treat")
    create_button("📋  Patient Queue", "queue")
    create_button("📜  History", "history")
    create_button("🔎  Search", "search")

    create_button("👤  Profile", "profile")

    # =====================================================
    # DEFAULT ACTIVE
    # =====================================================
    activate_button(home_btn)

    # =====================================================
    # SYSTEM STATUS
    # =====================================================
    status_frame = ctk.CTkFrame(
        sidebar,
        fg_color="#0F172A",
        corner_radius=12
    )

    status_frame.pack(
        side="bottom",
        fill="x",
        padx=15,
        pady=15
    )

    ctk.CTkLabel(
        status_frame,
        text="● System Online",
        text_color="#22C55E",
        font=("Segoe UI", 12, "bold")
    ).pack(pady=(12, 4))

    ctk.CTkLabel(
        status_frame,
        text="Hospital Triage v2.0",
        text_color="#94A3B8",
        font=("Segoe UI", 11)
    ).pack(pady=(0, 12))

    return sidebar