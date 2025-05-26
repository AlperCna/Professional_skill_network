import mysql.connector

def get_connection():
    return mysql.connector.connect()(
        host="localhost",
        user="root",
        password="<Emr314Ir159+>",
        database="professional_skill_network"
    )