import tkinter as tk
from tkinter import ttk, messagebox
from models.user_skill import UserSkill
from models.skill_endorsement import SkillEndorsement
from models.connection import Connection
from models.skill import Skill

class EndorseSkillWindow(tk.Toplevel):
    def __init__(self, current_user, target_user):
        super().__init__()
        self.title("👍 Endorse Skills")
        self.geometry("450x400")
        self.configure(bg="white")
        self.current_user = current_user
        self.target_user = target_user

        # Bağlantı kontrolü
        if not Connection.exists_between(current_user.id, target_user.id):
            messagebox.showerror("Access Denied", "You must be connected to endorse skills.")
            self.destroy()
            return

        tk.Label(self, text=f"Endorse {target_user.fullName}'s Skills", font=("Segoe UI", 14, "bold"), bg="white").pack(pady=10)

        self.skill_listbox = tk.Listbox(self, height=12, width=40)
        self.skill_listbox.pack(pady=10)

        self.load_skills()

        ttk.Button(self, text="✅ Endorse Selected", command=self.endorse_skill).pack(pady=10)

    def load_skills(self):
        skills = UserSkill.get_skills_by_user(self.target_user.id)
        for sid, name, level, count in skills:
            self.skill_listbox.insert("end", f"{name} ({level})")

    def endorse_skill(self):
        selection = self.skill_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a skill to endorse.")
            return

        skill_text = self.skill_listbox.get(selection[0])
        skill_name = skill_text.split(" (")[0]
        skill_id = Skill.get_id_by_name(skill_name)

        if SkillEndorsement.has_already_endorsed(self.current_user.id, self.target_user.id, skill_id):
            messagebox.showinfo("Info", "You already endorsed this skill.")
            return

        endorsement = SkillEndorsement(
            endorser_id=self.current_user.id,
            endorsed_user_id=self.target_user.id,
            skill_id=skill_id
        )
        endorsement.save()
        messagebox.showinfo("Success", "✅ Skill endorsed successfully.")
        self.destroy()
