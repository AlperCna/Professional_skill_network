from db.db_config import get_connection
from models.user import User

class Comment:
    def __init__(self, post_id, user_id, text, created_at=None):
        self.post_id = post_id
        self.user_id = user_id
        self.text = text
        self.created_at = created_at

    def save(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Comment (post_id, user_id, text)
                VALUES (%s, %s, %s)
            """, (self.post_id, self.user_id, self.text))
            conn.commit()
        except Exception as e:
            print(f"[❌] Yorum kaydedilemedi: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def get_comments(post_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = """
                SELECT u.fullName, c.text, c.created_at
                FROM Comment c
                JOIN users u ON c.user_id = u.id
                WHERE c.post_id = %s
                ORDER BY c.created_at ASC
            """
            cursor.execute(query, (post_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"[❌] Yorumlar alınamadı: {e}")
            return []
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
