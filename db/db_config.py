from mysql.connector import Error
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Emr314Ir159+",
        database="professional_skill_network"
    )

def test_db():
    try:
        print("🔌 Bağlantı deneniyor...")
        conn = get_connection()
        print("✅ Bağlantı başarılı mı?:", conn.is_connected())
        conn.close()
    except Exception as e:
        print("⛔ Hata:", e)


if __name__ == "__main__":
    test_db()
