import tkinter as tk
from tkinter import ttk
from main.profile_window import ProfileWindow  # Profil penceresini dahil ediyoruz

class MainWindow(tk.Toplevel):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.title("Professional Skill Network - Main Page")
        self.geometry("800x500")
        self.configure(bg="#f4f4f4")
        self.user = user

        # Hoş geldin mesajı
        greeting = f"Welcome, {user.fullName} ({user.role})"
        tk.Label(self, text=greeting, font=("Segoe UI", 16, "bold"), bg="#f4f4f4", fg="#0D4D56").pack(pady=20)

        # Butonlar
        ttk.Button(self, text="View Profile", command=self.view_profile).pack(pady=10)
        ttk.Button(self, text="Skills", command=self.view_skills).pack(pady=10)

        if user.role == "company":
            ttk.Button(self, text="Post a Job", command=self.post_job).pack(pady=10)
        elif user.role == "individual":
            ttk.Button(self, text="Find Jobs", command=self.find_jobs).pack(pady=10)

        ttk.Button(self, text="Logout", command=self.logout).pack(pady=20)

    def view_profile(self):
        # Profil penceresini aç
        ProfileWindow(self.user.id)

    def view_skills(self):
        print("Skills button clicked")  # Daha sonra eklenecek

    def post_job(self):
        print("Post job button clicked")  # Daha sonra eklenecek

    def find_jobs(self):
        print("Find job button clicked")  # Daha sonra eklenecek

    def logout(self):
        self.destroy()
