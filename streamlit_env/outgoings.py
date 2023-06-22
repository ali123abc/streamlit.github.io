import streamlit as st
import pandas as pd
from connection import FinanceDatabase

class OutgoingsPage:
    def __init__(self):
        self.load_data()

    def load_data(self):
        try:
            self.accounts_df = pd.read_csv('accounts.csv')
            if 'Total Outgoing' not in self.accounts_df.columns:
                self.accounts_df['Total Outgoing'] = 0.0
        except FileNotFoundError:
            self.accounts_df = pd.DataFrame({'Total Outgoing': [0.0]})

    def save_data(self):
        self.accounts_df.to_csv('accounts.csv', index=False)

    def main(self,user_id):
        st.title('Outgoings')

        total_outgoing = st.session_state.get('total_outgoing', 0.0)

        outgoing_label = st.text_input('Payment Title', value='')
        recurring = st.checkbox('Recurring Payment')

        if recurring:
            recurring_day = st.selectbox('Recurring Day', range(1, 29), index=0)
            payment_date = pd.Timestamp.now().date().replace(day=recurring_day)
        else:
            payment_date = st.date_input('Payment Date', value=pd.Timestamp.now().date())

        outgoing_amount = st.number_input('Add Outgoing Amount', min_value=0.0, step=100.0)

        if st.button('Add'):
            total_outgoing += outgoing_amount
            if recurring:
                recurring_date = recurring_day
            else:
                recurring_date = None
            finance_db = FinanceDatabase()
            finance_db.connect()
            finance_db.insert_outgoings_record(user_id=1, label=outgoing_label, amount=outgoing_amount, payment_date=payment_date, recurring=recurring, recurring_date=recurring_date)
            finance_db.close()
            payment_data = {'Title': outgoing_label, 'Amount': outgoing_amount, 'Date': payment_date}
            self.accounts_df.loc[len(self.accounts_df)] = payment_data  # Add a new row to the DataFrame
            self.accounts_df.loc[len(self.accounts_df), 'Total Outgoing'] = total_outgoing
            self.save_data()

        st.write(f'Total Outgoing: £{total_outgoing:.2f}')

        st.header('Outgoing Details')
        finance_db = FinanceDatabase()
        finance_db.connect()  # Establish the database connection
        outgoing_details = finance_db.get_outgoings()  # Fetch all the records from the "outgoings" table
        st.table(outgoing_details)
        finance_db.close()  # Close the database connection
