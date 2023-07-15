import pickle
import pandas as pd
import streamlit as st

# Load the pipeline from the file
filename = "RF_pipeline_.pkl"
with open(filename, "rb") as file:
    loaded_pipeline = pickle.load(file)

# Create a dictionary to map categorical features to their respective mappings
categorical_mappings = {
    'gender': {'Female': 0, 'Male': 1, 'Other': 3},
    'work_type': {'Private': 0, 'Self-employed': 1, 'Children': 3, 'Govt_job': 4, 'Never_worked': 5},
    'ever_married': {'Yes': 0, 'No': 1},
    'Residence_type': {'Urban': 0, 'Rural': 1},
    'smoking_status': {'Never smoked': 0, 'Unknown': 1, 'Formerly smoked': 3, 'Smokes': 4},
    'hypertension': {'No':0, 'Yes':1},
    'heart_disease': {'No':0, 'Yes':1}
}

# Create a web page using Streamlit
def main():
    st.title("Stroke Prediction")
    st.write("Fill in the information and click 'Submit' to predict the possibility of a stroke.")

    # Create input fields for each column
    gender = st.selectbox("Gender", options=["Female", "Male", "Other"])
    age = st.number_input("Age", min_value=0, max_value=100, value=30)
    hypertension = st.selectbox("Hypertension", options=["No", "Yes"])
    heart_disease = st.selectbox("Heart Disease", options=["No", "Yes"])
    ever_married = st.selectbox("Ever Married", options=["Yes", "No"])
    work_type = st.selectbox("Work Type", options=["Private", "Self-employed", "Children", "Govt_job", "Never_worked"])
    residence_type = st.selectbox("Residence Type", options=["Urban", "Rural"])
    avg_glucose_level = st.number_input("Average Glucose Level", value=80)
    bmi = st.number_input("BMI",min_value=0, max_value=100, value=25)
    smoking_status = st.selectbox("Smoking Status", options=["Never smoked", "Unknown", "Formerly smoked", "Smokes"])

    # Handle the submission
    if st.button("Submit"):
        test = pd.DataFrame({'gender': [gender], 'age': [age], 'hypertension': [hypertension],
                             'heart_disease': [heart_disease], 'ever_married': [ever_married],
                             'work_type': [work_type], 'Residence_type': [residence_type],
                             'avg_glucose_level': [avg_glucose_level], 'bmi': [bmi],
                             'smoking_status': [smoking_status]})

        # Map categorical features to their encoded values
        for column, mapping in categorical_mappings.items():
            test[column] = test[column].map(mapping)

        # Make prediction using the loaded pipeline
        prediction = loaded_pipeline.predict(test)

        # Show the prediction
        st.markdown('<div class="prediction">Prediction: Im sorry, You may have a stroke.</div>' if prediction[0] == 1 else '<div class="prediction">Prediction:  You may not have a stroke.</div>',unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
