from db.db_config import get_connection

class Message:
    def __init__(self, sender_id, receiver_id, text, sent_at=None):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.text = text
        self.sent_at = sent_at

    def save(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = "INSERT INTO Message (sender_id, receiver_id, text) VALUES (%s, %s, %s)"
            cursor.execute(query, (self.sender_id, self.receiver_id, self.text))
            conn.commit()
        except Exception as e:
            print("❌ Mesaj kaydedilemedi:", e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def get_conversation(user1_id, user2_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = """
                SELECT sender_id, receiver_id, text, sent_at
                FROM Message
                WHERE (sender_id = %s AND receiver_id = %s)
                   OR (sender_id = %s AND receiver_id = %s)
                ORDER BY sent_at ASC
            """
        # Aynı sorguda iki yönde konuşmaları getiriyoruz
            cursor.execute(query, (user1_id, user2_id, user2_id, user1_id))
            return cursor.fetchall()
        except Exception as e:
            print("❌ Mesajlar alınamadı:", e)
            return []
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
