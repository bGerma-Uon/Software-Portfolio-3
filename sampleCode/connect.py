# Run this command to install the Python module 
# mysql-connector-python (which provides mysql.connector):
# "pip install mysql-connector-python"

import mysql.connector
from configparser import ConfigParser

# Read config.ini
config = ConfigParser()
config.read('config.ini')

# mysql.connector.connect() does not directly support .ini files.
# You must parse the .ini file yourself (e.g., using ConfigParser) 
# and pass the parameters as a dictionary.
# Turn the mysql section of the config file into a dictionary

db_config = {key: value for key, value in config.items('mysql')}

try:
    # Connect to MySQL
    conn = mysql.connector.connect(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
    )

    if conn.is_connected():
        print('Connected to MySQL database')
        cursor = conn.cursor()

        # Query 1: Count total employees
        cursor.execute("SELECT COUNT(*) FROM employees;")
        total_employees = cursor.fetchone()[0]
        print(f"Total employees: {total_employees}")

        # Query 2: List of departments
        cursor.execute("SELECT dept_no, dept_name FROM departments;")
        print("\nDepartments:")
        for row in cursor.fetchall():
            print(f"{row[0]}: {row[1]}")

        # Query 3: Top 5 highest paid employees
        cursor.execute("""
            SELECT e.emp_no, e.first_name, e.last_name, s.salary 
            FROM employees e
            JOIN salaries s ON e.emp_no = s.emp_no
            ORDER BY s.salary DESC
            LIMIT 5;
        """)
        print("\nTop 5 Highest Paid Employees:")
        for row in cursor.fetchall():
            print(f"{row[0]}: {row[1]} {row[2]} - ${row[3]}")

        # Query 4: Employee count by title
        cursor.execute("""
            SELECT title, COUNT(*) as count 
            FROM titles 
            GROUP BY title 
            ORDER BY count DESC;
        """)
        print("\nEmployee Count by Title:")
        for row in cursor.fetchall():
            print(f"{row[0]}: {row[1]}")

        cursor.close()

    conn.close()
    print('\nMySQL connection is closed')

except mysql.connector.Error as err:
    print(f'Error: {err}')
