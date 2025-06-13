from db.db_config import get_connection

class UserProfile:
    def __init__(self, user_id, headline, bio, location, phone, birthdate, gender, website, verified=False, profile_picture_path=None):
        self.user_id = user_id
        self.headline = headline
        self.bio = bio
        self.location = location
        self.phone = phone
        self.birthdate = birthdate
        self.gender = gender
        self.website = website
        self.verified = verified
        self.profile_picture_path = profile_picture_path

    @staticmethod
    def get_by_user_id(user_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = """
                SELECT headline, bio, location, phone, birthdate, gender, website, verified, profile_picture_path
                FROM UserProfile WHERE user_id = %s
            """
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            if result:
                return UserProfile(user_id, *result)
            return None
        except Exception as e:
            print("⚠️ Profil getirme hatası:", e)
            return None
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def save(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO UserProfile (user_id, headline, bio, location, phone, birthdate, gender, website, verified, profile_picture_path)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    headline = VALUES(headline),
                    bio = VALUES(bio),
                    location = VALUES(location),
                    phone = VALUES(phone),
                    birthdate = VALUES(birthdate),
                    gender = VALUES(gender),
                    website = VALUES(website),
                    verified = VALUES(verified),
                    profile_picture_path = VALUES(profile_picture_path)
            """
            values = (
                self.user_id, self.headline, self.bio, self.location,
                self.phone, self.birthdate, self.gender,
                self.website, self.verified, self.profile_picture_path
            )
            cursor.execute(query, values)
            conn.commit()
        except Exception as e:
            print("⚠️ Profil kaydetme hatası:", e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
