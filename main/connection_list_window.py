import tkinter as tk
from tkinter import ttk
from models.connection import Connection
from models.user import User

class ConnectionListWindow(tk.Toplevel):
    def __init__(self, user_id):
        super().__init__()
        self.title("🤝 Connections")
        self.geometry("600x400")
        self.configure(bg="white")

        tk.Label(self, text="Your Connections", font=("Segoe UI", 16, "bold"), bg="white").pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("ID", "Full Name", "Email"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Full Name", text="Full Name")
        self.tree.heading("Email", text="Email")
        self.tree.pack(fill="both", expand=True)

        self.load_connections(user_id)

    def load_connections(self, user_id):
        connections = Connection.get_connections(user_id)
        for u1, u2, _ in connections:
            other_id = u2 if u1 == user_id else u1
            user = User.get_user_by_id(other_id)
            if user:
                self.tree.insert("", "end", values=(user.id, user.fullName, user.email))
