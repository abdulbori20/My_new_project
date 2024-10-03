import mysql.connector
from database.database_main import DB_NAME


def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345',
            auth_plugin='mysql_native_password',
            database=DB_NAME
        )

        return connection

    except mysql.connector.Error as e:
        print(f"Ma'lumotlar bazasiga ulanishda xatolik yuz berdi: {e}")

    return None

