import tkinter as tk
from tkinter import ttk
from models.connection import Connection
from models.user import User
from main.endorse_skill_window import EndorseSkillWindow  # Endorse penceresi import edilir

class ConnectionListWindow(tk.Toplevel):
    def __init__(self, current_user):
        super().__init__()
        self.title("🤝 Connections")
        self.geometry("600x500")
        self.configure(bg="white")
        self.current_user = current_user  # Bu artık bir User objesi

        tk.Label(self, text="Your Connections", font=("Segoe UI", 16, "bold"), bg="white").pack(pady=10)

        # Scrollable canvas-frame yapısı
        canvas = tk.Canvas(self, bg="white", borderwidth=0)
        frame = tk.Frame(canvas, bg="white")
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=frame, anchor="nw")
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self.scrollable_frame = frame
        self.load_connections()

    def load_connections(self):
        connections = Connection.get_connections(self.current_user.id)
        for u1, u2, _ in connections:
            other_id = u2 if u1 == self.current_user.id else u1
            user = User.get_user_by_id(other_id)
            if user:
                self.add_connection_row(user)

    def add_connection_row(self, user):
        row = tk.Frame(self.scrollable_frame, bg="white")
        row.pack(fill="x", padx=10, pady=5)

        # Kullanıcı bilgisi
        tk.Label(row, text=f"{user.fullName} ({user.email})", font=("Segoe UI", 12), bg="white").pack(side="left", padx=10)

        # Endorse butonu
        ttk.Button(row, text="👍 Endorse Skill", command=lambda u=user: EndorseSkillWindow(self.current_user, u)).pack(side="right", padx=10)
