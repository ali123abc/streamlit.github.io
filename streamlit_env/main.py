import streamlit as st
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from outgoings import OutgoingsPage
from connection import FinanceDatabase
from decimal import Decimal
from dateutil.relativedelta import relativedelta
from goals import GoalsPage

class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class MainApp:
    def __init__(self, finance_db):
        self.finance_db = finance_db
        self.session_state = SessionState(user_id=None)


    def generate_yearly_income_chart(self, monthly_income, total_outgoing):
        # Access user_id from session state
        user_id = self.session_state.user_id

        today = datetime.date.today()
        current_month = today.month

        remaining_months = 12 - current_month + 1
        balance = self.finance_db.get_current_balance()

        if balance is None:
            balance = 0.0
        else:
            balance = float(balance)

        monthly_balances = [balance]
        monthly_totals = [float(monthly_income) - float(total_outgoing)]

        for _ in range(remaining_months - 1):
            today += relativedelta(months=1)  # Add one month to the current date
            balance = balance + float(monthly_income) - float(total_outgoing)
            monthly_balances.append(balance)
            monthly_totals.append(float(monthly_income) - float(total_outgoing))

        months = pd.date_range(start=today.replace(day=1), periods=remaining_months, freq='MS').strftime('%b')

        table_data = {'Date of Transaction': pd.date_range(start=today.replace(day=1), periods=remaining_months, freq='MS'),
                      'Balance': monthly_balances, 'Total Change': monthly_totals}
        table_df = pd.DataFrame(table_data, columns=["Date of Transaction", "Balance", "Total Change"])
        table_df["Balance"] = table_df["Balance"].apply(lambda x: f"£{x:.2f}")
        table_df["Total Change"] = table_df["Total Change"].apply(lambda x: f"£{x:.2f}")

        st.subheader("Monthly Balance Predictions")
        st.table(table_df)

        # Convert masked values to valid values for plotting
        monthly_balances = np.ma.masked_invalid(monthly_balances).filled(np.nan)

        fig, ax = plt.subplots()
        ax.scatter(months, monthly_balances, marker='o')
        ax.plot(months, monthly_balances, linestyle=':', marker='')
        ax.set_xlabel('Month')
        ax.set_ylabel('Balance')
        ax.set_title('Yearly Balance')
        st.pyplot(fig)

    def main(self):
        st.title('Financial Management System')

        navigation = st.sidebar.radio("Navigation", ('Home', 'Add Outgoings','Goals'))

        if navigation == 'Home':
            monthly_income, total_outgoing = self.finance_db.get_income_and_outgoing()

            if monthly_income is None:
                monthly_income = 0.0

            if not total_outgoing:
                total_outgoing = 0

            monthly_income = st.number_input('Monthly Income', value=float(monthly_income), min_value=0.0, step=100.0)

            # Get the income change day from the user
            income_change_day = st.number_input('Income Change Day', value=1, min_value=1, max_value=31)
            if st.button('Update Income'):
                self.finance_db.update_income(user_id=self.session_state.user_id, monthly_income=monthly_income, income_change_day=income_change_day)
                st.success('Income successfully updated')
            else:
                st.warning('Income not updated')

            # Calculate total income
            total_outgoing = float(total_outgoing)
            total_income = total_outgoing + monthly_income

            # Display total income
            st.write(f'Total Outgoings: £{total_outgoing:.2f}')
            st.write(f'Total Income: £{total_income:.2f}')

            self.generate_yearly_income_chart(monthly_income, total_outgoing)

            # Retrieve the current balance from the database or set it to 0.0 if it doesn't exist
            balance = self.finance_db.get_current_balance() or 0.0
            st.write(f'Current Balance: £{balance:.2f}')

            # Update the balance in the database
            balance_input = st.number_input('Update Balance', min_value=0.0, step=100.0)
            if st.button('Update'):
                self.finance_db.insert_balance_record(amount=balance_input)
                st.success('Balance successfully updated')
            else:
                st.warning('Balance not updated')
            
            if st.button('Clear Database'):
                self.finance_db.clear_database()
                st.success('Database cleared successfully.')

        elif navigation == 'Add Outgoings':
            outgoings_page = OutgoingsPage()
            outgoings_page.main(self.session_state.user_id) 
        
        elif navigation == "Goals":
            goals_page = GoalsPage()
            goals_page.main(self.session_state.user_id)


        self.finance_db.close()

    def set_user_id(self, user_id):
        self.session_state.user_id = user_id


if __name__ == '__main__':
    finance_db = FinanceDatabase()
    finance_db.connect()
    main_app = MainApp(finance_db)

    # Set the user_id based on the logged-in user
    user_id = 1  # Replace with the actual user_id from the login process
    main_app.set_user_id(user_id)

    main_app.main()

    finance_db.close()





