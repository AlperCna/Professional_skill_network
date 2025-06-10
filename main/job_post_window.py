import tkinter as tk
from tkinter import ttk, messagebox
from models.job_post import JobPost

class JobPostWindow(tk.Toplevel):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.title("📢 Create Job Post")
        self.geometry("600x600")
        self.configure(bg="#f2f2f2")

        tk.Label(self, text="New Job Post", font=("Segoe UI", 18, "bold"), bg="#f2f2f2", fg="#0D4D56").pack(pady=20)

        form_frame = tk.Frame(self, bg="#f2f2f2")
        form_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.entries = {}

        # Alan: Title
        self.entries["Title"] = self.create_entry(form_frame, "Job Title")

        # Alan: Description
        self.entries["Description"] = self.create_textarea(form_frame, "Description", height=4)

        # Alan: Requirements
        self.entries["Requirements"] = self.create_textarea(form_frame, "Requirements", height=4)

        # Alan: Job Type
        tk.Label(form_frame, text="Job Type", bg="#f2f2f2", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(10, 0))
        self.combo_type = ttk.Combobox(form_frame, values=["full-time", "part-time", "internship", "remote"], state="readonly")
        self.combo_type.pack(fill="x", pady=5)
        self.combo_type.current(0)

        # Alan: Deadline
        self.entries["Deadline"] = self.create_entry(form_frame, "Application Deadline (YYYY-MM-DD)")

        # Kaydet Butonu
        ttk.Button(self, text="💾 Publish Job", command=self.save_job).pack(pady=20)

    def create_entry(self, parent, label_text):
        tk.Label(parent, text=label_text, font=("Segoe UI", 12, "bold"), bg="#f2f2f2").pack(anchor="w", pady=(10, 0))
        entry = ttk.Entry(parent)
        entry.pack(fill="x", pady=5)
        return entry

    def create_textarea(self, parent, label_text, height=3):
        tk.Label(parent, text=label_text, font=("Segoe UI", 12, "bold"), bg="#f2f2f2").pack(anchor="w", pady=(10, 0))
        text = tk.Text(parent, height=height)
        text.pack(fill="x", pady=5)
        return text

    def save_job(self):
        title = self.entries["Title"].get()
        description = self.entries["Description"].get("1.0", "end").strip()
        requirements = self.entries["Requirements"].get("1.0", "end").strip()
        job_type = self.combo_type.get()
        deadline = self.entries["Deadline"].get()

        if not all([title, description, requirements, job_type, deadline]):
            messagebox.showerror("Error", "Please fill all fields.")
            return

        try:
            job = JobPost(
                company_id=self.user.id,
                title=title,
                description=description,
                requirements=requirements,
                job_type=job_type,
                deadline=deadline
            )
            job.save()
            messagebox.showinfo("Success", "✅ Job posted successfully!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"❌ Failed to post job:\n{e}")
