from db.db_config import get_connection

class User:
    def __init__(self,fullName,email,password_hash,role,created_at=None,id=None):
        self.id = id
        self.fullName = fullName
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.created_at_ = created_at
