from tkinter import *
from tkinter import ttk, messagebox
from models.job_post import JobPost
from models.application import Application


class JobListWindow(Toplevel):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.title("🔍 Available Jobs")
        self.geometry("800x600")
        self.configure(bg="#f2f2f2")

        Label(self, text="Job Listings", font=("Segoe UI", 18, "bold"), bg="#f2f2f2", fg="#0D4D56").pack(pady=20)

        # Treeview
        columns = ("Title", "Company", "Type", "Deadline")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180)
        self.tree.pack(pady=10)

        # Başvuru Butonu
        ttk.Button(self, text="📩 Apply to Selected", command=self.apply_to_selected).pack(pady=10)

        self.load_jobs()

    def load_jobs(self):
        jobs = JobPost.get_all()
        for job in jobs:
            # company_id ile company_name yerine sadece ID gösteriyoruz, istersen CompanyProfile ekleyebilirim
            self.tree.insert("", "end", iid=job.id, values=(job.title, f"Company {job.company_id}", job.job_type, job.deadline))

    def apply_to_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a job to apply.")
            return

        job_id = int(selected[0])

        # Daha önce başvurmuş mu kontrol et
        if Application.has_applied(self.user.id, job_id):
            messagebox.showinfo("Already Applied", "❗ You have already applied to this job.")
            return

        try:
            app = Application(user_id=self.user.id, job_id=job_id)
            app.save()
            messagebox.showinfo("Success", "✅ Application submitted!")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Failed to apply:\n{e}")
