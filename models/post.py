from db.db_config import get_connection

class Post:
    def __init__(self, user_id, content, id=None, created_at=None):
        self.id = id
        self.user_id = user_id
        self.content = content
        self.created_at = created_at

    def save(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = "INSERT INTO Post (user_id, content) VALUES (%s, %s)"
            cursor.execute(query, (self.user_id, self.content))
            conn.commit()
        except Exception as e:
            print(f"[❌] Post kaydedilemedi: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def get_all_for_feed(user_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = """
                SELECT p.id, u.fullName, p.content, p.created_at
                FROM Post p
                JOIN users u ON p.user_id = u.id
                WHERE p.user_id = %s
                   OR p.user_id IN (
                        SELECT CASE
                            WHEN c.user1_id = %s THEN c.user2_id
                            WHEN c.user2_id = %s THEN c.user1_id
                        END
                        FROM connection c
                        WHERE (c.user1_id = %s OR c.user2_id = %s)
                          AND c.status = 'accepted'
                   )
                   OR p.user_id IN (
                        SELECT followed_id FROM follow WHERE follower_id = %s
                   )
                ORDER BY p.created_at DESC
            """
            cursor.execute(query, (user_id, user_id, user_id, user_id, user_id, user_id))
            return cursor.fetchall()
        except Exception as e:
            print(f"[❌] Feed alınamadı: {e}")
            return []
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
