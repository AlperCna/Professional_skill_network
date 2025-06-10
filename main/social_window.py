import tkinter as tk
from tkinter import ttk, messagebox

from models.connection import Connection
from models.follow import Follow
from models.user import User  # Kullanıcı bilgilerini getirmek için
from db.db_config import get_connection


class SocialWindow(tk.Toplevel):
    def __init__(self, current_user_id, parent=None):
        super().__init__(parent)
        self.title("Social Network")
        self.geometry("800x600")
        self.configure(bg="white")
        self.current_user_id = current_user_id

        self.create_widgets()
        self.load_users()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Email"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Email", text="Email")
        self.tree.pack(pady=10, fill="both", expand=True)

        btn_frame = tk.Frame(self, bg="white")
        btn_frame.pack(pady=10)

        self.btn_connect = ttk.Button(btn_frame, text="Bağlantı İsteği Gönder", command=self.send_connection_request)
        self.btn_connect.grid(row=0, column=0, padx=10)

        self.btn_follow = ttk.Button(btn_frame, text="Takip Et", command=self.follow_user)
        self.btn_follow.grid(row=0, column=1, padx=10)

        self.btn_unfollow = ttk.Button(btn_frame, text="Takibi Bırak", command=self.unfollow_user)
        self.btn_unfollow.grid(row=0, column=2, padx=10)

    def load_users(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = "SELECT id, fullName, email FROM users WHERE id != %s"
            cursor.execute(query, (self.current_user_id,))
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Hata", f"Kullanıcılar yüklenemedi: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def get_selected_user_id(self):
        selected = self.tree.selection()
        if not selected:
            return None
        return int(self.tree.item(selected[0])["values"][0])

    def send_connection_request(self):
        target_id = self.get_selected_user_id()
        if not target_id:
            messagebox.showwarning("Seçim yok", "Lütfen bir kullanıcı seçin.")
            return

        # Bağlantı kontrolü
        existing = Connection.get_connections(self.current_user_id)
        for sender, receiver, status in existing:
            if (sender == self.current_user_id and receiver == target_id) or (
                    receiver == self.current_user_id and sender == target_id):
                messagebox.showinfo("Zaten Bağlantı Var", "Bu kullanıcı ile zaten bağlantınız var.")
                return

        conn = Connection(self.current_user_id, target_id)
        conn.send_request()
        messagebox.showinfo("Başarılı", "Bağlantı isteği gönderildi.")

    def follow_user(self):
        target_id = self.get_selected_user_id()
        if not target_id:
            messagebox.showwarning("Seçim yok", "Lütfen bir kullanıcı seçin.")
            return

        # Takip kontrolü
        existing = Follow.get_followings(self.current_user_id)
        if target_id in existing:
            messagebox.showinfo("Zaten Takip Ediliyor", "Bu kullanıcıyı zaten takip ediyorsunuz.")
            return

        follow = Follow(follower_id=self.current_user_id, followed_id=target_id, followed_type="user")
        follow.save()
        messagebox.showinfo("Başarılı", "Kullanıcı takip edildi.")

    def unfollow_user(self):
        target_id = self.get_selected_user_id()
        if not target_id:
            messagebox.showwarning("Seçim yok", "Lütfen bir kullanıcı seçin.")
            return

        Follow.unfollow(follower_id=self.current_user_id, followed_id=target_id, followed_type="user")
        messagebox.showinfo("Başarılı", "Takipten çıkıldı.")
