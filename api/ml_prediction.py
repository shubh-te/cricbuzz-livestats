import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression

# Dummy historical dataset mapping team strengths (e.g., 1-100) to chance of winning (1=Team1, 0=Team2)
def load_ml_model():
    # Training Data
    X_train = np.array([
        [90, 85], [80, 85], [95, 80], [70, 75],
        [85, 90], [80, 70], [88, 88], [92, 85]
    ])
    y_train = np.array([1, 0, 1, 0, 0, 1, 1, 1]) # 1 if Team 1 wins, 0 otherwise
    
    model = LogisticRegression()
    model.fit(X_train, y_train)
    return model

@st.cache_resource
def get_prediction_model():
    return load_ml_model()

def render_ml_page():
    st.title("🤖 ML Predictor - Match Outcome")
    st.write("Predict the outcome of an upcoming match by assessing team strengths (Pitch factor, Recent Form, Overall Team Rating)")
    
    model = get_prediction_model()
    
    col1, col2 = st.columns(2)
    with col1:
        team_1 = st.text_input("Team 1 Name", "India")
        team_1_strength = st.slider(f"{team_1} Overall Strength", 1, 100, 85)
    with col2:
        team_2 = st.text_input("Team 2 Name", "Australia")
        team_2_strength = st.slider(f"{team_2} Overall Strength", 1, 100, 80)
        
    if st.button("🔮 Predict Outcome"):
        prediction = model.predict([[team_1_strength, team_2_strength]])
        prob = model.predict_proba([[team_1_strength, team_2_strength]])
        
        if prediction[0] == 1:
            st.success(f"{team_1} is more likely to win! (Probability: {prob[0][1]*100:.1f}%)")
        else:
            st.success(f"{team_2} is more likely to win! (Probability: {prob[0][0]*100:.1f}%)")
        
        st.info("Note: Prediction model uses experimental historical weighting algorithms.")
