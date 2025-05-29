import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

from models.user import User  # Aynı şekilde kullanılabilir
from main.register_window import RegisterWindow  # ✅ YENİ: RegisterWindow import edildi

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.configure(bg="#0D4D56")
        self.geometry("900x600")
        self.resizable(False, False)

        # Ana çerçeve (frame)
        main_frame = tk.Frame(self, bg="#0D4D56")
        main_frame.pack(fill="both", expand=True)

        # Sol: Form alanı
        form_frame = tk.Frame(main_frame, bg="#0D4D56")
        form_frame.place(relx=0.05, rely=0.2, relwidth=0.4, relheight=0.6)

        label_sign_in = tk.Label(form_frame, text="Sign in", font=("Segoe UI", 28, "bold"), fg="white", bg="#0D4D56")
        label_sign_in.pack(pady=(0, 20))

        self.entry_email = ttk.Entry(form_frame, font=("Segoe UI", 12))
        self.entry_email.insert(0, "Enter your e-mail")
        self.entry_email.pack(pady=10, ipady=5, ipadx=5, fill='x')

        self.entry_password = ttk.Entry(form_frame, show="*", font=("Segoe UI", 12))
        self.entry_password.insert(0, "123456")
        self.entry_password.pack(pady=10, ipady=5, ipadx=5, fill='x')

        login_button = ttk.Button(form_frame, text="Login", command=self.handle_login)
        login_button.pack(pady=20)

        # ✅ YENİ: Register butonu
        register_button = ttk.Button(form_frame, text="Don't have an account? Register", command=self.open_register_window)
        register_button.pack(pady=10)

        # Sağ: Görsel alanı
        image_frame = tk.Frame(main_frame, bg="white")
        image_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

        image_path = r"C:\Users\ogsar\OneDrive\Resimler\Screenshots\arkaplan1.png"
        try:
            image = Image.open(image_path)
            image = image.resize((450, 600), Image.ANTIALIAS)
            self.photo = ImageTk.PhotoImage(image)
            image_label = tk.Label(image_frame, image=self.photo, bg="white")
            image_label.pack(fill="both", expand=True)
        except Exception as e:
            error_label = tk.Label(image_frame, text="Görsel yüklenemedi.", bg="white", fg="red")
            error_label.pack(pady=20)

    def handle_login(self):
        email = self.entry_email.get()
        password = self.entry_password.get()

        print(f"🔍 Giriş deneniyor: {email} / {password}")
        user = User.get_user_by_email_and_password(email, password)

        if user:
            messagebox.showinfo("Login Result", f"✅ Hoş geldin, {user.fullName}!")
        else:
            messagebox.showerror("Login Result", "❌ Giriş başarısız. E-posta veya şifre hatalı.")

    # ✅ YENİ: Register penceresini açar
    def open_register_window(self):
        RegisterWindow(self)


if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()
