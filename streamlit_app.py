import streamlit as st
import requests
import pandas as pd
st.set_page_config(page_title="Credit Risk Predictor", layout="wide")
st.title("📊 AI Credit Risk Assessment")

with st.form("credit_form"):
    st.header("Applicant Information")
    col1, col2 = st.columns(2)
    
    with col1:
        income = st.number_input("Annual Income ($)", min_value=0, step=5000)
        loan_amount = st.number_input("Loan Amount ($)", min_value=0, step=1000)
        credit_score = st.slider("Credit Score", 300, 850, 650)
        
    with col2:
        employment = st.selectbox("Employment Status", 
                                ["Employed", "Self-Employed", "Unemployed"])
        debt_ratio = st.number_input("Debt-to-Income Ratio", min_value=0.0, max_value=1.0, step=0.01)
        dependents = st.number_input("Dependents", min_value=0, step=1)

    submitted = st.form_submit_button("Predict Risk")


# Prediction handler
if submitted:
    payload = {
        "features": [
            income,
            loan_amount,
            credit_score,
            1 if employment == "Employed" else 0,
            debt_ratio,
            dependents
        ]
    }

 try:
        response = requests.post("http://localhost:5000/predict", json=payload)
        result = response.json()
        
        st.subheader("Risk Assessment Result")
        if result["prediction"] == 0:
            st.success("✅ Low Risk (Approval Recommended)")
        else:
            st.error("❌ High Risk (Approval Not Recommended)")
            
        st.metric("Confidence Level", f"{result['probability']:.2%}")
  except Exception as e:
        st.error(f"🚨 Prediction failed: {str(e)}")



# Add footer
st.markdown("---")
st.caption("AI-powered credit risk assessment system • Model v2.1")
