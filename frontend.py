# import streamlit as st
# import requests

# st.set_page_config(page_title="Airtime Lending Demo", layout="centered")

# st.title("📱 Airtime Lending Simulator")
# st.markdown("Credit scoring + Fraud detection running on Kubernetes")

# # API URL (your backend)
# API_URL = "https://airtime-lending.onrender.com"

# st.divider()

# st.subheader("Enter Customer Details")

# msisdn = st.text_input("Phone Number", "08031234567")
# col1, col2 = st.columns(2)
# with col1:
#     requested_amount = st.number_input("Requested Amount (₦)", min_value=50, max_value=10000, value=500)
#     recharge_freq = st.slider("Recharges (last 30 days)", 0, 30, 25)
# with col2:
#     sim_age_days = st.slider("SIM Age (days)", 0, 730, 400)
#     avg_recharge = st.number_input("Avg Recharge (₦)", min_value=50, value=2000)

# defaults = st.selectbox("Past Defaults", [0, 1, 2])

# if st.button("🔍 Check Loan Eligibility"):
#     payload = {
#         "msisdn": msisdn,
#         "requested_amount": requested_amount,
#         "recharge_freq": recharge_freq,
#         "sim_age_days": sim_age_days,
#         "avg_recharge": avg_recharge,
#         "defaults": defaults
#     }
    
#     try:
#         response = requests.post(f"{API_URL}/request_loan", json=payload)
#         result = response.json()
        
#         st.divider()
#         if result["status"] == "approved":
#             st.success(f"✅ APPROVED for ₦{result['loan_amount']}")
#             st.info(f"Credit Score: {result['credit_score']}")
#         else:
#             st.error(f"❌ REJECTED")
#             st.warning(f"Reason: {result['reason']}")
            
#     except Exception as e:
#         st.error(f"API Error: {e}")

# st.divider()
# st.caption("Backend running on FastAPI with a simple credit scoring model and fraud detection logic.")

import streamlit as st
import requests

st.set_page_config(page_title="Airtime Lending + USSD", layout="centered")

API_URL = "https://airtime-lending.onrender.com"

# Initialize session state
if 'mode' not in st.session_state:
    st.session_state.mode = "web"  # web or ussd
if 'ussd_step' not in st.session_state:
    st.session_state.ussd_step = 0
if 'ussd_msisdn' not in st.session_state:
    st.session_state.ussd_msisdn = "08031234567"
if 'ussd_menu' not in st.session_state:
    st.session_state.ussd_menu = 0

st.title("📱 Airtime & Data Lending")

# Mode selector
mode = st.radio("Select Interface:", ["🌐 Web Form", "📞 USSD *303#"], horizontal=True)

if mode == "🌐 Web Form":
    st.session_state.mode = "web"
    st.markdown("---")
    
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
    
    if st.button("🔍 Check Loan Eligibility", type="primary"):
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

else:  # USSD Mode
    st.session_state.mode = "ussd"
    st.markdown("---")
    
    st.code("*303#", language="text")
    
    # Phone number input for USSD
    ussd_msisdn = st.text_input("SIM Number", "08031234567", key="ussd_phone")
    st.session_state.ussd_msisdn = ussd_msisdn
    
    st.markdown("---")
    
    # USSD Menu Logic
    def reset_ussd():
        st.session_state.ussd_step = 0
    
    # Display current menu
    if st.session_state.ussd_step == 0:
        st.markdown("""
        **Welcome to Airtime Lending**
        
        1. Borrow Airtime
        2. Borrow Data
        3. Check Balance
        4. Repay Loan
        
        0. Exit
        """)
        
        choice = st.text_input("Enter option:", key="ussd_choice0", placeholder="1, 2, 3, 4, or 0")
        
        if st.button("Send", key="ussd_send0"):
            if choice == "1":
                st.session_state.ussd_step = 1
                st.rerun()
            elif choice == "2":
                st.session_state.ussd_step = 2
                st.rerun()
            elif choice == "3":
                st.session_state.ussd_step = 3
                st.rerun()
            elif choice == "0":
                st.success("Thank you for using Airtime Lending")
                reset_ussd()
            else:
                st.error("Invalid option")
    
    elif st.session_state.ussd_step == 1:
        st.markdown("**Borrow Airtime**\n\nEnter amount (₦50 - ₦5000):\n\n0. Back")
        
        amount = st.text_input("Amount:", key="ussd_amount")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Send", key="ussd_send1"):
                if amount == "0":
                    st.session_state.ussd_step = 0
                    st.rerun()
                else:
                    try:
                        amt = int(amount)
                        if 50 <= amt <= 5000:
                            payload = {
                                "msisdn": st.session_state.ussd_msisdn,
                                "requested_amount": amt,
                                "recharge_freq": 25,
                                "sim_age_days": 400,
                                "avg_recharge": 2000,
                                "defaults": 0
                            }
                            response = requests.post(f"{API_URL}/request_loan", json=payload)
                            result = response.json()
                            
                            if result["status"] == "approved":
                                st.success(f"✅ Borrowed ₦{amt} airtime successfully!")
                                st.info(f"Credit score: {result['credit_score']} | Repay in 7 days")
                            else:
                                st.error(f"❌ Failed: {result['reason']}")
                            reset_ussd()
                        else:
                            st.error("Amount must be ₦50 - ₦5000")
                    except ValueError:
                        st.error("Enter a valid number")
    
    elif st.session_state.ussd_step == 2:
        st.markdown("""
        **Borrow Data**
        
        1. 100MB - ₦50
        2. 500MB - ₦200
        3. 1GB - ₦500
        4. 2GB - ₦1000
        5. 5GB - ₦2500
        
        0. Back
        """)
        
        choice = st.text_input("Enter option:", key="ussd_data_choice")
        
        if st.button("Send", key="ussd_send2"):
            data_plans = {
                "1": {"name": "100MB", "price": 50},
                "2": {"name": "500MB", "price": 200},
                "3": {"name": "1GB", "price": 500},
                "4": {"name": "2GB", "price": 1000},
                "5": {"name": "5GB", "price": 2500}
            }
            if choice == "0":
                st.session_state.ussd_step = 0
                st.rerun()
            elif choice in data_plans:
                plan = data_plans[choice]
                payload = {
                    "msisdn": st.session_state.ussd_msisdn,
                    "requested_amount": plan["price"],
                    "recharge_freq": 25,
                    "sim_age_days": 400,
                    "avg_recharge": 2000,
                    "defaults": 0
                }
                response = requests.post(f"{API_URL}/request_loan", json=payload)
                result = response.json()
                
                if result["status"] == "approved":
                    st.success(f"✅ Borrowed {plan['name']} data successfully!")
                    st.info(f"Cost: ₦{plan['price']} | Credit score: {result['credit_score']}")
                else:
                    st.error(f"❌ Failed: {result['reason']}")
                reset_ussd()
            else:
                st.error("Invalid option")
    
    elif st.session_state.ussd_step == 3:
        st.markdown("**Your Loan Balance**\n\nLoading...")
        
        # Mock balance check
        st.info("📊 Current loan balance: ₦0")
        st.caption("No outstanding loans")
        
        if st.button("Back to Main Menu"):
            reset_ussd()
            st.rerun()
    
    # Reset button
    if st.button("🔄 Reset USSD Session"):
        reset_ussd()
        st.rerun()

st.divider()
st.caption("💰 Powered by Airtime Lending API | *303# MTN Style")