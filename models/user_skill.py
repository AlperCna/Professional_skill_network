from db.db_config import get_connection

class UserSkill:
    def __init__(self, user_id, skill_id, level, endorsed_count=0):
        self.user_id = user_id
        self.skill_id = skill_id
        self.level = level
        self.endorsed_count = endorsed_count

    def save(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO UserSkills (user_id, skill_id, level, endorsed_count)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    level = VALUES(level),
                    endorsed_count = VALUES(endorsed_count)
            """
            cursor.execute(query, (self.user_id, self.skill_id, self.level, self.endorsed_count))
            conn.commit()
        except Exception as e:
            print("⚠️ UserSkill kaydetme hatası:", e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def get_skills_by_user(user_id):
        conn = get_connection()
        skills = []
        try:
            cursor = conn.cursor()
            query = """
                SELECT s.id, s.skill_name, us.level, us.endorsed_count
                FROM UserSkills us
                JOIN Skills s ON us.skill_id = s.id
                WHERE us.user_id = %s
            """
            cursor.execute(query, (user_id,))
            skills = cursor.fetchall()
        except Exception as e:
            print("⚠️ Kullanıcıya ait yetenekleri alma hatası:", e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
        return skills

    @staticmethod
    def delete(user_id, skill_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = "DELETE FROM UserSkills WHERE user_id = %s AND skill_id = %s"
            cursor.execute(query, (user_id, skill_id))
            conn.commit()
        except Exception as e:
            print("⚠️ UserSkill silme hatası:", e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
