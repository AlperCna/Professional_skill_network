import tkinter as tk
from tkinter import ttk, messagebox
from models.connection import Connection
from models.user import User
from db.db_config import get_connection


class ConnectionRequestsWindow(tk.Toplevel):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.title("Gelen Bağlantı İstekleri")
        self.geometry("600x500")
        self.configure(bg="white")
        self.user_id = user_id

        self.tree = ttk.Treeview(self, columns=("ID", "Ad", "Email", "Durum"), show="headings", height=15)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Ad", text="Ad")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Durum", text="Durum")
        self.tree.pack(padx=20, pady=20, fill="both", expand=True)

        btn_frame = tk.Frame(self, bg="white")
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="✅ Kabul Et", command=self.accept_request).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="❌ Reddet", command=self.reject_request).grid(row=0, column=1, padx=10)

        self.load_requests()

    def load_requests(self):
        self.tree.delete(*self.tree.get_children())
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = """
                SELECT u.id, u.fullName, u.email, c.status
                FROM connection c
                JOIN users u ON c.user1_id = u.id
                WHERE c.user2_id = %s AND c.status = 'pending'
            """
            cursor.execute(query, (self.user_id,))
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Hata", f"İstekler yüklenemedi: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def get_selected_sender_id(self):
        selected = self.tree.selection()
        if not selected:
            return None
        return int(self.tree.item(selected[0])["values"][0])

    def accept_request(self):
        sender_id = self.get_selected_sender_id()
        if not sender_id:
            messagebox.showwarning("Uyarı", "Lütfen bir istek seçin.")
            return

        Connection.respond_to_request(sender_id, self.user_id, "accepted")
        messagebox.showinfo("Başarılı", "İstek kabul edildi.")
        self.load_requests()

    def reject_request(self):
        sender_id = self.get_selected_sender_id()
        if not sender_id:
            messagebox.showwarning("Uyarı", "Lütfen bir istek seçin.")
            return

        Connection.respond_to_request(sender_id, self.user_id, "rejected")
        messagebox.showinfo("Başarılı", "İstek reddedildi.")
        self.load_requests()
