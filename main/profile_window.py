import tkinter as tk
from tkinter import ttk, messagebox
from models.user_profile import UserProfile

class ProfileWindow(tk.Toplevel):
    def __init__(self, user_id):
        super().__init__()
        self.title("🧑 My Profile")
        self.geometry("500x650")
        self.resizable(False, False)
        self.configure(bg="#e6f2f3")  # Hafif mavi ton

        self.user_id = user_id
        self.profile = UserProfile.get_by_user_id(self.user_id)

        # Başlık
        tk.Label(self, text="User Profile", font=("Segoe UI", 20, "bold"), fg="#0D4D56", bg="#e6f2f3").pack(pady=20)

        # Form alanı kapsayıcı
        form_frame = tk.Frame(self, bg="#e6f2f3")
        form_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Form verileri
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
            tk.Label(form_frame, text=label, font=("Segoe UI", 11, "bold"), bg="#e6f2f3", anchor="w").pack(anchor="w", pady=(10, 0))
            if label == "Gender":
                gender_combo = ttk.Combobox(form_frame, textvariable=var, values=["M", "F"])
                gender_combo.pack(fill="x")
            else:
                tk.Entry(form_frame, textvariable=var, font=("Segoe UI", 11)).pack(fill="x")

        # Kaydet butonu
        ttk.Button(self, text="💾 Save Profile", command=self.save_profile).pack(pady=20)

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
