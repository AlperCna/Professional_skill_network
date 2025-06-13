from db.db_config import get_connection

class Education:
    def __init__(self, user_id, school, degree, start_year, end_year, id=None):
        self.id = id
        self.user_id = user_id
        self.school = school
        self.degree = degree
        self.start_year = start_year
        self.end_year = end_year

    def save(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO Education (user_id, school, degree, start_year, end_year)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (self.user_id, self.school, self.degree, self.start_year, self.end_year))
            conn.commit()
        except Exception as e:
            print("❌ Education kaydedilemedi:", e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def get_by_user_id(user_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, school, degree, start_year, end_year FROM Education WHERE user_id = %s", (user_id,))
            return cursor.fetchall()
        except Exception as e:
            print("❌ Education verileri alınamadı:", e)
            return []
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def delete(education_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Education WHERE id = %s", (education_id,))
            conn.commit()
        except Exception as e:
            print("❌ Education silinemedi:", e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
