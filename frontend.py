import streamlit as st
import requests

st.set_page_config(page_title="Airtime Lending Demo", layout="centered")

st.title("📱 Airtime Lending Simulator")
st.markdown("Credit scoring + Fraud detection running on Kubernetes")

# API URL (your backend)
API_URL = "https://airtime-lending.onrender.com"

st.divider()

st.subheader("Enter Customer Details")

msisdn = st.text_input("Phone Number", "08031234567")
col1, col2 = st.columns(2)
with col1:
    requested_amount = st.number_input("Requested Amount (₦)", min_value=50, max_value=10000, value=500)
    recharge_freq = st.slider("Recharges (last 30 days)", 0, 30, 25)
with col2:
    sim_age_days = st.slider("SIM Age (days)", 0, 730, 400)
    avg_recharge = st.number_input("Avg Recharge (₦)", min_value=50, value=2000)

defaults = st.selectbox("Past Defaults", [0, 1, 2])

if st.button("🔍 Check Loan Eligibility"):
    payload = {
        "msisdn": msisdn,
        "requested_amount": requested_amount,
        "recharge_freq": recharge_freq,
        "sim_age_days": sim_age_days,
        "avg_recharge": avg_recharge,
        "defaults": defaults
    }
    
    try:
        response = requests.post(f"{API_URL}/request_loan", json=payload)
        result = response.json()
        
        st.divider()
        if result["status"] == "approved":
            st.success(f"✅ APPROVED for ₦{result['loan_amount']}")
            st.info(f"Credit Score: {result['credit_score']}")
        else:
            st.error(f"❌ REJECTED")
            st.warning(f"Reason: {result['reason']}")
            
    except Exception as e:
        st.error(f"API Error: {e}")

st.divider()
st.caption("Backend running on FastAPI with a simple credit scoring model and fraud detection logic.")