import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
from dashboard import RMS

class AuthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1350x700+110+80")
        self.root.minsize(1350, 700)
        self.root.config(bg="#f4f7fa")

        self.base_dir = os.path.dirname(__file__)
        self.db_path = os.path.join(self.base_dir, "rms.db")

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_var   = tk.StringVar()

        self.card = tk.Frame(self.root, bg="#ffffff", bd=0)
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=620, height=680)

        tk.Frame(self.card, bg="#e8ecef", bd=0).place(x=8, y=8, relwidth=1, relheight=1, width=-16, height=-16)
        self.main_container = tk.Frame(self.card, bg="#ffffff", bd=1, relief="flat")
        self.main_container.place(x=20, y=20, relwidth=1, relheight=1, width=-40, height=-40)

        header = tk.Frame(self.main_container, bg="#2c5282", height=140)
        header.pack(fill="x")
        tk.Label(header,text="Student Result\nManagement System",
                 font=("Helvetica", 28, "bold"), bg="#2c5282", fg="white").pack(pady=(35, 0))

        self.show_login()

    def clear_content(self):
        for widget in self.main_container.winfo_children():
            if isinstance(widget, tk.Frame) and widget != self.main_container.winfo_children()[0]:
                widget.destroy()

    def toggle_password_visibility(self, entry_widget, toggle_button):
        if entry_widget.cget("show") == "•":
            entry_widget.config(show="")
            toggle_button.config(text="Hide")
        else:
            entry_widget.config(show="•")
            toggle_button.config(text="Show")

    def create_modern_button(self, parent, text, command, bg_color="#3182ce", hover_color="#2b6cb0"):
        btn = tk.Button(
            parent,
            text=text.upper(),
            font=("Arial", 15, "bold"),
            bg=bg_color,
            fg="white",
            activebackground=hover_color,
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=60,
            pady=14,
            cursor="hand2",
            command=command
        )
        btn.pack(pady=35, padx=100)

        def on_enter(e): btn.config(bg=hover_color)
        def on_leave(e): btn.config(bg=bg_color)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    def show_login(self):
        self.clear_content()
        self.root.title("Login - Student Result Management System")

        content = tk.Frame(self.main_container, bg="#ffffff")
        content.pack(expand=True, fill="both", pady=(20, 0))

        tk.Label(content, text="Sign in to continue",
                 font=("Arial", 16), bg="#ffffff", fg="#4a5568").pack(pady=(0, 50))

        ttk.Label(content, text="Username", background="#ffffff", font=("Arial", 12)).pack(anchor="w", padx=100, pady=(0,6))
        self.username_entry = ttk.Entry(content, textvariable=self.username_var, font=("Arial", 14), width=40)
        self.username_entry.pack(padx=100, pady=6, ipady=10)

        pw_container = tk.Frame(content, bg="#ffffff")
        pw_container.pack(fill="x", padx=100, pady=(25, 0))

        ttk.Label(pw_container, text="Password", background="#ffffff", font=("Arial", 12)).pack(anchor="w")

        pass_frame = tk.Frame(pw_container, bg="#ffffff")
        pass_frame.pack(fill="x", pady=6)

        self.password_entry = ttk.Entry(pass_frame, textvariable=self.password_var, show="•", font=("Arial", 14), width=40)
        self.password_entry.pack(side="left", ipady=10, expand=True, fill="x")

        eye_btn = tk.Button(pass_frame, text="Show", font=("Arial", 11),
                            fg="#3182ce", bg="#ffffff", bd=0, cursor="hand2",
                            command=lambda: self.toggle_password_visibility(self.password_entry, eye_btn))
        eye_btn.pack(side="right", padx=(15, 0))

        self.create_modern_button(content, "Login", self.login, bg_color="#3182ce", hover_color="#2b6cb0")

        link_frame = tk.Frame(content, bg="#ffffff")
        link_frame.pack(pady=10)
        tk.Label(link_frame, text="Don't have an account? ", font=("Arial", 12), bg="#ffffff", fg="#4a5568").pack(side="left")
        tk.Button(link_frame, text="Sign up", command=self.show_register,
                  font=("Arial", 12, "underline"), fg="#3182ce", bg="#ffffff", bd=0, cursor="hand2").pack(side="left")

        self.username_entry.focus()

    def show_register(self):
            self.clear_content()
            self.root.title("Register - Student Result Management System")

            content = tk.Frame(self.main_container, bg="#ffffff")
            content.pack(expand=True, fill="both", pady=(20, 0))

            tk.Label(content, text="Create your account",
                    font=("Arial", 16), bg="#ffffff", fg="#4a5568").pack(pady=(0, 50))

            ttk.Label(content, text="Username", background="#ffffff", font=("Arial", 12)).pack(anchor="w", padx=100, pady=(0,6))
            ttk.Entry(content, textvariable=self.username_var, font=("Arial", 14), width=40).pack(padx=100, pady=6, ipady=10)

            pw_container = tk.Frame(content, bg="#ffffff")
            pw_container.pack(fill="x", padx=100, pady=(25, 0))

            ttk.Label(pw_container, text="Password", background="#ffffff", font=("Arial", 12)).pack(anchor="w")

            pass_frame = tk.Frame(pw_container, bg="#ffffff")
            pass_frame.pack(fill="x", pady=6)

            self.reg_password_entry = ttk.Entry(pass_frame, textvariable=self.password_var, show="•", font=("Arial", 14), width=40)
            self.reg_password_entry.pack(side="left", ipady=10, expand=True, fill="x")

            eye_reg = tk.Button(pass_frame, text="Show", font=("Arial", 11),
                                fg="#3182ce", bg="#ffffff", bd=0, cursor="hand2",
                                command=lambda: self.toggle_password_visibility(self.reg_password_entry, eye_reg))
            eye_reg.pack(side="right", padx=(15, 0))

            ttk.Label(content, text="Confirm Password", background="#ffffff", font=("Arial", 12)).pack(anchor="w", padx=100, pady=(25,6))
            ttk.Entry(content, textvariable=self.confirm_var, show="•", font=("Arial", 14), width=40).pack(padx=100, pady=6, ipady=10)

            self.create_modern_button(content, "Create Account", self.register, bg_color="#38a169", hover_color="#2f855a")

            # Back to Login - made more visible
            back_frame = tk.Frame(content, bg="#ffffff")
            back_frame.pack(pady=40, fill="x")  # increased pady

            back_btn = tk.Button(
                back_frame,
                text="← Back to Login",
                font=("Arial", 14, "bold"),
                fg="#3182ce",
                bg="#f0f4f8",               # light background to stand out
                activeforeground="#2b6cb0",
                activebackground="#e2e8f0",
                relief="flat",
                bd=1,                       # slight border
                padx=30,
                pady=12,
                cursor="hand2",
                command=self.show_login
            )
            back_btn.pack()

            # Hover effect for visibility
            def on_enter(e):
                back_btn.config(bg="#e2e8f0", fg="#2b6cb0", relief="raised")
            def on_leave(e):
                back_btn.config(bg="#f0f4f8", fg="#3182ce", relief="flat")

            back_btn.bind("<Enter>", on_enter)
            back_btn.bind("<Leave>", on_leave)

    def register(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()
        confirm  = self.confirm_var.get()

        if not username or not password:
            messagebox.showwarning("Required", "Username and password are required")
            return
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return

        try:
            with sqlite3.connect(self.db_path) as con:
                cur = con.cursor()
                cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                con.commit()
            messagebox.showinfo("Success", "Account created successfully!\nYou can now log in.")
            self.username_var.set("")
            self.password_var.set("")
            self.confirm_var.set("")
            self.show_login()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "This username is already taken.")
        except Exception as ex:
            messagebox.showerror("Database Error", str(ex))

    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()

        if not username or not password:
            messagebox.showwarning("Required", "Please enter username and password")
            return

        try:
            with sqlite3.connect(self.db_path) as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
                if cur.fetchone():
                    self.card.destroy()
                    self.root.config(bg="white")
                    self.root.title("Student Result Management System - Dashboard")
                    RMS(self.root)
                else:
                    messagebox.showerror("Login Failed", "Incorrect username or password")
        except Exception as ex:
            messagebox.showerror("Error", f"Login error: {str(ex)}")


if __name__ == "__main__":
    root = tk.Tk()
    AuthApp(root)
    root.mainloop()