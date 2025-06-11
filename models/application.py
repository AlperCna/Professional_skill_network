from db.db_config import get_connection
from datetime import datetime

class Application:
    def __init__(self, user_id, job_id, status="pending", applied_at=None, id=None, cv_file=None):
        self.id = id
        self.user_id = user_id
        self.job_id = job_id
        self.status = status
        self.applied_at = applied_at or datetime.now()
        self.cv_file = cv_file

    def save(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO Application (user_id, job_id, status, cv_file)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (self.user_id, self.job_id, self.status, self.cv_file))

            conn.commit()
            self.id = cursor.lastrowid
        except Exception as e:
            print("⚠️ Başvuru kaydedilemedi:", e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def has_applied(user_id, job_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM Application WHERE user_id = %s AND job_id = %s", (user_id, job_id))
            return cursor.fetchone() is not None
        except Exception as e:
            print("⚠️ Başvuru kontrol hatası:", e)
            return False
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def get_applications_to_company(company_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = """
                SELECT a.id, u.fullName, j.title, a.status, a.applied_at
                FROM Application a
                JOIN JobPost j ON a.job_id = j.id
                JOIN Users u ON a.user_id = u.id
                WHERE j.company_id = %s
                ORDER BY a.applied_at DESC
            """
            cursor.execute(query, (company_id,))
            return cursor.fetchall()
        except Exception as e:
            print("⚠️ Şirket başvuruları listelenemedi:", e)
            return []
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def get_applications_by_user(user_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = """
                SELECT j.title, c.company_name, a.status, a.applied_at
                FROM Application a
                JOIN JobPost j ON a.job_id = j.id
                JOIN CompanyProfile c ON j.company_id = c.company_id
                WHERE a.user_id = %s
                ORDER BY a.applied_at DESC
            """
            cursor.execute(query, (user_id,))
            return cursor.fetchall()
        except Exception as e:
            print("⚠️ Kullanıcının başvuruları alınamadı:", e)
            return []
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def update_status(application_id, new_status):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE Application SET status = %s WHERE id = %s", (new_status, application_id))
            conn.commit()
        except Exception as e:
            print("⚠️ Durum güncellenemedi:", e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    @staticmethod
    def get_application_detail(application_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = """
                SELECT 
                    a.id,
                    u.fullName,
                    u.email,
                    j.title,
                    a.applied_at,
                    a.status,
                    a.cv_file
                FROM Application a
                JOIN Users u ON a.user_id = u.id
                JOIN JobPost j ON a.job_id = j.id
                WHERE a.id = %s
            """
            cursor.execute(query, (application_id,))
            result = cursor.fetchone()
            if result:
                return {
                    "application_id": result[0],
                    "candidate_name": result[1],
                    "candidate_email": result[2],
                    "job_title": result[3],
                    "applied_at": result[4],
                    "status": result[5],
                    "cv_file": result[6]
                }
            return None
        except Exception as e:
            print("⚠️ Başvuru detayı alınamadı:", e)
            return None
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

