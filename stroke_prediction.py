import pickle
import pandas as pd
import streamlit as st

# Load the pipeline from the file
filename = 'RF_pipeline_.pkl'
with open(filename, "rb") as file:
    loaded_pipeline = pickle.load(file)

# Create a dictionary to map categorical features to their respective mappings
categorical_mappings = {
    'gender': {'Female': 0, 'Male': 1, 'Other': 3},
    'work_type': {'Private': 0, 'Self-employed': 1, 'Children': 2, 'Govt_job': 3, 'Never_worked': 4},
    'ever_married': {'Yes': 0, 'No': 1},
    'Residence_type': {'Urban': 0, 'Rural': 1},
    'smoking_status': {'Never smoked': 0, 'Unknown': 1, 'Formerly smoked': 2, 'Smokes': 3},
    'hypertension': {'No': 0, 'Yes': 1},
    'heart_disease': {'No': 0, 'Yes': 1}
}

# CSS styles for background
background_styles = """
    <style>
        body {
            font-family: Arial, sans-serif;
            color: #333;
            background-color: #F4F4F4;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            padding: 40px;
            background-color: #FFFFFF;
            border-radius: 10px;
            box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            margin-bottom: 40px;
        }
        .form-section {
            margin-bottom: 30px;
        }
        .form-section h3 {
            font-size: 18px;
            margin-bottom: 20px;
        }
        .form-section .input-field {
            margin-bottom: 20px;
        }
        .submit-button {
            background-color: #3366FF;
            color: #FFF;
            padding: 12px 20px;
            border-radius: 5px;
            border: none;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
        }
        .submit-button:hover {
            background-color: #3355CC;
        }
        .prediction {
            margin-top: 30px;
            font-size: 18px;
            font-weight: bold;
            text-align: center;
        }
    </style>
"""

# Create a web page using Streamlit
def main():
    # Apply CSS styles
    st.markdown(background_styles, unsafe_allow_html=True)
    st.markdown('<div style="position: absolute; top: 10px; right: 10px;">Created by- Akash Patil</div>', unsafe_allow_html=True)

    st.title("Stroke Prediction")

    # Section 1: Introduction and Information
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.write("Fill in the information and click 'Submit' to predict the possibility of a stroke.")
    st.write("Note: The dataset used for training this model is small, which may limit its accuracy and ability to make predictions in real-life scenarios.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Section 2: Input Fields
    with st.container():
        st.markdown('<div class="container form-section">', unsafe_allow_html=True)
        st.subheader("User Information")
        gender = st.selectbox("Gender", options=["Female", "Male", "Other"], key="gender")
        age = st.number_input("Age", min_value=0, max_value=100, value=30, key="age")
        hypertension = st.selectbox("Hypertension", options=["No", "Yes"], key="hypertension")
        heart_disease = st.selectbox("Heart Disease", options=["No", "Yes"], key="heart_disease")
        ever_married = st.selectbox("Ever Married", options=["Yes", "No"], key="ever_married")
        work_type = st.selectbox("Work Type", options=["Private", "Self-employed", "Children", "Govt_job", "Never_worked"], key="work_type")
        residence_type = st.selectbox("Residence Type", options=["Urban", "Rural"], key="residence_type")
        avg_glucose_level = st.number_input("Average Glucose Level", value=80, key="avg_glucose_level")
        bmi = st.number_input("BMI", min_value=0, max_value=100, value=25, key="bmi")
        smoking_status = st.selectbox("Smoking Status", options=["Never smoked", "Unknown", "Formerly smoked", "Smokes"], key="smoking_status")
        st.markdown('</div>', unsafe_allow_html=True)

    # Section 3: Prediction
    with st.container():
        st.markdown('<div class="container">', unsafe_allow_html=True)
        if st.button("Submit", key="prediction_button"):
            # Create a DataFrame for the input data
            test = pd.DataFrame({'gender': [gender], 'age': [age], 'hypertension': [hypertension],
                                 'heart_disease': [heart_disease], 'ever_married': [ever_married],
                                 'work_type': [work_type], 'Residence_type': [residence_type],
                                 'avg_glucose_level': [avg_glucose_level], 'bmi': [bmi],
                                 'smoking_status': [smoking_status]})
            
            # Map categorical features to their encoded values
            for column, mapping in categorical_mappings.items():
                if column in test.columns:
                    test[column] = test[column].map(mapping)
            
            # Check for missing values and correct data types
            if test.isnull().sum().sum() > 0:
                st.write("Error: Missing values in the input data.")
            else:
                try:
                    # Make prediction using the loaded pipeline
                    prediction = loaded_pipeline.predict(test)
                    st.markdown('<div class="prediction">Prediction: I am sorry, you may have a stroke.</div>' if prediction[0] == 1 else '<div class="prediction">Prediction: You may not have a stroke.</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.write("Error during prediction:", e)
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
