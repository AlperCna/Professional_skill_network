from db.db_config import get_connection
from datetime import datetime

class Follow:
    def __init__(self, follower_id, followed_id, followed_type="user", followed_at=None):
        self.follower_id = follower_id
        self.followed_id = followed_id
        self.followed_type = followed_type
        self.followed_at = followed_at or datetime.now()

    def save(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO follow (follower_id, followed_id, followed_type, followed_at)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE followed_at = VALUES(followed_at)
            """
            cursor.execute(query, (self.follower_id, self.followed_id, self.followed_type, self.followed_at))
            conn.commit()
        except Exception as e:
            print("⚠️ Takip etme hatası:", e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def unfollow(follower_id, followed_id, followed_type="user"):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = """
                DELETE FROM follow
                WHERE follower_id = %s AND followed_id = %s AND followed_type = %s
            """
            cursor.execute(query, (follower_id, followed_id, followed_type))
            conn.commit()
        except Exception as e:
            print("⚠️ Takipten çıkarılamadı:", e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def get_followings(follower_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT followed_id FROM follow WHERE follower_id = %s AND followed_type = 'user'",
                           (follower_id,))
            return [row[0] for row in cursor.fetchall()]  # Bu doğru
        except Exception as e:
            print("⚠️ Takip edilenler alınamadı:", e)
            return []
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def get_followers(user_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = "SELECT follower_id FROM follow WHERE followed_id = %s AND followed_type = 'user'"
            cursor.execute(query, (user_id,))
            return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print("⚠️ Takipçiler alınamadı:", e)
            return []
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
