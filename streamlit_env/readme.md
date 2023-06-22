## `main.py`
This file contains the main functionality of the financial management system. It includes the user interface using Streamlit and connects to a finance database using the `FinanceDatabase` class. The file also includes a `SessionState` class for managing session-specific data.

### Methods:
1. `generate_yearly_income_chart(finance_db, monthly_income, total_outgoing)`: This method generates a yearly income chart and table. It takes three parameters:
   - `finance_db`: An instance of the `FinanceDatabase` class for database operations.
   - `monthly_income`: The monthly income value.
   - `total_outgoing`: The total outgoing value.

   Inside the method:
   - It calculates the current month and the number of remaining months in the year.
   - It retrieves the current balance from the database and converts it to a float.
   - It calculates the monthly balances and monthly totals based on the provided income and outgoing values.
   - It creates a table using Pandas DataFrame and displays it using Streamlit's `st.table()` function.
   - It converts the monthly balances to valid values for plotting.
   - It creates a scatter plot of the monthly balances using Matplotlib and displays it using Streamlit's `st.pyplot()` function.

2. `main()`: This method is the entry point of the financial management system. It sets up the Streamlit user interface and handles user interactions.

   Inside the method:
   - It establishes a connection to the finance database.
   - It allows the user to navigate between the "Home" and "Add Outgoings" pages using Streamlit's `st.sidebar.radio()` function.
   - If the user selects "Home":
     - It retrieves the monthly income and total outgoing values from the database.
     - It creates a session state object and displays a number input for the monthly income.
     - It calculates the total income based on the total outgoing and the provided monthly income.
     - It displays the total outgoings and total income using Streamlit's `st.write()` function.
     - It calls the `generate_yearly_income_chart()` method to display the yearly income chart and table.
     - It updates the monthly income in the database if the user clicks the "Update" button.
     - It retrieves and displays the current balance from the database.
     - It allows the user to update the balance in the database using a number input and button.
   - If the user selects "Add Outgoings", it creates an instance of the `OutgoingsPage` class and calls its `main()` method.

## `outgoings.py`
This file contains the `OutgoingsPage` class, which is responsible for managing the outgoings functionality of the financial management system. It interacts with a finance database using the `FinanceDatabase` class and allows users to add and view outgoing payments.

### Methods:
1. `__init__(self)`: The constructor method initializes the `OutgoingsPage` class and calls the `load_data()` method.

2. `load_data(self)`: This method loads the data from the 'accounts.csv' file into the `accounts_df` attribute. If the file is not found or if the 'Total Outgoing' column is missing, it creates a new DataFrame with a 'Total Outgoing' column.

3. `save_data(self)`: This method saves the `accounts_df` DataFrame into the 'accounts.csv' file.

4. `main(self)`: This method is the entry point for the outgoings functionality. It sets up the Streamlit user interface and handles user interactions.

   Inside the method:
   - It displays the title 'Outgoings' using Streamlit's `st.title()` function.
   - It retrieves the last recorded total outgoing from the `accounts_df` DataFrame.
   - It displays a text input for the payment title, a checkbox for recurring payments, and a number input for the outgoing amount.
   - If the user clicks the 'Add' button, it updates the total outgoing, creates an instance of the `FinanceDatabase` class, inserts the outgoing record into the database, and adds a new row to the `accounts_df` DataFrame.
   - It displays the total outgoing using Streamlit's `st.write()` function.
   - It displays a header 'Outgoing Details' and fetches the outgoing details from the database using the `get_outgoing_details()` method of the `FinanceDatabase` class.
   - It displays the outgoing details in a table using Streamlit's `st.table()` function.
   - It closes the database connection.

## `connection.py`
This file contains the `FinanceDatabase` class, which handles the connection and interaction with the MySQL database for the financial management system.

### Methods:
1. `__init__(self)`: The constructor method initializes the `FinanceDatabase` class and sets the `cnx` attribute to `None`.

2. `connect(self)`: This method establishes a connection to the MySQL database using the provided host, username, password, and database name. It handles potential connection errors and prints appropriate messages.

3. `close(self)`: This method closes the database connection if it is currently open.

4. `insert_income_record(self, user_id, amount)`: Inserts an income record into the 'income' table of the database, including the user ID, amount, and the current timestamp.

5. `insert_outgoings_record(self, user_id, label, amount, payment_date, recurring, recurring_date)`: Inserts an outgoings record into the 'outgoings' table of the database, including the user ID, label, amount, payment date, recurring flag, recurring date, and the current timestamp.

6. `get_current_balance(self)`: Retrieves the current balance from the 'balance' table of the database. It returns the amount of the most recent balance record.

7. `get_income_and_outgoing(self)`: Retrieves the monthly income and total outgoing amount from the 'income' and 'outgoings' tables of the database. It returns these values as a tuple.

8. `update_income(self, user_id, monthly_income)`: Updates the monthly income for a specific user in the 'income' table of the database.

9. `update_outgoing(self, outgoing_data)`: Inserts an outgoing record into the 'outgoings' table of the database using a dictionary of outgoing data.

10. `get_outgoings(self)`: Retrieves all the outgoings records from the 'outgoings' table of the database and returns them as a DataFrame.

11. `insert_balance_record(self, amount)`: Inserts a balance record into the 'balance' table of the database, including the amount and the current timestamp.


