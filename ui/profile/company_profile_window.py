import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from models.company_profile import CompanyProfile


class CompanyProfileWindow(tk.Toplevel):
    def __init__(self, company_id, readonly=False):
        super().__init__()
        self.title("🏢 Company Profile")
        self.geometry("500x650")
        self.configure(bg="#f0f8ff")
        self.resizable(False, False)
        self.company_id = company_id
        self.readonly = readonly

        self.profile = CompanyProfile.get_by_company_id(company_id)
        self.profile_picture_path = self.profile.profile_picture_path if self.profile else None

        # Görsel Alanı
        self.image_label = tk.Label(self, bg="#f0f8ff")
        self.image_label.pack(pady=(20, 5))
        self.load_profile_picture()

        if not self.readonly:
            ttk.Button(self, text="📁 Upload Logo", command=self.upload_picture).pack(pady=(0, 10))

        # Başlık
        tk.Label(self, text="Company Profile", font=("Segoe UI", 20, "bold"),
                 bg="#f0f8ff", fg="#0D4D56").pack(pady=5)

        form_frame = tk.Frame(self, bg="#f0f8ff")
        form_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.fields = {
            "Company Name": tk.StringVar(value=self.profile.company_name if self.profile else ""),
            "Description": tk.StringVar(value=self.profile.description if self.profile else ""),
            "Website": tk.StringVar(value=self.profile.website if self.profile else ""),
            "Industry": tk.StringVar(value=self.profile.industry if self.profile else ""),
            "Size": tk.StringVar(value=self.profile.size if self.profile else ""),
            "Location": tk.StringVar(value=self.profile.location if self.profile else "")
        }

        self.inputs = {}
        for label, var in self.fields.items():
            tk.Label(form_frame, text=label, font=("Segoe UI", 11, "bold"),
                     bg="#f0f8ff", anchor="w").pack(anchor="w", pady=(10, 0))

            if label == "Size":
                state = "disabled" if self.readonly else "readonly"
                combo = ttk.Combobox(form_frame, textvariable=var,
                                     values=["1-10", "11-50", "51-200", "200+"],
                                     state=state if self.readonly else "normal")
                combo.pack(fill="x")
                self.inputs[label] = combo
            else:
                entry = ttk.Entry(form_frame, textvariable=var,
                                  state="readonly" if self.readonly else "normal")
                entry.pack(fill="x")
                self.inputs[label] = entry

        if not self.readonly:
            ttk.Button(self, text="💾 Save", command=self.save_profile).pack(pady=20)

    def load_profile_picture(self):
        if self.profile_picture_path and os.path.exists(self.profile_picture_path):
            image = Image.open(self.profile_picture_path)
            image = image.resize((120, 120))
            self.photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.photo)
            self.image_label.image = self.photo
        else:
            self.image_label.config(text="No Logo", width=15, height=7, bg="#ccc", font=("Segoe UI", 10, "italic"))

    def upload_picture(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if path:
            self.profile_picture_path = path
            self.load_profile_picture()

    def save_profile(self):
        profile = CompanyProfile(
            company_id=self.company_id,
            company_name=self.fields["Company Name"].get(),
            description=self.fields["Description"].get(),
            website=self.fields["Website"].get(),
            industry=self.fields["Industry"].get(),
            size=self.fields["Size"].get(),
            location=self.fields["Location"].get(),
            profile_picture_path=self.profile_picture_path
        )

        try:
            profile.save()
            messagebox.showinfo("Success", "✅ Company main1 saved successfully!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"❌ Failed to save:\n{e}")
