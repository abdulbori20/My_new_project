import mysql.connector

DB_NAME = 'Students'

##Ushbularni o'ziznikiga o'zgartiring
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = '12345'


def init_db():
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            auth_plugin='mysql_native_password'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            create_database_script = f"""
                CREATE DATABASE IF NOT EXISTS {DB_NAME};
            """
            cursor.execute(create_database_script)
            connection.commit()

            connection.database = DB_NAME

            create_users_table_script = """
                CREATE TABLE IF NOT EXISTS users(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    full_name VARCHAR(100) NOT NULL,
                    age INT,
                    major VARCHAR(100) NOT NULL,
                    username VARCHAR(100) NOT NULL UNIQUE,
                    password VARCHAR(100) NOT NULL
                );
            """
            cursor.execute(create_users_table_script)
            connection.commit()

    except mysql.connector.Error as e:
        print(f"Mysql ma'lumotlar bazasiga ulanishda xatolik yuz berdi: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

    return connection