import streamlit as st
import pandas as pd
from connection import FinanceDatabase

class GoalsPage:
    def __init__(self):
        pass

    def main(self,user_id):
        st.title('Goals')

        