import tkinter as tk
from tkinter import ttk, messagebox
from models.application import Application

class MyApplicationsWindow(tk.Toplevel):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.title("My Applications")
        self.geometry("700x400")
        self.user_id = user_id

        self.tree = ttk.Treeview(self, columns=("Job Title", "Company", "Status", "Applied At"), show="headings")
        self.tree.heading("Job Title", text="Job Title")
        self.tree.heading("Company", text="Company")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Applied At", text="Applied At")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_applications()

    def load_applications(self):
        applications = Application.get_applications_by_user(self.user_id)
        for app in applications:
            self.tree.insert("", "end", values=app)
