from db.db_config import get_connection
from datetime import datetime

class Connection:
    def __init__(self, user1_id, user2_id, status="pending", requested_at=None):
        self.user1_id = user1_id
        self.user2_id = user2_id
        self.status = status
        self.requested_at = requested_at or datetime.now()

    def send_request(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO connection (user1_id, user2_id, status, requested_at)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE status = 'pending', requested_at = VALUES(requested_at)
            """
            cursor.execute(query, (self.user1_id, self.user2_id, self.status, self.requested_at))
            conn.commit()
        except Exception as e:
            print("⚠️ Bağlantı isteği hatası:", e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def respond_to_request(user1_id, user2_id, new_status):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = """
                UPDATE connection
                SET status = %s
                WHERE user1_id = %s AND user2_id = %s
            """
            cursor.execute(query, (new_status, user1_id, user2_id))
            conn.commit()
        except Exception as e:
            print("⚠️ İstek yanıtlanamadı:", e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def get_connections(user_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = """
                SELECT user1_id, user2_id, status
                FROM connection
                WHERE (user1_id = %s OR user2_id = %s) AND status = 'accepted'
            """
            cursor.execute(query, (user_id, user_id))
            return cursor.fetchall()
        except Exception as e:
            print("⚠️ Bağlantı listesi alınamadı:", e)
            return []
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def exists_between(user1_id, user2_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = """
                SELECT 1 FROM Connection
                WHERE 
                    (user1_id = %s AND user2_id = %s) OR 
                    (user1_id = %s AND user2_id = %s)
                LIMIT 1
            """
            cursor.execute(query, (user1_id, user2_id, user2_id, user1_id))
            return cursor.fetchone() is not None
        except Exception as e:
            print("⚠️ Connection kontrol hatası:", e)
            return False
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
