import tkinter as tk
from tkinter import ttk
from models.application import Application

class ApplicationListWindow(tk.Toplevel):
    def __init__(self, user):
        super().__init__()
        self.title("📋 My Applications")
        self.geometry("700x500")
        self.configure(bg="#f2f2f2")

        tk.Label(self, text="My Applications", font=("Segoe UI", 18, "bold"), bg="#f2f2f2").pack(pady=20)

        columns = ("Job Title", "Company", "Status", "Applied At")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=160)
        self.tree.pack(pady=10, padx=20)

        self.load_data(user.id)

    def load_data(self, user_id):
        records = Application.get_applications_by_user(user_id)
        for job_title, company, status, applied_at in records:
            self.tree.insert("", "end", values=(job_title, company, status, applied_at.strftime("%Y-%m-%d %H:%M")))
