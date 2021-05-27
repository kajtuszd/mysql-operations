import os
import time
import mysql.connector


def connect_to_databases():
    """ Connect to given databases. Return connections. """
    connection1 = mysql.connector.connect(host=os.environ['HOST_1'],
                                          database=os.environ['DATABASE_1'],
                                          user=os.environ['USER_1'],
                                          password=os.environ['PASSWORD_1'])
    connection2 = mysql.connector.connect(host=os.environ['HOST_2'],
                                          database=os.environ['DATABASE_2'],
                                          user=os.environ['USER_2'],
                                          password=os.environ['PASSWORD_2'])
    return connection1, connection2


def extract_create_table_query(cursor):
    """
    Connect to first database and return SQL CREATE TABLE query
    in order to use it while target database creation.
    """
    create_table_query = ""
    show_create_table_query = """SHOW CREATE TABLE employees.titles;"""
    cursor.execute(show_create_table_query)
    create_table_info = cursor.fetchall()
    for element in create_table_info[0][1:][0]:
        create_table_query += element
    return create_table_query


def disconnect_from_databases(connection1, connection2, cursor1, cursor2):
    """ Terminate connections with databases. """
    if connection1.is_connected():
        cursor1.close()
        connection1.close()
        print("MySQL connection1 closed")
    if connection2.is_connected():
        cursor2.close()
        connection2.close()
        print("MySQL connection2 closed")


def get_records_from_database(cursor):
    """ Return table records from given database. """
    show_table_query = """SELECT * FROM employees.titles"""
    cursor.execute(show_table_query)
    return cursor.fetchall()


def insert_table_to_database(records, cursor, connection):
    """ Insert all records to target database. """
    start_insert = time.time()
    query = """INSERT INTO employees_copy.titles(emp_no, title, from_date, 
    to_date) VALUES (%s, %s, %s, %s); """
    params = [(record[0], record[1], record[2], record[3]) for record in records]
    cursor.executemany(query, params)
    connection.commit()
    end_insert = time.time()
    print("Insert time is {}".format(end_insert - start_insert))


def copy_table_to_database(cursor1, cursor2, connection2):
    """ Copy table to target database. """
    start_copy = time.time()
    create_table_query = extract_create_table_query(cursor1)
    cursor2.execute("""{}""".format(create_table_query))
    records = get_records_from_database(cursor1)
    insert_table_to_database(records, cursor2, connection2)
    end_copy = time.time()
    print("Copy time is {}".format(end_copy - start_copy))


def main():
    try:
        connection1, connection2 = connect_to_databases()
        cursor1 = connection1.cursor()
        cursor2 = connection2.cursor()
        copy_table_to_database(cursor1, cursor2, connection2)
    except mysql.connector.Error as error:
        print("Error: {}".format(error))
    finally:
        disconnect_from_databases(connection1, connection2, cursor1, cursor2)


if __name__ == "__main__":
    main()
