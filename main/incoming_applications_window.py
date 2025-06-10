import tkinter as tk
from tkinter import ttk, messagebox
from models.application import Application

class IncomingApplicationsWindow(tk.Toplevel):
    def __init__(self, user):
        super().__init__()
        self.title("📨 Incoming Applications")
        self.geometry("800x500")
        self.configure(bg="#f4f4f4")
        self.user = user  # company user

        tk.Label(self, text="Applications to Your Job Posts",
                 font=("Segoe UI", 18, "bold"), bg="#f4f4f4").pack(pady=20)

        # TreeView setup
        columns = ("ID", "Candidate", "Job Title", "Status", "Applied At")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(pady=10, padx=20)

        self.load_data()

        # Action buttons
        btn_frame = tk.Frame(self, bg="#f4f4f4")
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="✅ Accept", command=self.accept_application).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="❌ Reject", command=self.reject_application).grid(row=0, column=1, padx=10)

    def load_data(self):
        applications = Application.get_applications_to_company(self.user.id)
        for app in applications:
            app_id, fullName, job_title, status, applied_at = app
            self.tree.insert("", "end", iid=app_id,
                             values=(app_id, fullName, job_title, status, applied_at.strftime("%Y-%m-%d %H:%M")))

    def accept_application(self):
        self._update_status("accepted")

    def reject_application(self):
        self._update_status("rejected")

    def _update_status(self, status):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an application.")
            return

        app_id = int(selected[0])
        Application.update_status(app_id, status)
        messagebox.showinfo("Updated", f"Application marked as '{status}'")

        # Update status in treeview
        current_values = list(self.tree.item(app_id)["values"])
        current_values[3] = status  # status column index
        self.tree.item(app_id, values=current_values)
