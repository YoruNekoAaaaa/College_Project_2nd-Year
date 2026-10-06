import customtkinter as ctk
from tkinter import messagebox

from database import (
    change_password,
    delete_account
)


# =========================================================
# PROFILE PAGE
# =========================================================
def profile_page(frame, systems, username):

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
    RED = "#EF4444"

    # =====================================================
    # PAGE CONFIG
    # =====================================================
    frame.configure(fg_color=BG)

    # =====================================================
    # SCROLLABLE CONTAINER
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
        text="👤 Profile Settings",
        font=("Segoe UI", 30, "bold"),
        text_color="white"
    ).pack(anchor="w", pady=(10, 0))

    ctk.CTkLabel(
        container,
        text=f"Logged in as: {username}",
        font=("Segoe UI", 14),
        text_color=MUTED
    ).pack(anchor="w", pady=(0, 10))

    # =====================================================
    # ACCOUNT CARD
    # =====================================================
    account_card = ctk.CTkFrame(
        container,
        fg_color=CARD,
        corner_radius=18,
        border_width=1,
        border_color=BORDER
    )

    account_card.pack(
        fill="x",
        pady=(0, 20)
    )

    # =====================================================
    # ACCOUNT INFO
    # =====================================================
    ctk.CTkLabel(
        account_card,
        text="👨‍⚕ Account Information",
        font=("Segoe UI", 20, "bold"),
        text_color="white"
    ).pack(anchor="w", padx=20, pady=(20, 10))

    info_frame = ctk.CTkFrame(
        account_card,
        fg_color="#0F172A",
        corner_radius=12
    )

    info_frame.pack(
        fill="x",
        padx=20,
        pady=(0, 20)
    )

    ctk.CTkLabel(
        info_frame,
        text=f"Username: {username}",
        font=("Segoe UI", 14),
        text_color=TEXT
    ).pack(anchor="w", padx=15, pady=(15, 5))

    ctk.CTkLabel(
        info_frame,
        text="Role: Hospital Staff",
        font=("Segoe UI", 14),
        text_color=TEXT
    ).pack(anchor="w", padx=15, pady=(0, 15))

    # =====================================================
    # PASSWORD CARD
    # =====================================================
    password_card = ctk.CTkFrame(
        container,
        fg_color=CARD,
        corner_radius=18,
        border_width=1,
        border_color=BORDER
    )

    password_card.pack(
        fill="x",
        pady=(0, 20)
    )

    ctk.CTkLabel(
        password_card,
        text="🔐 Change Password",
        font=("Segoe UI", 20, "bold"),
        text_color="white"
    ).pack(anchor="w", padx=20, pady=(20, 15))

    # =====================================================
    # STATUS LABEL
    # =====================================================
    status = ctk.CTkLabel(
        password_card,
        text="",
        font=("Segoe UI", 13),
        text_color=MUTED
    )

    status.pack(anchor="w", padx=20, pady=(0, 10))

    # =====================================================
    # INPUT CREATOR
    # =====================================================
    def create_input(label_text, placeholder):

        wrapper = ctk.CTkFrame(
            password_card,
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
            show="*",
            height=42,
            corner_radius=10
        )

        entry.pack(fill="x")

        return entry

    # =====================================================
    # INPUTS
    # =====================================================
    new_pass = create_input(
        "New Password",
        "Enter new password"
    )

    confirm_pass = create_input(
        "Confirm Password",
        "Confirm new password"
    )

    # =====================================================
    # PASSWORD VISIBILITY
    # =====================================================
    show_password = ctk.BooleanVar(value=False)

    def toggle_password():

        if show_password.get():

            new_pass.configure(show="")
            confirm_pass.configure(show="")

        else:

            new_pass.configure(show="*")
            confirm_pass.configure(show="*")

    ctk.CTkCheckBox(
        password_card,
        text="Show Password",
        variable=show_password,
        command=toggle_password
    ).pack(anchor="w", padx=20, pady=(5, 10))

    # =====================================================
    # UPDATE PASSWORD
    # =====================================================
    def update_pass():

        status.configure(
            text="",
            text_color=MUTED
        )

        password1 = new_pass.get().strip()
        password2 = confirm_pass.get().strip()

        # =================================================
        # VALIDATION
        # =================================================
        if not password1 or not password2:

            status.configure(
                text="⚠ Please fill all password fields",
                text_color=RED
            )

            return

        if len(password1) < 4:

            status.configure(
                text="⚠ Password must be at least 4 characters",
                text_color=RED
            )

            return

        if password1 != password2:

            status.configure(
                text="⚠ Passwords do not match",
                text_color=RED
            )

            return

        # =================================================
        # UPDATE DATABASE
        # =================================================
        try:

            change_password(
                username,
                password1
            )

            status.configure(
                text="✅ Password updated successfully",
                text_color=GREEN
            )

            messagebox.showinfo(
                "Success",
                "Password updated successfully"
            )

            new_pass.delete(0, "end")
            confirm_pass.delete(0, "end")

        except Exception as e:

            status.configure(
                text="⚠ Failed to update password",
                text_color=RED
            )

            messagebox.showerror(
                "Database Error",
                str(e)
            )

    # =====================================================
    # UPDATE BUTTON
    # =====================================================
    ctk.CTkButton(
        password_card,
        text="🔐 Update Password",
        height=45,
        corner_radius=12,
        fg_color=BLUE,
        hover_color="#2563EB",
        font=("Segoe UI", 14, "bold"),
        command=update_pass
    ).pack(
        fill="x",
        padx=20,
        pady=(10, 20)
    )

    # =====================================================
    # DANGER ZONE
    # =====================================================
    danger_card = ctk.CTkFrame(
        container,
        fg_color="#1F1111",
        corner_radius=18,
        border_width=1,
        border_color="#3A1F1F"
    )

    danger_card.pack(fill="x", pady=(0, 20))

    ctk.CTkLabel(
        danger_card,
        text="⚠ Danger Zone",
        font=("Segoe UI", 20, "bold"),
        text_color=RED
    ).pack(anchor="w", padx=20, pady=(20, 10))

    ctk.CTkLabel(
        danger_card,
        text="Deleting your account is permanent and cannot be undone.",
        font=("Segoe UI", 13),
        text_color=MUTED
    ).pack(anchor="w", padx=20)

    # =====================================================
    # DELETE ACCOUNT
    # =====================================================
    def delete_user():

        confirm = messagebox.askyesno(
            "Delete Account",
            "Are you sure you want to permanently delete your account?"
        )

        if not confirm:
            return

        try:

            delete_account(username)

            messagebox.showinfo(
                "Account Deleted",
                "Your account has been deleted successfully"
            )

            frame.quit()

        except Exception as e:

            messagebox.showerror(
                "Delete Failed",
                str(e)
            )

    # =====================================================
    # DELETE BUTTON
    # =====================================================
    ctk.CTkButton(
        danger_card,
        text="🗑 Delete Account",
        height=45,
        corner_radius=12,
        fg_color=RED,
        hover_color="#DC2626",
        font=("Segoe UI", 14, "bold"),
        command=delete_user
    ).pack(
        fill="x",
        padx=20,
        pady=20
    )