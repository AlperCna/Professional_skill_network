import tkinter as tk
from tkinter import ttk
from models.follow import Follow
from models.user import User

class FollowerListWindow(tk.Toplevel):
    def __init__(self, user_id):
        super().__init__()
        self.title("👥 Your Followers")
        self.geometry("600x400")
        self.configure(bg="white")

        tk.Label(self, text="Users Following You", font=("Segoe UI", 16, "bold"), bg="white").pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("ID", "Full Name", "Email"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Full Name", text="Full Name")
        self.tree.heading("Email", text="Email")
        self.tree.pack(fill="both", expand=True)

        self.load_followers(user_id)

    def load_followers(self, user_id):
        followers = Follow.get_followers(user_id)
        for fid in followers:
            user = User.get_user_by_id(fid)
            if user:
                self.tree.insert("", "end", values=(user.id, user.fullName, user.email))
