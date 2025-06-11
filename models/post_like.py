from db.db_config import get_connection

class PostLike:
    def __init__(self, user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id

    def save(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            # Aynı kullanıcı aynı postu tekrar beğenemesin
            cursor.execute("""
                INSERT IGNORE INTO PostLike (user_id, post_id)
                VALUES (%s, %s)
            """, (self.user_id, self.post_id))
            conn.commit()
        except Exception as e:
            print(f"[❌] Beğeni kaydedilemedi: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def count_likes(post_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM PostLike WHERE post_id = %s", (post_id,))
            return cursor.fetchone()[0]
        except Exception as e:
            print(f"[❌] Beğeni sayısı alınamadı: {e}")
            return 0
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
