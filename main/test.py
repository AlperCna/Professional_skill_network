from PyQt5.QtWidgets import QApplication
from login_window import LoginWindow  # <-- Bu satır
from models.user import User

"""app = QApplication([])
window = LoginWindow()               # <-- Bu satır
window.show()
app.exec_()"""

def test_login():
    email = "alpar@gmail.com"
    password_hash = "123123"

    print(f"🔍 Giriş deneniyor: {email} / {password_hash}")
    user = User.get_user_by_email_and_password(email, password_hash)

    if user:
        print(f"✅ Kullanıcı girişi başarılı. Hoş geldin, {user.name}")
    else:
        print("❌ Giriş başarısız. Kullanıcı bulunamadı.")

if __name__ == "__main__":
    test_login()
