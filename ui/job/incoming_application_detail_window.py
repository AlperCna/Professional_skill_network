import tkinter as tk
from tkinter import ttk, messagebox
import os
import webbrowser

from models.application import Application
from models.application_skill import ApplicationSkill


class IncomingApplicationDetailWindow(tk.Toplevel):
    def __init__(self, application_id, refresh_callback=None):
        super().__init__()
        self.title("📨 Incoming Application Details")
        self.geometry("600x550")
        self.configure(bg="white")

        self.application_id = application_id
        self.refresh_callback = refresh_callback

        self.init_ui()

    def init_ui(self):
        # Veriyi getir
        app = Application.get_application_detail(self.application_id)
        if not app:
            messagebox.showerror("Error", "Application not found.")
            self.destroy()
            return

        skills = ApplicationSkill.get_skills_for_application(self.application_id)

        # Başlık
        tk.Label(self, text="Incoming Application", font=("Segoe UI", 16, "bold"), bg="white").pack(pady=10)

        frame = tk.Frame(self, bg="white")
        frame.pack(padx=20, fill="both", expand=True)

        # Aday ve iş bilgileri
        ttk.Label(frame, text=f"👤 Candidate: {app['candidate_name']}").pack(anchor="w", pady=3)
        ttk.Label(frame, text=f"📧 Email: {app['candidate_email']}").pack(anchor="w", pady=3)
        ttk.Label(frame, text=f"💼 Job Title: {app['job_title']}").pack(anchor="w", pady=3)
        ttk.Label(frame, text=f"🕓 Applied At: {app['applied_at']}").pack(anchor="w", pady=3)
        ttk.Label(frame, text=f"📌 Status: {app['status']}").pack(anchor="w", pady=3)

        # Yetenekler
        ttk.Label(frame, text="🧠 Skills:", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(10, 0))
        for skill in skills:
            ttk.Label(frame, text=f"• {skill}").pack(anchor="w")

        # CV Dosyası
        ttk.Label(frame, text="📎 CV File:", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(15, 0))
        if app["cv_file"] and os.path.exists(app["cv_file"]):
            ttk.Button(frame, text="Open CV", command=lambda: webbrowser.open(app["cv_file"])).pack(anchor="w", pady=5)
        else:
            ttk.Label(frame, text="No CV uploaded.").pack(anchor="w", pady=5)

        # Onay / Red Butonları
        btn_frame = tk.Frame(self, bg="white")
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="✅ Accept", command=lambda: self.update_status("accepted")).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="❌ Reject", command=lambda: self.update_status("rejected")).grid(row=0, column=1, padx=10)

    def update_status(self, new_status):
        Application.update_status(self.application_id, new_status)
        messagebox.showinfo("Başarılı", f"Başvuru '{new_status}' olarak güncellendi.")
        if self.refresh_callback:
            self.refresh_callback()
        self.destroy()
