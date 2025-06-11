import tkinter as tk
from tkinter import ttk

from main.connection_requests_window import ConnectionRequestsWindow
from main.followed_list_window import FollowedListWindow
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
        if self.user.role == "individual":
            ttk.Button(self, text="🧠 Skills", command=self.view_skills).pack(pady=10)

        # Sosyal ağ butonu (tüm kullanıcılar için aktif)
        ttk.Button(self, text="🌐 Discover People", command=self.open_social_window).pack(pady=10)

        # Takip istekleri
        ttk.Button(self, text="🔗 Connection Requests", command=self.view_connection_requests).pack(pady=10)

        # Takip edenler
        ttk.Button(self, text="👁️ Followers", command=self.view_followers).pack(pady=10)

        # Bağlantılarım
        ttk.Button(self, text="🤝 Connections", command=self.view_connections).pack(pady=10)

        # Takip edilenler
        ttk.Button(self, text="👥 Followed Users", command=self.view_followed_users).pack(pady=10)

        # My job applications
        if self.user.role == "individual":
            ttk.Button(self, text="🔍 Find Jobs", command=self.find_jobs).pack(pady=10)
            ttk.Button(self, text="📄 My Applications", command=self.view_my_applications).pack(pady=10)

        elif self.user.role == "company":
            ttk.Button(self, text="📢 Post a Job", command=self.post_job).pack(pady=10)
            ttk.Button(self, text="📨 View Applications", command=self.view_incoming_applications).pack(pady=10)

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

    def open_social_window(self):
        from main.social_window import SocialWindow
        SocialWindow(self.user.id)

    def view_connection_requests(self):
        ConnectionRequestsWindow(self.user.id)

    def view_incoming_applications(self):
        from main.incoming_applications_window import IncomingApplicationsWindow
        IncomingApplicationsWindow(self.user)

    def view_my_applications(self):
        from main.my_applications_window import MyApplicationsWindow
        MyApplicationsWindow(user_id=self.user.id)

    def view_followed_users(self):
        FollowedListWindow(self.user.id)

    def view_followers(self):
        from main.follower_list_window import FollowerListWindow
        FollowerListWindow(self.user.id)

    def view_connections(self):
        from main.connection_list_window import ConnectionListWindow
        ConnectionListWindow(self.user.id)

    def logout(self):
        self.destroy()
