from db.db_config import get_connection

class CompanyProfile:
    def __init__(self, company_id, company_name, description, website, industry, size, location, profile_picture_path=None):
        self.company_id = company_id
        self.company_name = company_name
        self.description = description
        self.website = website
        self.industry = industry
        self.size = size
        self.location = location
        self.profile_picture_path = profile_picture_path

    def save(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO companyprofile 
                (company_id, company_name, description, website, industry, size, location, profile_picture_path)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    company_name = VALUES(company_name),
                    description = VALUES(description),
                    website = VALUES(website),
                    industry = VALUES(industry),
                    size = VALUES(size),
                    location = VALUES(location),
                    profile_picture_path = VALUES(profile_picture_path)
            """
            cursor.execute(query, (
                self.company_id,
                self.company_name,
                self.description,
                self.website,
                self.industry,
                self.size,
                self.location,
                self.profile_picture_path
            ))
            conn.commit()
        except Exception as e:
            print("⚠️ Şirket profili kaydedilemedi:", e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def get_by_company_id(company_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = """
                SELECT company_name, description, website, industry, size, location, profile_picture_path
                FROM companyprofile
                WHERE company_id = %s
            """
            cursor.execute(query, (company_id,))
            row = cursor.fetchone()
            if row:
                return CompanyProfile(company_id, *row)
            return None
        except Exception as e:
            print("⚠️ Şirket profili alınamadı:", e)
            return None
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
