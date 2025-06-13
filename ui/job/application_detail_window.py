import tkinter as tk
from tkinter import ttk, messagebox
import os
import webbrowser

from models.application import Application
from models.application_skill import ApplicationSkill
from models.user import User
from models.job_post import JobPost

class ApplicationDetailWindow(tk.Toplevel):
    def __init__(self, application_id):
        super().__init__()
        self.title("📄 Application Details")
        self.geometry("600x500")
        self.configure(bg="#f7f7f7")

        self.application_id = application_id

        self.init_ui()

    def init_ui(self):
        # Başlık
        tk.Label(self, text="Application Details", font=("Segoe UI", 18, "bold"), bg="#f7f7f7", fg="#0D4D56").pack(pady=20)

        # Verileri çek
        app = self.get_application()
        if not app:
            messagebox.showerror("Error", "Application not found.")
            self.destroy()
            return

        user = self.get_user(app.user_id)
        job = self.get_job(app.job_id)
        skills = ApplicationSkill.get_skills_for_application(self.application_id)
        cv_path = app.cv_path

        form_frame = tk.Frame(self, bg="#f7f7f7")
        form_frame.pack(padx=20, fill="both", expand=True)

        # Aday bilgileri
        ttk.Label(form_frame, text=f"👤 Candidate: {user.fullName}").pack(anchor="w", pady=5)
        ttk.Label(form_frame, text=f"📧 Email: {user.email}").pack(anchor="w", pady=5)

        # İş bilgileri
        ttk.Label(form_frame, text=f"💼 Job Title: {job.title}").pack(anchor="w", pady=5)
        ttk.Label(form_frame, text=f"🏢 Company: {job.company_name}").pack(anchor="w", pady=5)

        # Yetenekler
        ttk.Label(form_frame, text="🧠 Skills:", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(10, 0))
        for skill in skills:
            ttk.Label(form_frame, text=f"• {skill}").pack(anchor="w")

        # CV Görüntüleme
        ttk.Label(form_frame, text="📎 CV File:", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(15, 0))
        if cv_path and os.path.exists(cv_path):
            open_btn = ttk.Button(form_frame, text="Open CV", command=lambda: webbrowser.open(cv_path))
            open_btn.pack(anchor="w", pady=5)
        else:
            ttk.Label(form_frame, text="No CV uploaded.").pack(anchor="w", pady=5)

    def get_application(self):
        conn = None
        try:
            from db.db_config import get_connection
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, user_id, job_id, status, applied_at, cv_path FROM Application WHERE id = %s", (self.application_id,))
            result = cursor.fetchone()
            if result:
                app = Application(
                    id=result[0], user_id=result[1], job_id=result[2],
                    status=result[3], applied_at=result[4]
                )
                app.cv_path = result[5]
                return app
        except Exception as e:
            print("⚠️ get_application hatası:", e)
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
        return None

    def get_user(self, user_id):
        return User.get_user_by_id(user_id)

    def get_job(self, job_id):
        all_jobs = JobPost.get_all()
        for job in all_jobs:
            if job.id == job_id:
                return job
        return None
