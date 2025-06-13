from db.db_config import get_connection

class Experience:
    def __init__(self, user_id, position, company, start_date, end_date, id=None):
        self.id = id
        self.user_id = user_id
        self.position = position
        self.company = company
        self.start_date = start_date
        self.end_date = end_date

    def save(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO Experience (user_id, position, company, start_date, end_date)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (self.user_id, self.position, self.company, self.start_date, self.end_date))
            conn.commit()
        except Exception as e:
            print("❌ Experience kaydedilemedi:", e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def get_by_user_id(user_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, position, company, start_date, end_date FROM Experience WHERE user_id = %s", (user_id,))
            return cursor.fetchall()
        except Exception as e:
            print("❌ Experience verileri alınamadı:", e)
            return []
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def delete(experience_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Experience WHERE id = %s", (experience_id,))
            conn.commit()
        except Exception as e:
            print("❌ Experience silinemedi:", e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
