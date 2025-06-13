import tkinter as tk
from tkinter import ttk, messagebox
from models.user import User
from models.user_profile import UserProfile
from models.experience import Experience
from models.education import Education
from tkcalendar import DateEntry
from datetime import datetime


class ProfileWindow(tk.Toplevel):
    def __init__(self, user_id, readonly=False):
        super().__init__()
        self.title("👤 User Profile")
        self.geometry("750x650")
        self.configure(bg="#f1f3f5")
        self.user_id = user_id
        self.readonly = readonly

        self.user = User.get_user_by_id(user_id)
        self.profile = UserProfile.get_by_user_id(user_id)

        # ÜST BİLGİ BÖLÜMÜ
        header = tk.Frame(self, bg="#0D4D56")
        header.pack(fill="x")

        tk.Label(header, text=self.user.fullName, font=("Segoe UI", 18, "bold"),
                 bg="#0D4D56", fg="white").pack(pady=(15, 0))

        if self.profile and self.profile.headline:
            tk.Label(header, text=self.profile.headline, font=("Segoe UI", 12),
                     bg="#0D4D56", fg="#d1e7dd").pack(pady=(5, 10))

        if self.profile and self.profile.location:
            tk.Label(header, text=self.profile.location, font=("Segoe UI", 10),
                     bg="#0D4D56", fg="#ced4da").pack()

        # SEKMELER
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=20, pady=15)

        self.init_info_tab(notebook)
        self.init_experience_tab(notebook)
        self.init_education_tab(notebook)

    def init_info_tab(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="🧾 Info")

        form_frame = tk.Frame(tab, bg="white")
        form_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.fields = {
            "Headline": tk.StringVar(value=self.profile.headline if self.profile else ""),
            "Bio": tk.StringVar(value=self.profile.bio if self.profile else ""),
            "Location": tk.StringVar(value=self.profile.location if self.profile else ""),
            "Phone": tk.StringVar(value=self.profile.phone if self.profile else ""),
            "Birthdate": tk.StringVar(value=self.profile.birthdate if self.profile else ""),
            "Gender": tk.StringVar(value=self.profile.gender if self.profile else ""),
            "Website": tk.StringVar(value=self.profile.website if self.profile else "")
        }

        for label, var in self.fields.items():
            tk.Label(form_frame, text=label, font=("Segoe UI", 10, "bold"), bg="white").pack(anchor="w", pady=(10, 0))
            if label == "Gender":
                gender_combo = ttk.Combobox(form_frame, textvariable=var, values=["M", "F"],
                                            state="readonly" if self.readonly else "normal")
                gender_combo.pack(fill="x")
            else:
                state = "readonly" if self.readonly else "normal"
                tk.Entry(form_frame, textvariable=var, state=state).pack(fill="x")

        if not self.readonly:
            ttk.Button(tab, text="💾 Save Profile", command=self.save_profile).pack(pady=10)

    def init_experience_tab(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="💼 Experience")

        if not self.readonly:
            top_frame = tk.Frame(tab)
            top_frame.pack(fill="x", padx=10, pady=10)

            tk.Label(top_frame, text="Position").grid(row=0, column=0, sticky="w", padx=5, pady=2)
            tk.Label(top_frame, text="Company").grid(row=1, column=0, sticky="w", padx=5, pady=2)
            tk.Label(top_frame, text="Start Date").grid(row=0, column=2, sticky="w", padx=5, pady=2)
            tk.Label(top_frame, text="End Date").grid(row=1, column=2, sticky="w", padx=5, pady=2)

            self.exp_position = tk.StringVar()
            self.exp_company = tk.StringVar()
            self.exp_start = tk.StringVar()
            self.exp_end = tk.StringVar()

            tk.Entry(top_frame, textvariable=self.exp_position).grid(row=0, column=1)
            tk.Entry(top_frame, textvariable=self.exp_company).grid(row=1, column=1)
            DateEntry(top_frame, textvariable=self.exp_start, date_pattern="yyyy-mm-dd").grid(row=0, column=3)
            DateEntry(top_frame, textvariable=self.exp_end, date_pattern="yyyy-mm-dd").grid(row=1, column=3)

            ttk.Button(top_frame, text="➕ Add Experience", command=self.add_experience).grid(row=2, column=0, columnspan=4, pady=10)

        self.exp_tree = ttk.Treeview(tab, columns=("Position", "Company", "Start", "End"), show="headings")
        for col in self.exp_tree["columns"]:
            self.exp_tree.heading(col, text=col)
            self.exp_tree.column(col, width=150)
        self.exp_tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.load_experiences()

    def add_experience(self):
        exp = Experience(
            user_id=self.user_id,
            position=self.exp_position.get(),
            company=self.exp_company.get(),
            start_date=self.exp_start.get(),
            end_date=self.exp_end.get()
        )
        exp.save()
        self.load_experiences()
        self.exp_position.set("")
        self.exp_company.set("")
        self.exp_start.set("")
        self.exp_end.set("")
        messagebox.showinfo("Success", "✅ Experience added successfully!")

    def load_experiences(self):
        for i in self.exp_tree.get_children():
            self.exp_tree.delete(i)
        for exp in Experience.get_by_user_id(self.user_id):
            self.exp_tree.insert("", "end", values=(exp[1], exp[2], exp[3], exp[4]))

    def init_education_tab(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="🎓 Education")

        if not self.readonly:
            top_frame = tk.Frame(tab)
            top_frame.pack(fill="x", padx=10, pady=10)

            tk.Label(top_frame, text="School").grid(row=0, column=0, sticky="w", padx=5, pady=2)
            tk.Label(top_frame, text="Degree").grid(row=1, column=0, sticky="w", padx=5, pady=2)
            tk.Label(top_frame, text="Start Year").grid(row=0, column=2, sticky="w", padx=5, pady=2)
            tk.Label(top_frame, text="End Year").grid(row=1, column=2, sticky="w", padx=5, pady=2)

            self.edu_school = tk.StringVar()
            self.edu_degree = tk.StringVar()
            self.edu_start = tk.StringVar()
            self.edu_end = tk.StringVar()

            tk.Entry(top_frame, textvariable=self.edu_school).grid(row=0, column=1)
            tk.Entry(top_frame, textvariable=self.edu_degree).grid(row=1, column=1)
            current_year = datetime.now().year
            year_options = [str(y) for y in range(1980, current_year + 1)]

            ttk.Combobox(top_frame, textvariable=self.edu_start, values=year_options, state="readonly").grid(row=0,
                                                                                                             column=3)
            ttk.Combobox(top_frame, textvariable=self.edu_end, values=year_options, state="readonly").grid(row=1,
                                                                                                           column=3)
            ttk.Button(top_frame, text="➕ Add Education", command=self.add_education).grid(row=2, column=0, columnspan=4, pady=10)

        self.edu_tree = ttk.Treeview(tab, columns=("School", "Degree", "Start", "End"), show="headings")
        for col in self.edu_tree["columns"]:
            self.edu_tree.heading(col, text=col)
            self.edu_tree.column(col, width=150)
        self.edu_tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.load_educations()

    def add_education(self):
        edu = Education(
            user_id=self.user_id,
            school=self.edu_school.get(),
            degree=self.edu_degree.get(),
            start_year=self.edu_start.get(),
            end_year=self.edu_end.get()
        )
        edu.save()
        self.load_educations()
        self.edu_school.set("")
        self.edu_degree.set("")
        self.edu_start.set("")
        self.edu_end.set("")
        messagebox.showinfo("Success", "✅ Education added successfully!")

    def load_educations(self):
        for i in self.edu_tree.get_children():
            self.edu_tree.delete(i)
        for edu in Education.get_by_user_id(self.user_id):
            self.edu_tree.insert("", "end", values=(edu[1], edu[2], edu[3], edu[4]))

    def save_profile(self):
        profile = UserProfile(
            user_id=self.user_id,
            headline=self.fields["Headline"].get(),
            bio=self.fields["Bio"].get(),
            location=self.fields["Location"].get(),
            phone=self.fields["Phone"].get(),
            birthdate=self.fields["Birthdate"].get(),
            gender=self.fields["Gender"].get(),
            website=self.fields["Website"].get(),
            verified=False
        )
        profile.save()
        messagebox.showinfo("Success", "✅ Profile saved successfully!")
