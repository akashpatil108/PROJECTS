import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Page Title and Description
st.title("Data Filtering App")
st.write("This app allows users to filter data based on selected criteria.")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

# User Input Section
if uploaded_file is not None:
    st.header("Select Filtering Criteria")

    # End date selection
    e_date = st.date_input("Select End Date", pd.to_datetime(datetime.today()))
    end_date = pd.to_datetime(e_date)


    # Period selection
    period = st.number_input("Select Period (in days)", min_value=1, value=30)

    # Confirmation button
    confirmation_button = st.button("Confirm Selection")

    if confirmation_button:
        try:
            # Read and preprocess the data
            df = pd.read_csv(uploaded_file)
            df["date"] = pd.to_datetime(df["date"])

            # Calculate start date based on period
            start_date = end_date - timedelta(days=period)

            # Filter data based on date range
            filtered_df = df[df["date"] >= start_date]

            # Perform additional calculations
            value_count = filtered_df['symbol'].value_counts()
            count_values = value_count.to_dict()
            filtered_df['count'] = filtered_df['symbol'].map(count_values)

            # Display filtered data
            st.subheader("Original Data")
            st.dataframe(df)

            # Filter based on user-selected end date and count
            filter_date = filtered_df['date'].max()
            final_df = filtered_df[(filtered_df["count"] == 1) & (filtered_df["date"] == filter_date)]

            # Display the final results
            if not final_df.empty:
                st.subheader("Final Results")
                st.dataframe(final_df)
            else:
                st.warning("No data found for the selected criteria.")

        except Exception as e:
            st.error(f"An error occurred: {e}")

# Provide instructions for usage
st.markdown("### How to Use:")
st.write("1. Upload a CSV file.")
st.write("2. Select the end date and period.")
st.write("3. Click the 'Confirm Selection' button.")
