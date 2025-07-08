import streamlit as st
import pandas as pd
import os

EXCEL_FILE = "hostel_data.xlsx"

USERS = {
    "admin": "1234",
    "manager": "abcd"
}

def load_data():
    if os.path.exists(EXCEL_FILE):
        return pd.read_excel(EXCEL_FILE)
    else:
        return pd.DataFrame(columns=["Hostel", "Room", "Occupant", "Contact", "Fee Paid"])

def save_data(df):
    df.to_excel(EXCEL_FILE, index=False)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "df" not in st.session_state:
    st.session_state.df = load_data()

# Three-dot menu
def top_menu():
    cols = st.columns([10, 1])
    with cols[1]:
        with st.expander("⋮"):
            choice = st.radio("Options", ["Settings", "Help"])

            if choice == "Settings":
                if st.session_state.logged_in:
                    if st.button("Logout"):
                        st.session_state.logged_in = False
                        st.rerun()
                else:
                    username = st.text_input("Username").strip()
                    password = st.text_input("Password", type="password").strip()
                    if st.button("Login"):
                        if username in USERS and USERS[username] == password:
                            st.session_state.logged_in = True
                            st.success("✅ Login successful!")
                            st.rerun()
                        else:
                            st.error("❌ Invalid username or password")

            elif choice == "Help":
                st.markdown("""
                - **Add Hostel**: Register a new building  
                - **Add Room**: Add room numbers to a hostel  
                - **Add Bed**: Assign people to rooms with fee info  
                - **View All**: See all hostel, room, and bed data  
                """, unsafe_allow_html=True)

# Main interface
def hostel_manager_app():
    st.set_page_config(page_title="Hostel Manager", layout="wide")
    top_menu()

    st.title("🏨 Hostel Manager")
    menu = st.sidebar.radio("Menu", ["Add Hostel", "Add Room", "Add Bed", "View All"])

    if "hostels" not in st.session_state:
        st.session_state.hostels = {}
        for _, row in st.session_state.df.iterrows():
            h = row["Hostel"]
            r = row["Room"]
            st.session_state.hostels.setdefault(h, {}).setdefault(r, []).append({
                "name": row["Occupant"],
                "contact": row["Contact"],
                "fee_paid": row["Fee Paid"]
            })

    # --- (keep your Add Hostel, Add Room, Add Bed, View All logic unchanged) ---
    ...
    # Paste your full internal app logic here exactly as it was

# Run the interface
hostel_manager_app()
