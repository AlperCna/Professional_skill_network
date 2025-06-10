from db.db_config import get_connection
from datetime import datetime

class SkillEndorsement:
    def __init__(self, endorser_id, endorsed_user_id, skill_id, endorsed_at=None):
        self.endorser_id = endorser_id
        self.endorsed_user_id = endorsed_user_id
        self.skill_id = skill_id
        self.endorsed_at = endorsed_at or datetime.now()

    def save(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            # SkillEndorsement tablosuna ekle
            query = """
                INSERT INTO SkillEndorsement (endorser_id, endorsed_user_id, skill_id, endorsed_at)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE endorsed_at = VALUES(endorsed_at)
            """
            cursor.execute(query, (self.endorser_id, self.endorsed_user_id, self.skill_id, self.endorsed_at))

            # UserSkills tablosundaki endorsed_count'ı 1 artır
            update_query = """
                UPDATE UserSkills
                SET endorsed_count = endorsed_count + 1
                WHERE user_id = %s AND skill_id = %s
            """
            cursor.execute(update_query, (self.endorsed_user_id, self.skill_id))

            conn.commit()
        except Exception as e:
            print("⚠️ Endorsement kaydetme hatası:", e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def has_already_endorsed(endorser_id, endorsed_user_id, skill_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = """
                SELECT * FROM SkillEndorsement
                WHERE endorser_id = %s AND endorsed_user_id = %s AND skill_id = %s
            """
            cursor.execute(query, (endorser_id, endorsed_user_id, skill_id))
            return cursor.fetchone() is not None
        except Exception as e:
            print("⚠️ Endorsement sorgulama hatası:", e)
            return False
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
