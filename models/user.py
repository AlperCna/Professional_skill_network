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