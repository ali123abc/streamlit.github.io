import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
import pandas as pd

class FinanceDatabase:
    def __init__(self):
        self.cnx = None

    def connect(self):
        # Establish a connection to the MySQL database
        try:
            self.cnx = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='finance'
            )
            print("Connected to the database.")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Access denied. Check your username and password.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist.")
            else:
                print("Error occurred:", err)

    def close(self):
        # Close the database connection
        if self.cnx:
            self.cnx.close()
            print("Database connection closed.")

    def check_user_credentials(self, username, password):
        if not self.cnx:
            print("Not connected to the database.")
            return False

        cursor = self.cnx.cursor()
        query = "SELECT COUNT(*) FROM users WHERE username = %s AND password = %s"
        values = (username, password)

        try:
            cursor.execute(query, values)
            result = cursor.fetchone()
            if result:
                count = result[0]
                return count
            else:
                return False
        except mysql.connector.Error as err:
            print("Error occurred:", err)
            return False

        cursor.close()
        
    def check_username_exists(self, username):
        if not self.cnx:
            print("Not connected to the database.")
            return False

        cursor = self.cnx.cursor()
        query = "SELECT COUNT(*) FROM users WHERE username = %s"
        values = (username,)

        try:
            cursor.execute(query, values)
            result = cursor.fetchone()
            if result:
                count = result[0]
                return count > 0
            else:
                return False
        except mysql.connector.Error as err:
            print("Error occurred:", err)
            return False

        cursor.close()

    def insert_user(self, username, password):
        if not self.cnx:
            print("Not connected to the database.")
            return

        cursor = self.cnx.cursor()
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        values = (username, password)

        try:
            cursor.execute(query, values)
            self.cnx.commit()
            print("User inserted successfully.")
        except mysql.connector.Error as err:
            print("Error occurred:", err)

        cursor.close()

    def insert_income_record(self, user_id, amount):
        if not self.cnx:
            print("Not connected to the database.")
            return

        cursor = self.cnx.cursor()
        query = "INSERT INTO income (user_id, amount, updated_at) VALUES (%s, %s, %s)"
        values = (user_id, amount, datetime.now())

        try:
            cursor.execute(query, values)
            self.cnx.commit()
            print("Record inserted successfully.")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Table already exists.")
            else:
                print("Error occurred:", err)

        cursor.close()

    def insert_outgoings_record(self, user_id, label, amount, payment_date, recurring, recurring_date):
        if not self.cnx:
            print("Not connected to the database.")
            return

        cursor = self.cnx.cursor()
        query = "INSERT INTO outgoings (user_id, label, amount, payment_date, recurring, recurring_date, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (user_id, label, amount, payment_date, recurring, recurring_date, datetime.now())

        try:
            cursor.execute(query, values)
            self.cnx.commit()
            print("Record inserted successfully.")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Table already exists.")
            else:
                print("Error occurred:", err)

        cursor.close()

    def get_current_balance(self):
        if not self.cnx:
            print("Not connected to the database.")
            return

        cursor = self.cnx.cursor()
        query = "SELECT amount FROM balance ORDER BY updated_at DESC LIMIT 1"

        try:
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                return result[0]  # Return the first column (amount) of the result
            else:
                print("No balance record found.")
                return 0
        except mysql.connector.Error as err:
            print("Error occurred:", err)

        cursor.close()

    def get_income_and_outgoing(self):
        if not self.cnx:
            print("Not connected to the database.")
            return None, None

        cursor = self.cnx.cursor()
        query = "SELECT amount FROM income ORDER BY updated_at DESC LIMIT 1"
        try:
            cursor.execute(query)
            monthly_income = cursor.fetchone()
            if monthly_income:
                monthly_income = monthly_income[0]
            else:
                monthly_income = 0.0 

            query = "SELECT SUM(amount) FROM outgoings"
            cursor.execute(query)
            total_outgoing = cursor.fetchone()
            if total_outgoing:
                total_outgoing = total_outgoing[0]
            else:
                total_outgoing = 0.0

            return monthly_income, total_outgoing
        except mysql.connector.Error as err:
            print("Error occurred:", err)
            return None, None

    def update_income(self, user_id, monthly_income, income_change_day):
        if not self.cnx:
            print("Not connected to the database.")
            return

        cursor = self.cnx.cursor()
        query = "INSERT INTO income (user_id, amount, income_change_day, updated_at) VALUES (%s, %s, %s, %s)"
        values = (user_id, monthly_income, income_change_day, datetime.now())

        try:
            cursor.execute(query, values)
            self.cnx.commit()
            print("Income updated successfully.")
        except mysql.connector.Error as err:
            print("Error occurred:", err)

        cursor.close()

    def update_outgoing(self, outgoing_data):
        if not self.cnx:
            print("Not connected to the database.")
            return

        cursor = self.cnx.cursor()
        query = "INSERT INTO outgoings (label, amount, payment_date, recurring, recurring_date, created_at) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (
            outgoing_data["label"],
            outgoing_data["amount"],
            outgoing_data["payment_date"],
            outgoing_data["recurring"],
            outgoing_data["recurring_date"],
            datetime.now(),
        )

        try:
            cursor.execute(query, values)
            self.cnx.commit()
            print("Outgoing record inserted successfully.")
        except mysql.connector.Error as err:
            print("Error occurred:", err)

        cursor.close()

    def get_outgoings(self):
        if not self.cnx:
            print("Not connected to the database.")
            return None

        cursor = self.cnx.cursor()
        query = "SELECT * FROM outgoings"
        try:
            cursor.execute(query)
            results = cursor.fetchall()

            if results:
                columns = [desc[0] for desc in cursor.description]  # Get the column names from the cursor description
                outgoing_df = pd.DataFrame(results, columns=columns)
                return outgoing_df
            else:
                print("No outgoing records found.")
                return pd.DataFrame()  # Return an empty DataFrame if no records found
        except mysql.connector.Error as err:
            print("Error occurred:", err)
            return None

    def insert_balance_record(self, amount):
        if not self.cnx:
            print("Not connected to the database.")
            return

        cursor = self.cnx.cursor()
        query = "INSERT INTO balance (amount, updated_at) VALUES (%s, %s)"
        values = (amount, datetime.now())

        try:
            cursor.execute(query, values)
            self.cnx.commit()
            print("Balance record inserted successfully.")
        except mysql.connector.Error as err:
            print("Error occurred:", err)

        cursor.close()

    def clear_database(self):
        if not self.cnx:
            print("Not connected to the database.")
            return

        cursor = self.cnx.cursor()

        try:
            cursor.execute('DELETE FROM income')
            cursor.execute('DELETE FROM balance')
            cursor.execute('DELETE FROM outgoings')
            self.cnx.commit()
            print("Database cleared successfully.")
        except mysql.connector.Error as err:
            print("Error occurred:", err)

        cursor.close()
