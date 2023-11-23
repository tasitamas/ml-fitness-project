import streamlit as st
import pandas as pd

from style import set_bg_hack_url, set_color_text, set_color_title

def streamlitShow(X_train, y_train, logistic_regression, random_forest_classifier):
    st.set_page_config(page_title="Fitness Class Attendance Prediction")

    set_bg_hack_url()
    set_color_title('white', 'Fitness Class Attendance Prediction')

    st.sidebar.header("Model Selection")
    model_choice = st.sidebar.radio("Select a Model", ("Logistic Regression", "Random Forest Classifier"))

    months_as_member = st.sidebar.number_input("Months as a member", min_value=0, max_value=150, value=10)
    weight = st.sidebar.number_input("Weight", min_value=5.0, max_value=300.0, value=75.5)
    days_before = st.sidebar.number_input("Days before attendance", min_value=0, max_value=1000, value=10)
    day_of_week = st.sidebar.selectbox("Select day of the week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    time = st.sidebar.selectbox("Select time", ["AM", "PM"])
    category = st.sidebar.selectbox("Select category", ["Aqua", "unknown", "Cycling", "HIIT", "Strength", "Yoga"])

    

    feature_values = {
        "months_as_member": months_as_member,
        "weight": weight,
        "days_before": days_before,
        "day_of_week": day_mapper(day_of_week),
        "time": 0 if time == "AM" else 1,
        "category": category_mapper(category)
    }

    if st.sidebar.button("Predict"):
        if model_choice == "Logistic Regression":
            model = logistic_regression
        else:
            model = random_forest_classifier

        # Prepare the data for prediction
        user_input_data = pd.DataFrame.from_dict(feature_values, orient="index").transpose()
        user_input_data = user_input_data.astype({"months_as_member": int, "weight": float, "days_before": int, "day_of_week": int, "time": int, "category": int})

        # Fit the model
        model.fit(X_train, y_train)

        # Prediction
        prediction = model.predict(user_input_data)

        # Prediction probabilities
        prediction_probabilities = model.predict_proba(user_input_data)

        # Display the predicted value as text
        st.markdown("<h3 style='color:white; font-size: 30px; font-weight: normal; text-align: center;'>Based on the provided features, the prediction is: </h3>", unsafe_allow_html=True)
        if prediction[0] == 1:
            set_color_text('lime', 'You are going to attend')
        else:
            set_color_text('red', 'You are not going to attend')

        st.markdown("<h3 style='color:white; font-size: 30px; font-weight: normal; text-align: center;'>Prediction Probability (0: No, 1: Yes): </h3>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color:white; font-size: 24px; font-weight: normal; text-align: center;'>0: {prediction_probabilities[0][0]:.5f}</h3>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color:white; font-size: 24px; font-weight: normal; text-align: center;'>1: {prediction_probabilities[0][1]:.5f}</h3>", unsafe_allow_html=True)

def day_mapper(day_of_week):
    if day_of_week == "Monday":
        return 0
    elif day_of_week == "Tuesday":
        return 1
    elif day_of_week == "Wednesday":
        return 2
    elif day_of_week == "Thursday":
        return 3
    elif day_of_week == "Friday":
        return 4
    elif day_of_week == "Saturday":
        return 5
    else:
        return 6
    
def category_mapper(category):
    if category == "Aqua":
        return 0
    elif category == "unknown":
        return 1
    elif category == "Cycling":
        return 2
    elif category == "HIIT":
        return 3
    elif category == "Strength":
        return 4
    else:
        return 5