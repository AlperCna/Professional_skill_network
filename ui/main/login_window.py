import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from ui.main.MainWindow import MainWindow
from models.user import User
from ui.main.register_window import RegisterWindow

IMAGE_PATH = r"C:\Users\ogsar\Downloads\496c22bea2c410b12d1bde2918a1088c.jpg"

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.configure(bg="#0D4D56")
        self.geometry("900x600")
        self.resizable(True, True)

        main_frame = tk.Frame(self, bg="#0D4D56")
        main_frame.pack(fill="both", expand=True)

        form_frame = tk.Frame(main_frame, bg="#0D4D56")
        form_frame.place(relx=0.05, rely=0.2, relwidth=0.4, relheight=0.6)

        tk.Label(form_frame, text="Sign in", font=("Segoe UI", 28, "bold"), fg="white", bg="#0D4D56").pack(pady=(0, 20))

        # E-POSTA ALANI
        self.entry_email = ttk.Entry(form_frame, font=("Segoe UI", 12), foreground="gray")
        self.entry_email.insert(0, "Enter your e-mail")
        self.entry_email.bind("<FocusIn>", lambda e: self.clear_placeholder(e, "Enter your e-mail"))
        self.entry_email.bind("<FocusOut>", lambda e: self.add_placeholder(e, "Enter your e-mail"))
        self.entry_email.pack(pady=10, ipady=5, ipadx=5, fill='x')

        # ŞİFRE ALANI
        self.entry_password = ttk.Entry(form_frame, font=("Segoe UI", 12), foreground="gray")
        self.entry_password.insert(0, "Enter your password")
        self.entry_password.bind("<FocusIn>", self.clear_password)
        self.entry_password.bind("<FocusOut>", self.reset_password)
        self.entry_password.pack(pady=10, ipady=5, ipadx=5, fill='x')

        ttk.Button(form_frame, text="Login", command=self.handle_login).pack(pady=20)
        ttk.Button(form_frame, text="Don't have an account? Register", command=self.open_register_window).pack(pady=10)

        # Yeni görsel yükleme yöntemi
        self.add_image_section(main_frame)

    def clear_placeholder(self, event, placeholder):
        entry = event.widget
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.config(foreground="black")

    def add_placeholder(self, event, placeholder):
        entry = event.widget
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(foreground="gray")

    def add_image_section(self, parent):
        image_frame = tk.Frame(parent, bg="white")
        image_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

        if os.path.exists(IMAGE_PATH):
            try:
                image = Image.open(IMAGE_PATH)
                image = image.resize((450, 600), Image.Resampling.LANCZOS)
                self.photo = ImageTk.PhotoImage(image)
                tk.Label(image_frame, image=self.photo, bg="white").pack(fill="both", expand=True)
            except Exception as e:
                tk.Label(image_frame, text=f"⚠️ Görsel yüklenemedi {e}", bg="white", fg="red").pack(pady=20)
        else:
            tk.Label(image_frame, text="🖼️ No image found.\nUpdate IMAGE_PATH to add one.",
                     bg="white", fg="gray", font=("Segoe UI", 12)).pack(expand=True)

    def clear_password(self, event):
        if self.entry_password.get() == "Enter your password":
            self.entry_password.delete(0, "end")
            self.entry_password.config(foreground="black", show="*")

    def reset_password(self, event):
        if not self.entry_password.get():
            self.entry_password.insert(0, "Enter your password")
            self.entry_password.config(foreground="gray", show="")

    def handle_login(self):
        email = self.entry_email.get()
        password = self.entry_password.get()

        if email == "Enter your e-mail" or password == "Enter your password":
            messagebox.showwarning("Eksik Bilgi", "Lütfen e-posta ve şifre giriniz.")
            return

        print(f"🔍 Giriş deneniyor: {email} / {password}")
        user = User.get_user_by_email_and_password(email, password)

        if user:
            self.withdraw()
            MainWindow(self, user)
        else:
            messagebox.showerror("Login Result", "❌ Giriş başarısız. E-posta veya şifre hatalı.")

    def open_register_window(self):
        RegisterWindow(self)


if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()
