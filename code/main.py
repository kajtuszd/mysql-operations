import os
import time
import mysql.connector


def extract_create_table_query(cursor):
    create_table_query = ""
    show_create_table_query = """SHOW CREATE TABLE employees.titles;"""
    cursor.execute(show_create_table_query)
    create_table_info = cursor.fetchall()
    for element in create_table_info[0][1:][0]:
        create_table_query += element
    return create_table_query


def copy_table_to_database(records, cursor, connection):
    start = time.time()
    for record in records:
        insert_to_table_query = """INSERT INTO employees_copy.titles(
            emp_no, title, from_date, to_date) VALUES ('{}','{}','{}','{}');""".format(
            record[0], record[1], record[2], record[3])
        cursor.execute(insert_to_table_query)
    connection.commit()
    end = time.time()
    print("Elapsed time is {}".format(end - start))


try:
    connection1 = mysql.connector.connect(host=os.environ['HOST_1'],
                                         database=os.environ['DATABASE_1'],
                                         user=os.environ['USER_1'],
                                         password=os.environ['PASSWORD_1'])

    connection2 = mysql.connector.connect(host=os.environ['HOST_2'],
                                         database=os.environ['DATABASE_2'],
                                         user=os.environ['USER_2'],
                                         password=os.environ['PASSWORD_2'])
    cursor1 = connection1.cursor()
    cursor2 = connection2.cursor()

    create_table_query = extract_create_table_query(cursor1)
    
    cursor2.execute("""{}""".format(create_table_query))
    show_table_query = """SELECT * FROM employees.titles"""
    cursor1.execute(show_table_query)
    records = cursor1.fetchall()
    
    copy_table_to_database(records, cursor2, connection2)

except mysql.connector.Error as error:
    print("Error: {}".format(error))

finally:
    if connection1.is_connected():
        cursor1.close()
        connection1.close()
        print("MySQL connection1 closed")
    if connection2.is_connected():
        cursor2.close()
        connection2.close()
        print("MySQL connection2 closed")
