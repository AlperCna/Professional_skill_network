import tkinter as tk
from tkinter import ttk, messagebox
from models.skill import Skill
from models.user_skill import UserSkill
from models.skill_endorsement import SkillEndorsement

class SkillWindow(tk.Toplevel):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.title("🧠 Manage Your Skills")
        self.geometry("600x500")
        self.configure(bg="#e6f2f3")

        self.skills = Skill.get_all()
        self.levels = ["beginner", "intermediate", "advanced"]

        # Başlık
        tk.Label(self, text="Add a Skill", font=("Segoe UI", 16, "bold"), bg="#e6f2f3", fg="#0D4D56").pack(pady=10)

        # Skill seçimi
        self.selected_skill = tk.StringVar()
        skill_names = [s.skill_name for s in self.skills]
        self.combo_skill = ttk.Combobox(self, textvariable=self.selected_skill, values=skill_names, state="readonly")
        self.combo_skill.pack(pady=5)

        # Level seçimi
        self.selected_level = tk.StringVar()
        self.combo_level = ttk.Combobox(self, textvariable=self.selected_level, values=self.levels, state="readonly")
        self.combo_level.pack(pady=5)

        # Ekle butonu
        ttk.Button(self, text="➕ Add Skill", command=self.add_skill).pack(pady=10)

        # Yetenek Listesi
        tk.Label(self, text="Your Skills", font=("Segoe UI", 14, "bold"), bg="#e6f2f3", fg="#0D4D56").pack(pady=10)
        self.tree = ttk.Treeview(self, columns=("Skill", "Level", "Endorsed"), show="headings", height=8)
        self.tree.heading("Skill", text="Skill")
        self.tree.heading("Level", text="Level")
        self.tree.heading("Endorsed", text="Endorsements")
        self.tree.pack(pady=10)

        # Sil butonu
        ttk.Button(self, text="❌ Delete Selected", command=self.delete_selected).pack(pady=5)

        self.refresh_skill_list()

    def get_skill_id_by_name(self, name):
        for s in self.skills:
            if s.skill_name == name:
                return s.id
        return None

    def add_skill(self):
        skill_name = self.selected_skill.get()
        level = self.selected_level.get()

        if not skill_name or not level:
            messagebox.showerror("Error", "Please select a skill and level.")
            return

        skill_id = self.get_skill_id_by_name(skill_name)
        if not skill_id:
            messagebox.showerror("Error", "Skill not found.")
            return

        us = UserSkill(user_id=self.user.id, skill_id=skill_id, level=level)
        us.save()
        messagebox.showinfo("Success", f"✅ Skill '{skill_name}' added.")
        self.refresh_skill_list()

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        skill_name = values[0]
        skill_id = self.get_skill_id_by_name(skill_name)

        if skill_id:
            UserSkill.delete(self.user.id, skill_id)
            messagebox.showinfo("Deleted", f"❌ Skill '{skill_name}' removed.")
            self.refresh_skill_list()

    def refresh_skill_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        skills = UserSkill.get_skills_by_user(self.user.id)
        for sid, name, level, count in skills:
            self.tree.insert("", "end", values=(name, level, count))
