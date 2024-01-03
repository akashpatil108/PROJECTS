import streamlit as st
from datetime import datetime
import pandas as pd

def extract_symbols(df, output_file, selected_date):
    selected_df = df[df['date'] == selected_date]
    
    def condition(row):
        return len(df[(df['date'] >= row['date'] - pd.DateOffset(30)) & (df['date'] < row['date']) & (df['symbol'] == row['symbol'])]) == 0

    selected_df['keep'] = selected_df.apply(condition, axis=1)
    result_df = selected_df[selected_df['keep']]

    result_df[['symbol', 'marketcapname', 'sector']].to_csv(output_file, index=False)

    return result_df

st.title("Symbol Extractor")

# File upload
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Read the uploaded file
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)

    # Date selection
    min_date = df['date'].min() if not df.empty else datetime.today()  # Use minimum date in the DataFrame or today's date
    selected_date = st.date_input("Select a date", min_value=min_date, max_value=df['date'].max() if not df.empty else datetime.today(), value=datetime.today())

    # Button to trigger extraction
    if st.button("Extract Symbols"):
        # Run the extraction script with the uploaded DataFrame
        extracted_symbols = extract_symbols(df, 'output_symbols.csv', str(selected_date))
        st.success("Symbols extracted successfully!")

        # Display the table of extracted symbols
        st.table(extracted_symbols[['symbol', 'marketcapname', 'sector']])
