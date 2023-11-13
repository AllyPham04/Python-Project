import streamlit as st
import os
import pandas as pd
from config import *
from datetime import datetime

def app():
    col_a1, col_a2, col_a3 = st.columns([1, 1, 2])
    col_b1, col_b2 = st.columns(2)
    now = datetime.now()

    total_balance = 0
    total_income = 0
    total_expense = 0

    with col_b1:
        with st.form("add_transaction", clear_on_submit=True):
            st.subheader("Transaction")
            type = st.radio("Type:",
                            ["Income", "Expense"])
            selected_date = st.date_input("Select date:", value=datetime.today(), format="DD/MM/YYYY")
            amount = st.number_input(f"Amount:", min_value=0, format="%i", step=10, key="amount_input")
            if type == "Income":
                category = st.selectbox("Category:", incomes)
            elif type == "Expense":
                category = st.selectbox("Category:", expenses)
            if st.form_submit_button("Save Data"):
                # Gather user inputs
                user_data = {
                    'Type': 'Income' if type == "Income" else 'Expense',
                    'Date': selected_date.strftime("%d-%m-%Y"),
                    'Category': category,
                    'Amount': amount
                }
                        
                try:
                    df = pd.read_csv('data.csv')
                except (FileNotFoundError, pd.errors.EmptyDataError):
                    df = pd.DataFrame(columns=user_data.keys())
                        
                df = pd.concat([df, pd.DataFrame(user_data, index=[0])], ignore_index=True)
                df = df.sort_values(by=['Date'], ascending=False)
                df.to_csv('data.csv', index=False, date_format='%H:%M:%S')

                st.write(f"{category}: {amount} {currency}")
                st.success("Data saved!")
                
    with col_a1:
        if os.path.exists('data.csv'):
            df = pd.read_csv('data.csv')
            total_income = df[df['Type'] == 'Income']['Amount'].sum()
            total_expense = df[df['Type'] == 'Expense']['Amount'].sum()
            total_balance = total_income - total_expense
        else:
            total_balance = 0
        st.metric("Total Credits", f"{total_balance} {currency}")

    with col_b2:
        with st.form("transactions_history", clear_on_submit=True):
            st.subheader("History")
            if os.path.exists('data.csv'):
                df = pd.read_csv('data.csv')
            else:
                df = pd.DataFrame()

            if not df.empty:
                df.index = df.index + 1
                df['Amount'] = df.apply(lambda row: f'+ {row["Amount"]} {currency}' 
                                        if row['Type'] == 'Income' 
                                        else f'- {row["Amount"]} {currency}', axis=1)
                st.table(df.drop(columns=['Type']))

            if st.form_submit_button("Clear all data"):
                st.session_state.clear()
                if os.path.exists('data.csv'):
                    os.remove('data.csv')
                    st.success("Data cleared!")
                user_income.clear()
                user_expense.clear()