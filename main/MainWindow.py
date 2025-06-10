import tkinter as tk
from tkinter import ttk
from main.profile_window import ProfileWindow
from main.company_profile_window import CompanyProfileWindow
from main.skill_window import SkillWindow
from main.job_list_window import JobListWindow
from main.job_post_window import JobPostWindow
from main.application_list_window import ApplicationListWindow
from main.incoming_applications_window import IncomingApplicationsWindow  # ✅ Şirket başvurular penceresi eklendi

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

        # Profil görüntüleme
        ttk.Button(self, text="👤 View Profile", command=self.view_profile).pack(pady=10)

        # Yetenek yönetimi (tüm roller için aktif)
        ttk.Button(self, text="🧠 Skills", command=self.view_skills).pack(pady=10)

        # Rol bazlı iş ilanı ve başvuru işlemleri
        if self.user.role == "company":
            ttk.Button(self, text="📢 Post a Job", command=self.post_job).pack(pady=10)
            ttk.Button(self, text="📨 View Applications", command=self.view_incoming_applications).pack(pady=10)  # ✅ eklendi

        elif self.user.role == "individual":
            ttk.Button(self, text="🔍 Find Jobs", command=self.find_jobs).pack(pady=10)
            ttk.Button(self, text="📋 My Applications", command=self.view_applications).pack(pady=10)

        # Çıkış
        ttk.Button(self, text="🚪 Logout", command=self.logout).pack(pady=20)

    def view_profile(self):
        if self.user.role == "company":
            CompanyProfileWindow(self.user.id)
        else:
            ProfileWindow(self.user.id)

    def view_skills(self):
        SkillWindow(self.user)

    def post_job(self):
        JobPostWindow(self.user)

    def find_jobs(self):
        JobListWindow(self.user)

    def view_applications(self):
        ApplicationListWindow(self.user)

    def view_incoming_applications(self):
        IncomingApplicationsWindow(self.user)

    def logout(self):
        self.destroy()
