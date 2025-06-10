from db.db_config import get_connection
from datetime import datetime

class JobPost:
    def __init__(self, company_id, title, description, requirements, job_type, deadline, id=None, posted_at=None):
        self.id = id
        self.company_id = company_id
        self.title = title
        self.description = description
        self.requirements = requirements
        self.job_type = job_type
        self.deadline = deadline
        self.posted_at = posted_at or datetime.now()

    def save(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO JobPost (company_id, title, description, requirements, job_type, deadline)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                self.company_id, self.title, self.description,
                self.requirements, self.job_type, self.deadline
            ))
            conn.commit()
            self.id = cursor.lastrowid
        except Exception as e:
            print("⚠️ İlan eklenemedi:", e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = """
                SELECT id, company_id, title, description, requirements, job_type, posted_at, deadline
                FROM JobPost
                ORDER BY posted_at DESC
            """
            cursor.execute(query)
            results = cursor.fetchall()
            return [JobPost(*row[1:], id=row[0], posted_at=row[6]) for row in results]
        except Exception as e:
            print("⚠️ İlan listelenemedi:", e)
            return []
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

