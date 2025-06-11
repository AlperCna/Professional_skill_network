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
            # Endorsement kaydı ekle
            cursor.execute("""
                INSERT INTO SkillEndorsement (endorser_id, endorsed_user_id, skill_id, endorsed_at)
                VALUES (%s, %s, %s, %s)
            """, (self.endorser_id, self.endorsed_user_id, self.skill_id, self.endorsed_at))

            # Kullanıcının ilgili becerisinin onay sayısını artır
            cursor.execute("""
                UPDATE UserSkills
                SET endorsed_count = endorsed_count + 1
                WHERE user_id = %s AND skill_id = %s
            """, (self.endorsed_user_id, self.skill_id))

            conn.commit()
        except Exception as e:
            print("⚠️ Endorsement kayıt hatası:", e)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def has_already_endorsed(endorser_id, endorsed_user_id, skill_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 1 FROM SkillEndorsement
                WHERE endorser_id = %s AND endorsed_user_id = %s AND skill_id = %s
            """, (endorser_id, endorsed_user_id, skill_id))
            return cursor.fetchone() is not None
        except Exception as e:
            print("⚠️ Endorsement kontrol hatası:", e)
            return False
        finally:
            cursor.close()
            conn.close()
