import tkinter as tk
from tkinter import ttk, messagebox
from models.user import User

class RegisterWindow(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("Register")
        self.geometry("900x600")
        self.configure(bg="#0D4D56")
        self.resizable(False, False)

        # Ana çerçeve
        main_frame = tk.Frame(self, bg="#0D4D56")
        main_frame.pack(fill="both", expand=True)

        # Sol panel (form alanı)
        form_frame = tk.Frame(main_frame, bg="#0D4D56")
        form_frame.place(relx=0.05, rely=0.1, relwidth=0.4, relheight=0.8)

        label_register = tk.Label(form_frame, text="Create Account", font=("Segoe UI", 28, "bold"), fg="white", bg="#0D4D56")
        label_register.pack(pady=(0, 20))

        # Form alanları
        self.create_input(form_frame, "Full Name")
        self.entry_name = self.last_entry

        self.create_input(form_frame, "Email")
        self.entry_email = self.last_entry

        self.create_input(form_frame, "Password", show="*")
        self.entry_password = self.last_entry

        tk.Label(form_frame, text="Role", font=("Segoe UI", 12), fg="white", bg="#0D4D56").pack(pady=(10, 0), anchor="w")
        self.combo_role = ttk.Combobox(form_frame, values=["individual", "company"])
        self.combo_role.pack(pady=5, fill="x")
        self.combo_role.current(0)

        ttk.Button(form_frame, text="Register", command=self.register_user).pack(pady=20)

        # Sağ panel (görsel veya açıklama için boşluk)
        right_frame = tk.Frame(main_frame, bg="white")
        right_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

        tk.Label(right_frame, text="👤 Kayıt ol ve profesyonel ağını oluştur!", font=("Segoe UI", 14, "bold"), fg="#0D4D56", bg="white").pack(pady=40)

    def create_input(self, parent, label_text, show=None):
        tk.Label(parent, text=label_text, font=("Segoe UI", 12), fg="white", bg="#0D4D56").pack(pady=(10, 0), anchor="w")
        entry = ttk.Entry(parent, font=("Segoe UI", 12), show=show)
        entry.pack(pady=5, ipady=5, ipadx=5, fill='x')
        self.last_entry = entry  # bir sonraki satır için girişi tut

    def register_user(self):
        name = self.entry_name.get()
        email = self.entry_email.get()
        password = self.entry_password.get()
        role = self.combo_role.get()

        if not all([name, email, password]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            user = User(fullName=name, email=email, password_hash=password, role=role)
            user.save()
            messagebox.showinfo("Success", "✅ Registration successful!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"❌ Registration failed:\n{e}")
