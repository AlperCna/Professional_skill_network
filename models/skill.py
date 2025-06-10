from db.db_config import get_connection

class Skill:
    def __init__(self, id=None, skill_name=None, category=None):
        self.id = id
        self.skill_name = skill_name
        self.category = category

    def save(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = "INSERT INTO Skills (skill_name, category) VALUES (%s, %s)"
            cursor.execute(query, (self.skill_name, self.category))
            conn.commit()
            self.id = cursor.lastrowid
        except Exception as e:
            print("⚠️ Skill kaydetme hatası:", e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        skills = []
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, skill_name, category FROM Skills")
            rows = cursor.fetchall()
            for row in rows:
                skills.append(Skill(*row))
        except Exception as e:
            print("⚠️ Skill listeleme hatası:", e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
        return skills

    @staticmethod
    def delete_by_id(skill_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Skills WHERE id = %s", (skill_id,))
            conn.commit()
        except Exception as e:
            print("⚠️ Skill silme hatası:", e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
