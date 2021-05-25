import os
import mysql.connector

'''
tests to be run before main.py file execution
'''

def test_check_titles_are_not_in_database_employees_copy():
    connection = mysql.connector.connect(host=os.environ['HOST_2'],
                                         database=os.environ['DATABASE_2'],
                                         user=os.environ['USER_2'],
                                         password=os.environ['PASSWORD_2'])
    cursor = connection.cursor()
    show_table_query = """SHOW TABLES FROM employees_copy"""
    cursor.execute(show_table_query)
    result = cursor.fetchall()
    assert len(result) == 7
    assert ('titles',) not in result


def test_check_titles_are_in_database_employees():
    connection = mysql.connector.connect(host=os.environ['HOST_1'],
                                         database=os.environ['DATABASE_1'],
                                         user=os.environ['USER_1'],
                                         password=os.environ['PASSWORD_1'])
    cursor = connection.cursor()
    show_table_query = """SHOW TABLES FROM employees"""
    cursor.execute(show_table_query)
    result = cursor.fetchall()
    assert len(result) == 8
    assert ('titles',) in result
