import customtkinter as ctk
from tkinter import messagebox

from database import (
    create_users_table,
    create_patients_table,
    register_user,
    login_user
)

from triage_queue import TriageSystem

from pages.home_page import home_page
from pages.add_patient_page import add_patient_page
from pages.view_queue_page import view_queue_page
from pages.search_page import search_page
from pages.treat_page import treat_page
from pages.history_page import history_page
from pages.profile_page import profile_page


# =========================================================
# DATABASE SETUP
# =========================================================
try:
    create_users_table()
    create_patients_table()

except Exception as e:
    print("Database Error:", e)


# =========================================================
# APP THEME
# =========================================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# =========================================================
# LOGIN WINDOW
# =========================================================
app = ctk.CTk()

app.geometry("650x520")
app.title("🏥 Hospital Triage System")


# =========================================================
# MAIN LOGIN FRAME
# =========================================================
login_frame = ctk.CTkFrame(
    app,
    corner_radius=20
)

login_frame.place(
    relx=0.5,
    rely=0.5,
    anchor="center"
)


# =========================================================
# TITLE
# =========================================================
ctk.CTkLabel(
    login_frame,
    text="🏥 Hospital System",
    font=("Segoe UI", 30, "bold")
).pack(pady=(30, 10))


ctk.CTkLabel(
    login_frame,
    text="Emergency Triage Management",
    font=("Segoe UI", 14)
).pack(pady=(0, 20))


# =========================================================
# USERNAME
# =========================================================
username = ctk.CTkEntry(
    login_frame,
    placeholder_text="Username",
    width=280,
    height=42
)

username.pack(pady=10)


# =========================================================
# PASSWORD
# =========================================================
password = ctk.CTkEntry(
    login_frame,
    placeholder_text="Password",
    show="*",
    width=280,
    height=42
)

password.pack(pady=10)


# =========================================================
# SHOW PASSWORD
# =========================================================
def toggle_password():

    if password.cget("show") == "*":
        password.configure(show="")

    else:
        password.configure(show="*")


ctk.CTkCheckBox(
    login_frame,
    text="Show Password",
    command=toggle_password
).pack(pady=5)


# =========================================================
# REGISTER WINDOW
# =========================================================
def register():

    register_window = ctk.CTkToplevel(app)

    register_window.geometry("400x320")
    register_window.title("Create Account")

    frame = ctk.CTkFrame(register_window)
    frame.pack(
        expand=True,
        fill="both",
        padx=20,
        pady=20
    )

    ctk.CTkLabel(
        frame,
        text="Create New Account",
        font=("Segoe UI", 24, "bold")
    ).pack(pady=20)

    new_user = ctk.CTkEntry(
        frame,
        placeholder_text="Username",
        width=250
    )

    new_user.pack(pady=10)

    new_pass = ctk.CTkEntry(
        frame,
        placeholder_text="Password",
        show="*",
        width=250
    )

    new_pass.pack(pady=10)

    def save_account():

        user = new_user.get().strip()
        pwd = new_pass.get().strip()

        if not user or not pwd:
            messagebox.showwarning(
                "Missing Fields",
                "Please fill all fields"
            )
            return

        try:

            if register_user(user, pwd):

                messagebox.showinfo(
                    "Success",
                    "Account created successfully"
                )

                register_window.destroy()

            else:
                messagebox.showerror(
                    "Error",
                    "Username already exists"
                )

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

    ctk.CTkButton(
        frame,
        text="Create Account",
        width=250,
        height=40,
        fg_color="#10B981",
        hover_color="#059669",
        command=save_account
    ).pack(pady=20)


# =========================================================
# LOGIN FUNCTION
# =========================================================
def login():

    user = username.get().strip()
    pwd = password.get().strip()

    if not user or not pwd:

        messagebox.showwarning(
            "Missing Fields",
            "Enter username and password"
        )

        return

    try:

        if login_user(user, pwd):

            app.withdraw()
            open_dashboard(user)

        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid username or password"
            )

    except Exception as e:
        messagebox.showerror(
            "System Error",
            str(e)
        )


# =========================================================
# LOGIN BUTTONS
# =========================================================
ctk.CTkButton(
    login_frame,
    text="Login",
    width=280,
    height=42,
    command=login
).pack(pady=(20, 10))


