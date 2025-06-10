import tkinter as tk
from tkinter import ttk, messagebox
from models.job_post import JobPost
from models.application import Application

class JobListWindow(tk.Toplevel):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.title("🔍 Available Jobs")
        self.geometry("800x600")
        self.configure(bg="#f2f2f2")

        tk.Label(self, text="Job Listings", font=("Segoe UI", 18, "bold"),
                 bg="#f2f2f2", fg="#0D4D56").pack(pady=20)

        # TreeView tablosu
        columns = ("Title", "Company", "Type", "Deadline")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180)
        self.tree.pack(pady=10)

        # Seçim tetikleyicisi
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        self.load_jobs()

    def load_jobs(self):
        print("load_jobs çalışıyor")
        jobs = JobPost.get_all_for_listing()
        for job in jobs:
            self.tree.insert(
                "", "end", iid=job.id,
                values=(job.title, job.company_name, job.job_type, job.deadline)
            )

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        job_id = int(selected[0])
        job = self.get_job_by_id(job_id)
        if not job:
            return

        # Detay penceresi
        detail_win = tk.Toplevel(self)
        detail_win.title("📄 Job Details")
        detail_win.geometry("500x500")
        detail_win.configure(bg="#ffffff")

        tk.Label(detail_win, text=job.title, font=("Segoe UI", 16, "bold"), bg="#ffffff").pack(pady=10)
        tk.Label(detail_win, text=f"Company: {job.company_name}", font=("Segoe UI", 12), bg="#ffffff").pack()
        tk.Label(detail_win, text=f"Type: {job.job_type}", font=("Segoe UI", 12), bg="#ffffff").pack()
        tk.Label(detail_win, text=f"Deadline: {job.deadline}", font=("Segoe UI", 12), bg="#ffffff").pack()

        tk.Label(detail_win, text="Description", font=("Segoe UI", 12, "bold"), bg="#ffffff").pack(pady=(15, 0))
        tk.Message(detail_win, text=job.description, width=450, bg="#f8f8f8").pack()

        tk.Label(detail_win, text="Requirements", font=("Segoe UI", 12, "bold"), bg="#ffffff").pack(pady=(10, 0))
        tk.Message(detail_win, text=job.requirements, width=450, bg="#f8f8f8").pack()

        def apply():
            if Application.has_applied(self.user.id, job.id):
                messagebox.showinfo("Already Applied", "You have already applied.")
            else:
                Application(self.user.id, job.id).save()
                messagebox.showinfo("Applied", "Your application has been submitted.")
            detail_win.destroy()

        ttk.Button(detail_win, text="📩 Apply for this job", command=apply).pack(pady=20)

    def get_job_by_id(self, job_id):
        print("get_job_by_id çalışıyor")
        all_jobs = JobPost.get_all()
        for job in all_jobs:
            if job.id == job_id:
                return job
        return None
