from db.db_config import get_connection
from datetime import datetime

class JobPost:
    def __init__(self, company_id, title, description, requirements, job_type, deadline,
                 id=None, posted_at=None, company_name=None):
        self.id = id
        self.company_id = company_id
        self.company_name = company_name
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
    def get_all_for_listing():
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = """
                SELECT 
                    j.id, j.title, c.company_name, j.job_type, j.deadline
                FROM 
                    JobPost j
                JOIN 
                    CompanyProfile c ON j.company_id = c.company_id
                ORDER BY 
                    j.posted_at DESC
            """
            cursor.execute(query)
            results = cursor.fetchall()
            job_list = []
            for row in results:
                job = JobPost(
                    company_id=None,
                    title=row[1],
                    description="",
                    requirements="",
                    job_type=row[3],
                    deadline=row[4],
                    id=row[0],
                    company_name=row[2]
                )
                job_list.append(job)
            return job_list
        except Exception as e:
            print("⚠️ Job listing failed:", e)
            return []
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
            job_list = []
            for row in results:
                id, company_id, title, description, requirements, job_type, posted_at, deadline = row
                job = JobPost(
                    company_id=company_id,
                    title=title,
                    description=description,
                    requirements=requirements,
                    job_type=job_type,
                    deadline=deadline,
                    id=id,
                    posted_at=posted_at
                )
                job_list.append(job)
            return job_list
        except Exception as e:
            print("⚠️ Job list error:", e)
            return []
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
