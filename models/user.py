from db.db_config import get_connection

class User:
    def __init__(self,fullName,email,password_hash,role,created_at=None,id=None):
        self.id = id
        self.fullName = fullName
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.created_at_ = created_at

    def save(self):
        conn = get_connection()
        cursor = conn.cursor() #imleç
        query = ("INSERT INTO Users (fullName, email, password_hash, role, created_at) "
                 "VALUES (%s, %s, %s, %s, NOW())")
        values = [self.fullName, self.email, self.password_hash, self.role] #created_at NOW() ile oto ataniyor
        cursor.execute(query, values) #sorguyu execute ettik
        conn.commit() #degisiklikleri commit ettik
        self.id = cursor.lastrowid #auto_increment tanimladigimiz icin last_id + 1 yapiyoz
        conn.close()  #baglantiyi kapiyoruz

    @staticmethod
    def get_user_by_email_and_password(email, password_hash):
        print("🔍 Veritabanına bağlanılıyor...")
        conn = get_connection()
        if not conn:
            print("❌ Bağlantı başarısız.")
            return None

        try:
            cursor = conn.cursor()
            query = "SELECT id, fullName, email, role FROM Users WHERE email = %s AND password_hash = %s"
            cursor.execute(query, (email, password_hash))
            result = cursor.fetchone()
            if result:
                print("✅ Kullanıcı bulundu:", result)
                id, fullName, email, role = result
                return User(fullName=fullName, email=email, password_hash=password_hash, role=role, id=id)
            else:
                print("❌ Kullanıcı bulunamadı.")
                return None
        except Exception as e:
            print("⚠️ Sorgulama hatası:", e)
            return None
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
