from db.db_config import get_connection
from datetime import datetime

class Application:
    def __init__(self, user_id, job_id, status="pending", applied_at=None, id=None):
        self.id = id
        self.user_id = user_id
        self.job_id = job_id
        self.status = status
        self.applied_at = applied_at or datetime.now()

    def save(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO Application (user_id, job_id, status)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (self.user_id, self.job_id, self.status))
            conn.commit()
            self.id = cursor.lastrowid
        except Exception as e:
            print("⚠️ Başvuru kaydedilemedi:", e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def has_applied(user_id, job_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = "SELECT id FROM Application WHERE user_id = %s AND job_id = %s"
            cursor.execute(query, (user_id, job_id))
            return cursor.fetchone() is not None
        except Exception as e:
            print("⚠️ Başvuru sorgulama hatası:", e)
            return False
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def get_applications_by_user(user_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = """
                SELECT a.id, a.job_id, j.title, a.status, a.applied_at
                FROM Application a
                JOIN JobPost j ON a.job_id = j.id
                WHERE a.user_id = %s
                ORDER BY a.applied_at DESC
            """
            cursor.execute(query, (user_id,))
            return cursor.fetchall()
        except Exception as e:
            print("⚠️ Kullanıcının başvuruları alınamadı:", e)
            return []
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
