import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from models.user_skill import UserSkill
from models.application import Application
import shutil
import os


class ApplicationFormWindow(tk.Toplevel):
    def __init__(self, user, job_id):
        super().__init__()
        self.title("📄 Job Application Form")
        self.geometry("750x500")
        self.configure(bg="white")
        self.user = user
        self.job_id = job_id
        self.selected_skills = []

        # Frame yapısı
        main_frame = tk.Frame(self, bg="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Başlık
        tk.Label(main_frame, text="Select Your Skills", font=("Segoe UI", 14, "bold"), bg="white").grid(row=0, column=0, sticky="w")

        # Skill listesi (sol)
        self.skill_listbox = tk.Listbox(main_frame, selectmode="multiple", height=10, width=30)
        self.skill_listbox.grid(row=1, column=0, padx=10, pady=10)
        self.load_skills()

        # Seçilen skiller (sağ)
        tk.Label(main_frame, text="Selected Skills", font=("Segoe UI", 14, "bold"), bg="white").grid(row=0, column=1, sticky="w")
        self.selected_listbox = tk.Listbox(main_frame, height=10, width=30)
        self.selected_listbox.grid(row=1, column=1, padx=10, pady=10)

        # Skill ekle/kaldır
        btn_frame = tk.Frame(main_frame, bg="white")
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="➕ Add Selected", command=self.add_selected_skills).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="❌ Remove Selected", command=self.remove_selected_skills).pack(side="left", padx=5)

        # CV yükleme
        tk.Label(main_frame, text="Upload CV:", font=("Segoe UI", 12), bg="white").grid(row=3, column=0, sticky="w")
        self.cv_path_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.cv_path_var, state="readonly", width=50).grid(row=3, column=1, pady=10)
        ttk.Button(main_frame, text="📁 Browse", command=self.browse_cv).grid(row=3, column=2, padx=5)

        # Gönder butonu
        ttk.Button(main_frame, text="📩 Submit Application", command=self.submit_application).grid(row=4, column=0, columnspan=3, pady=20)

    def load_skills(self):
        skills = UserSkill.get_skills_by_user(self.user.id)
        for sid, name, level, count in skills:
            self.skill_listbox.insert("end", f"{name} ({level})")

    def add_selected_skills(self):
        selected = self.skill_listbox.curselection()
        for i in selected:
            value = self.skill_listbox.get(i)
            if value not in self.selected_skills:
                self.selected_skills.append(value)
                self.selected_listbox.insert("end", value)

    def remove_selected_skills(self):
        selected = self.selected_listbox.curselection()
        for i in reversed(selected):
            self.selected_skills.remove(self.selected_listbox.get(i))
            self.selected_listbox.delete(i)

    def browse_cv(self):
        filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
        if filepath:
            self.cv_path_var.set(filepath)

    def submit_application(self):
        if not self.selected_skills:
            messagebox.showerror("Error", "Please select at least one skill.")
            return
        if not self.cv_path_var.get():
            messagebox.showerror("Error", "Please upload your CV.")
            return

        # CV dosyasını 'uploads' klasörüne kopyalayalım
        try:
            os.makedirs("uploads", exist_ok=True)
            filename = f"user_{self.user.id}_job_{self.job_id}.pdf"
            dest = os.path.join("uploads", filename)
            shutil.copyfile(self.cv_path_var.get(), dest)
        except Exception as e:
            messagebox.showerror("Error", f"CV upload failed:\n{e}")
            return

        # Basit başvuru kaydı (detaylı skill + cv dosyası DB'ye ileride eklenebilir)
        app = Application(user_id=self.user.id, job_id=self.job_id)
        app.save()

        messagebox.showinfo("Success", "✅ Application submitted successfully.")
        self.destroy()
