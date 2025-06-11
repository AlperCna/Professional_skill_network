import tkinter as tk
from tkinter import ttk, messagebox
from models.message import Message
from models.user import User
from db.db_config import get_connection


class ChatWindow(tk.Toplevel):
    def __init__(self, current_user):
        super().__init__()
        self.title("💬 Messages")
        self.geometry("850x550")
        self.configure(bg="#e9ecef")
        self.current_user = current_user
        self.selected_user_id = None

        self.create_widgets()
        self.load_users()

    def create_widgets(self):
        # Ana çerçeve bölmeleri
        main_frame = tk.Frame(self, bg="#e9ecef")
        main_frame.pack(fill="both", expand=True)

        # Sol panel (kullanıcı listesi)
        left_frame = tk.Frame(main_frame, width=250, bg="#f8f9fa", bd=2, relief="groove")
        left_frame.pack(side="left", fill="y")

        tk.Label(left_frame, text="📇 Users", bg="#f8f9fa", font=("Segoe UI", 12, "bold")).pack(pady=10)

        self.user_listbox = tk.Listbox(left_frame, font=("Segoe UI", 10), bg="white", bd=0, highlightthickness=0)
        self.user_listbox.pack(fill="y", expand=True, padx=10, pady=5)
        self.user_listbox.bind("<<ListboxSelect>>", self.load_conversation)

        # Sağ panel (mesaj + giriş alanı)
        right_frame = tk.Frame(main_frame, bg="#ffffff", bd=2, relief="groove")
        right_frame.pack(side="right", fill="both", expand=True)

        self.chat_text = tk.Text(right_frame, state="disabled", wrap="word",
                                 font=("Segoe UI", 10), bg="#ffffff", relief="flat")
        self.chat_text.pack(padx=10, pady=10, fill="both", expand=True)

        bottom_frame = tk.Frame(right_frame, bg="#ffffff")
        bottom_frame.pack(fill="x", padx=10, pady=10)

        self.entry = tk.Entry(bottom_frame, font=("Segoe UI", 10), bg="#f1f3f5", relief="flat")
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=6)

        send_btn = ttk.Button(bottom_frame, text="📨 Send", command=self.send_message)
        send_btn.pack(side="right")

    def load_users(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, fullName FROM users WHERE role = 'individual' AND id != %s",
                           (self.current_user.id,))
            self.user_map = {}
            self.user_listbox.delete(0, "end")
            for row in cursor.fetchall():
                self.user_map[row[1]] = row[0]
                self.user_listbox.insert("end", row[1])
        except Exception as e:
            messagebox.showerror("Hata", f"Kullanıcılar yüklenemedi: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def load_conversation(self, event):
        selection = self.user_listbox.curselection()
        if not selection:
            return
        selected_name = self.user_listbox.get(selection[0])
        self.selected_user_id = self.user_map[selected_name]

        messages = Message.get_conversation(self.current_user.id, self.selected_user_id)

        self.chat_text.config(state="normal")
        self.chat_text.delete("1.0", "end")

        for sender_id, receiver_id, text, sent_at in messages:
            prefix = "Me" if sender_id == self.current_user.id else selected_name
            time_str = sent_at.strftime("%H:%M")
            self.chat_text.insert("end", f"{prefix} [{time_str}]: {text}\n\n")

        self.chat_text.config(state="disabled")
        self.chat_text.see("end")

    def send_message(self):
        text = self.entry.get().strip()
        if not text:
            return
        if not self.selected_user_id:
            messagebox.showwarning("Uyarı", "Lütfen bir kullanıcı seçin.")
            return

        msg = Message(sender_id=self.current_user.id, receiver_id=self.selected_user_id, text=text)
        msg.save()
        self.entry.delete(0, "end")
        self.load_conversation(None)
