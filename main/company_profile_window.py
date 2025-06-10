import tkinter as tk
from tkinter import ttk, messagebox
from models.company_profile import CompanyProfile


class CompanyProfileWindow(tk.Toplevel):
    def __init__(self, company_id):
        super().__init__()
        self.title("🏢 Company Profile")
        self.geometry("500x600")
        self.configure(bg="#f0f8ff")
        self.resizable(False, False)
        self.company_id = company_id

        # Profil nesnesi
        self.profile = CompanyProfile.get_by_company_id(company_id)

        # Alanlar
        self.fields = {
            "Company Name": tk.StringVar(value=self.profile.company_name if self.profile else ""),
            "Description": tk.StringVar(value=self.profile.description if self.profile else ""),
            "Website": tk.StringVar(value=self.profile.website if self.profile else ""),
            "Industry": tk.StringVar(value=self.profile.industry if self.profile else ""),
            "Size": tk.StringVar(value=self.profile.size if self.profile else ""),
            "Location": tk.StringVar(value=self.profile.location if self.profile else "")
        }

        tk.Label(self, text="Company Profile", font=("Segoe UI", 20, "bold"), bg="#f0f8ff", fg="#0D4D56").pack(pady=20)

        form_frame = tk.Frame(self, bg="#f0f8ff")
        form_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Form alanları
        for label, var in self.fields.items():
            tk.Label(form_frame, text=label, font=("Segoe UI", 11, "bold"), bg="#f0f8ff", anchor="w").pack(anchor="w", pady=(10, 0))
            if label == "Size":
                ttk.Combobox(form_frame, textvariable=var,
                             values=["1-10", "11-50", "51-200", "200+"],
                             state="readonly").pack(fill="x")
            else:
                ttk.Entry(form_frame, textvariable=var).pack(fill="x")

        # Kaydet butonu
        ttk.Button(self, text="💾 Save", command=self.save_profile).pack(pady=20)

    def save_profile(self):
        profile = CompanyProfile(
            company_id=self.company_id,
            company_name=self.fields["Company Name"].get(),
            description=self.fields["Description"].get(),
            website=self.fields["Website"].get(),
            industry=self.fields["Industry"].get(),
            size=self.fields["Size"].get(),
            location=self.fields["Location"].get()
        )

        try:
            profile.save()
            messagebox.showinfo("Success", "✅ Company profile saved successfully!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"❌ Failed to save:\n{e}")
