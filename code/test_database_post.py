import os
import mysql.connector

'''
tests to be run after main.py file execution
'''

def test_check_titles_are_in_database_employees_copy():
    connection = mysql.connector.connect(host=os.environ['HOST_2'],
                                         database=os.environ['DATABASE_2'],
                                         user=os.environ['USER_2'],
                                         password=os.environ['PASSWORD_2'])
    cursor = connection.cursor()
    show_table_query = """SHOW TABLES FROM employees_copy"""
    cursor.execute(show_table_query)
    result = cursor.fetchall()
    assert len(result) == 8
    assert ('titles',) in result
