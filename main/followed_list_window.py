import tkinter as tk
from tkinter import ttk, messagebox
from db.db_config import get_connection
from models.user import User
from models.follow import Follow


class FollowedListWindow(tk.Toplevel):
    def __init__(self, user_id):
        super().__init__()
        self.title("👥 Followed Users")
        self.geometry("600x400")
        self.configure(bg="#ffffff")
        self.user_id = user_id

        tk.Label(self, text="Users You Follow", font=("Segoe UI", 18, "bold"), bg="white", fg="#0D4D56").pack(pady=15)

        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Email"), show="headings")
        self.tree.heading("ID", text="User ID")
        self.tree.heading("Name", text="Full Name")
        self.tree.heading("Email", text="Email")
        self.tree.pack(padx=20, pady=10, fill="both", expand=True)

        self.load_followed_users()

    def load_followed_users(self):
        followed_ids = Follow.get_followings(self.user_id)

        if not followed_ids:
            messagebox.showinfo("Info", "You are not following anyone yet.")
            return

        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = "SELECT id, fullName, email FROM users WHERE id IN (%s)" % ",".join(["%s"] * len(followed_ids))
            cursor.execute(query, tuple(followed_ids))
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Hata", f"Kullanıcılar getirilemedi: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
