from db.db_config import get_connection

class ApplicationSkill:
    def __init__(self, application_id, skill_id):
        self.application_id = application_id
        self.skill_id = skill_id

    def save(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = "INSERT INTO ApplicationSkills (application_id, skill_id) VALUES (%s, %s)"
            cursor.execute(query, (self.application_id, self.skill_id))
            conn.commit()
        except Exception as e:
            print("⚠️ ApplicationSkill kaydedilemedi:", e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def get_skills_for_application(application_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = """
                SELECT s.skill_name
                FROM ApplicationSkills a
                JOIN Skills s ON a.skill_id = s.id
                WHERE a.application_id = %s
            """
            cursor.execute(query, (application_id,))
            return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print("⚠️ Başvuruya ait skill listesi alınamadı:", e)
            return []
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
