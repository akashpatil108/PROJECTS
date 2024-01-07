import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.sidebar.header("User Input")

# File uploader
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

# End date selection
e_date = st.sidebar.date_input("Select End Date")
end_date = pd.to_datetime(e_date)

# Period selection
period = st.sidebar.number_input("Select Period (in days)", min_value=1, value=30)



# Confirmation button
confirmation_button = st.sidebar.button("Confirm Selection")

if confirmation_button:
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        # Convert date column to datetime
        df["date"] = pd.to_datetime(df["date"])

        # Calculate start date based on period
        start_date = end_date - timedelta(days=period)

        # Filter data based on date range
        filtered_df = df[df["date"] >= start_date]

        # Perform additional calculations (as in your original code)
        value_count = filtered_df['symbol'].value_counts()
        count_values = value_count.to_dict()
        filtered_df['count'] = filtered_df['symbol'].map(count_values)

        # Display filtered data
        st.dataframe(filtered_df)
        # Assuming 'date' column is in datetime format
        filtered_df['date'] = pd.to_datetime(filtered_df['date'])
        # Filter date selection
        filter_date =filtered_df['date'].max()

        # Apply the filter based on user-selected end date and count
        filtered_df = filtered_df[(filtered_df["count"] == 1) & (filtered_df["date"] == filter_date)]

        # Display the filtered DataFrame
        if not filtered_df.empty:
            st.dataframe(filtered_df)
        else:
            st.warning("No data found for the selected criteria.")