ctk.CTkButton(
    login_frame,
    text="Register",
    width=280,
    height=42,
    fg_color="#10B981",
    hover_color="#059669",
    command=register
).pack(pady=(0, 30))


# =========================================================
# DASHBOARD
# =========================================================
def open_dashboard(user):

    dashboard = ctk.CTkToplevel()

    dashboard.geometry("1400x800")
    dashboard.title("🏥 Hospital Dashboard")

    dashboard.grid_columnconfigure(1, weight=1)
    dashboard.grid_rowconfigure(0, weight=1)

    # =====================================================
    # TRIAGE SYSTEM
    # =====================================================
    systems = TriageSystem()

    try:
        systems.load_from_db(user)

    except:
        pass

    # =====================================================
    # SIDEBAR
    # =====================================================
    sidebar = ctk.CTkFrame(
        dashboard,
        width=260,
        corner_radius=0
    )

    sidebar.grid(row=0, column=0, sticky="ns")

    # =====================================================
    # CONTENT
    # =====================================================
    content = ctk.CTkFrame(dashboard)

    content.grid(
        row=0,
        column=1,
        sticky="nsew",
        padx=10,
        pady=10
    )

    # =====================================================
    # HEADER
    # =====================================================
    header = ctk.CTkFrame(
        content,
        height=70
    )

    header.pack(fill="x", padx=15, pady=15)

    page_title = ctk.CTkLabel(
        header,
        text="Dashboard",
        font=("Segoe UI", 26, "bold")
    )

    page_title.pack(side="left", padx=20)

    # =====================================================
    # PAGE CONTAINER
    # =====================================================
    page_container = ctk.CTkFrame(content)

    page_container.pack(
        expand=True,
        fill="both",
        padx=15,
        pady=(0, 15)
    )

    # =====================================================
    # PAGE ROUTER
    # =====================================================
    def show_page(page, title):

        page_title.configure(text=title)

        for widget in page_container.winfo_children():
            widget.destroy()

        try:

            if page in [profile_page, add_patient_page]:
                page(page_container, systems, user)

            else:
                page(page_container, systems)

        except Exception as e:
            messagebox.showerror(
                "Page Error",
                str(e)
            )

    # =====================================================
    # SIDEBAR TITLE
    # =====================================================
    ctk.CTkLabel(
        sidebar,
        text="🏥 HOSPITAL",
        font=("Segoe UI", 28, "bold")
    ).pack(pady=(30, 10))

    ctk.CTkLabel(
        sidebar,
        text=f"Logged in as\n{user}",
        font=("Segoe UI", 14)
    ).pack(pady=(0, 25))

    # =====================================================
    # NAV BUTTON
    # =====================================================
    def nav_button(text, page, title, color="#1E293B"):

        btn = ctk.CTkButton(
            sidebar,
            text=text,
            height=45,
            corner_radius=12,
            fg_color=color,
            hover_color="#2563EB",
            font=("Segoe UI", 14, "bold"),
            command=lambda: show_page(page, title)
        )

        btn.pack(
            fill="x",
            padx=15,
            pady=6
        )

    # =====================================================
    # NAVIGATION
    # =====================================================
    nav_button("🏠 Home", home_page, "Home")
    nav_button("👤 Profile", profile_page, "Profile")
    nav_button("➕ Add Patient", add_patient_page, "Add Patient")
    nav_button("📋 Queue", view_queue_page, "Queue")
    nav_button("🔍 Search", search_page, "Search")
    nav_button("💊 Treat", treat_page, "Treat Patient")
    nav_button("📜 History", history_page, "History")

    # =====================================================
    # LOGOUT
    # =====================================================
    def logout():

        dashboard.destroy()
        app.deiconify()

    ctk.CTkButton(
        sidebar,
        text="Logout",
        fg_color="#DC2626",
        hover_color="#B91C1C",
        height=45,
        command=logout
    ).pack(
        side="bottom",
        fill="x",
        padx=15,
        pady=20
    )

    # =====================================================
    # LOAD HOME PAGE
    # =====================================================
    show_page(home_page, "Home")


# =========================================================
# RUN APP
# =========================================================
app.mainloop()