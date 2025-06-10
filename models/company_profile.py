from db.db_config import get_connection

class CompanyProfile:
    def __init__(self, company_id, company_name, description, website, industry, size, location):
        self.company_id = company_id
        self.company_name = company_name
        self.description = description
        self.website = website
        self.industry = industry
        self.size = size
        self.location = location

    def save(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO CompanyProfile 
                (company_id, company_name, description, website, industry, size, location)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    company_name = VALUES(company_name),
                    description = VALUES(description),
                    website = VALUES(website),
                    industry = VALUES(industry),
                    size = VALUES(size),
                    location = VALUES(location)
            """
            cursor.execute(query, (
                self.company_id, self.company_name, self.description,
                self.website, self.industry, self.size, self.location
            ))
            conn.commit()
        except Exception as e:
            print("⚠️ Şirket bilgisi kaydedilemedi:", e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def get_by_company_id(company_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = "SELECT company_name, description, website, industry, size, location FROM CompanyProfile WHERE company_id = %s"
            cursor.execute(query, (company_id,))
            result = cursor.fetchone()
            if result:
                return CompanyProfile(company_id, *result)
            return None
        except Exception as e:
            print("⚠️ Şirket profili alınamadı:", e)
            return None
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
