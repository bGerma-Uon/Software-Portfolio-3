"""
This file contains code for creating and populating a MySQL database
"""
# Builtins
import csv
from configparser import ConfigParser

# External
import mysql.connector

# Internal
from sampleCode.sqlQueries import *

# Constants for database and file configuration
DATABASE_NAME = "myDataBase"  # Name of the database
TABLE_NAME = "customer_retention"  # Name of the table
CSV_FILE = "customer_retention.csv"  # Path to the CSV data file


class DatabaseManager:
    """
    Manages MySQL database operations like connection, creation of
    databases and tables, and data insertion from CSV files.
    """

    def __init__(
        self,
        config_file='config.ini',
        database_name=DATABASE_NAME,
        table_name=TABLE_NAME
    ):
        """
        Initialises the DatabaseManager with configuration details.

        :param config_file: (str)
            Path to the configuration file. Defaults to 'config.ini'.
        :param database_name: (str)
            Name of the database to manage. Defaults to the global
            DATABASE_NAME.
        :param table_name: (str)
            Name of the table to manage. Defaults to the global TABLE_NAME.
        """
        self.config = ConfigParser()
        self.config.read(config_file)
        self.db_config = {key: value for key, value in
                          self.config.items('mysql')}
        self.database_name = database_name
        self.table_name = table_name
        self.conn = None
        self.cursor = None

    def connect(self, use_database=False):
        """
        Establishes a connection to the MySQL server.

        :param use_database: (bool)
            If True, connect to the specified database. Otherwise, connect
            without specifying a database (e.g., for creating the database
            itself). Defaults to False.

        :raises RuntimeError:
            If the database connection fails.
        """
        try:
            if use_database:
                self.conn = mysql.connector.connect(
                    host=self.db_config["host"],
                    user=self.db_config["user"],
                    password=self.db_config["password"],
                    database=self.database_name
                )
            else:
                self.conn = mysql.connector.connect(
                    host=self.db_config["host"],
                    user=self.db_config["user"],
                    password=self.db_config["password"]
                )
            self.cursor = self.conn.cursor()
        except Exception as err:
            raise RuntimeError(f"Database connection error: {err}")

    def close(self):
        """
        Closes the database cursor and connection if they are open.
        """
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def create_database(self):
        """
        Creates the database if it does not already exist.

        Connects to the MySQL server without specifying a database,
        executes the CREATE DATABASE IF NOT EXISTS command, and then
        closes the connection.

        Raises:
            RuntimeError: If database creation fails.
        """
        self.connect(use_database=False)
        try:
            query = SQL_CREATE_DATABASE_TEMPLATE.format(self.database_name)
            self.cursor.execute(query)
            print(f"Database '{self.database_name}' ensured.")
        except Exception as err:
            raise RuntimeError(f"Failed to create database: {err}")
        finally:
            self.close()

    def create_table(self):
        """
        Creates the specified table in the database.

        Connects to the specified database, drops the table if it
        already exists, and then creates a new table with a
        predefined schema for customer retention data.

        Raises:
            RuntimeError: If table creation fails.
        """
        self.connect(use_database=True)
        try:
            drop_query = SQL_DROP_TABLE_TEMPLATE.format(self.table_name)
            self.cursor.execute(drop_query)
            create_query = SQL_CREATE_TABLE_TEMPLATE.format(self.table_name)
            self.cursor.execute(create_query)
            print(f"Table '{self.table_name}' created.")
        except Exception as err:
            raise RuntimeError(f"Failed to create table: {err}")
        finally:
            self.close()

    def insert_csv_data(self, csv_file):
        """
        Inserts data from a CSV file into the specified table.

        Connects to the database, reads data from the given CSV file,
        and inserts it into the table using a bulk insert operation.
        The CSV file must have a header row matching the table columns.

        Args:
            csv_file (str): The path to the CSV file containing
                            the data to be inserted.

        Raises:
            RuntimeError: If the CSV file is not found, or if data
                          insertion fails for other reasons.
        """
        self.connect(use_database=True)
        try:
            data_to_insert = digest_csv_data(csv_file)
            insert_query = SQL_INSERT_DATA_TEMPLATE.format(self.table_name)
            self.cursor.executemany(insert_query, data_to_insert)
            self.conn.commit()
            print(f"CSV data inserted into '{self.table_name}' successfully.")
        except FileNotFoundError:
            raise RuntimeError(f"CSV file '{csv_file}' not found.")
        except Exception as err:
            if self.conn:
                self.conn.rollback()
            raise RuntimeError(f"Failed to insert data: {err}")
        finally:
            self.close()


def digest_csv_data(csv_file: str):
    """
    Digests raw data from a CSV file and transforms into correct data types

    :return:
    """
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data_to_insert = []
        for row in reader:
            data = (
                int(row['customer_id']),
                row['customer_name'],
                row['email'],
                row['signup_date'],
                row['last_active_date'],
                bool(int(row['is_retained'])),
                row['plan_type'],
                row['region'],
                float(row['total_spent']),
                row['last_purchase_date'],
                float(row['feedback_score']),
                row['account_manager'],
                row['referral_source'],
                int(row['login_count']),
                int(row['support_tickets'])
            )
            data_to_insert.append(data)

    return data_to_insert


def main():
    """
    Main function to set up and populate the database.

    Initialises the DatabaseManager using global constants for database
    name and table name. It then attempts to create the database,
    create the table, and insert data from the global CSV_FILE path.
    Handles potential RuntimeError exceptions during these operations.
    """
    db_manager = DatabaseManager()

    try:
        db_manager.create_database()
        db_manager.create_table()
        db_manager.insert_csv_data(CSV_FILE)
    except RuntimeError as e:
        print(e)


if __name__ == "__main__":
    main()
