from backend.database import get_db_connection

connection = get_db_connection()

if connection:
    cursor = connection.cursor()

    cursor.execute("SELECT DATABASE()")
    result = cursor.fetchone()

    print("Connected Database:", result[0])

    cursor.close()
    connection.close()

    print("Database connection test successful!")
else:
    print("Database connection failed!")

    