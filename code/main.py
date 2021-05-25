import mysql.connector
import os

try:
    connection = mysql.connector.connect(host=os.environ['HOST_2'],
                                         database=os.environ['DATABASE_2'],
                                         user=os.environ['USER_2'],
                                         password=os.environ['PASSWORD_2'])
    cursor = connection.cursor()
    show_table_query = """SHOW TABLES FROM employees_copy"""
    cursor.execute(show_table_query)
    result = cursor.fetchall()
    print(result)

    print("Table shown successfully ")

except mysql.connector.Error as error:
    print("Failed to show table: {}".format(error))
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

