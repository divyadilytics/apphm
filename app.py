import streamlit as st
import pandas as pd
import os

# Excel file to store hostel data
EXCEL_FILE = "hostel_data.xlsx"

# Dummy login credentials (username: password)
USERS = {
    "admin": "1234",
    "manager": "abcd"
}

# Load existing data or create a new empty DataFrame
def load_data():
    if os.path.exists(EXCEL_FILE):
        return pd.read_excel(EXCEL_FILE)
    else:
        return pd.DataFrame(columns=["Hostel", "Room", "Occupant", "Contact", "Fee Paid"])

# Save updated data to Excel
def save_data(df):
    df.to_excel(EXCEL_FILE, index=False)

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "df" not in st.session_state:
    st.session_state.df = load_data()

# Login screen
def login():
    st.title("🔐 Bot Login")
    username = st.text_input("Username").strip()
    password = st.text_input("Password", type="password").strip()

    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.success("✅ Login successful!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

# Logout function
def logout():
    st.session_state.logged_in = False
    st.rerun()

# Main app logic
def hostel_manager_app():
    st.title("🏨 Hostel Manager")
    st.sidebar.success("✅ Logged in")
    st.sidebar.button("Logout", on_click=logout)

    menu = st.sidebar.radio("Menu", ["Add Hostel", "Add Room", "Add Bed", "View All"])

    # Initialize in-memory hostel structure from Excel if not already set
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

    # Add Hostel
    if menu == "Add Hostel":
        st.header("➕ Add Hostel")
        hostel_name = st.text_input("Hostel Name")
        if st.button("Add Hostel"):
            if hostel_name:
                if hostel_name not in st.session_state.hostels:
                    st.session_state.hostels[hostel_name] = {}
                    st.success(f"✅ Hostel '{hostel_name}' added.")
                else:
                    st.warning("⚠️ Hostel already exists.")
            else:
                st.error("❌ Please enter a hostel name.")

    # Add Room
    elif menu == "Add Room":
        st.header("🛏️ Add Room to Hostel")
        hostel_list = list(st.session_state.hostels.keys())
        if hostel_list:
            hostel = st.selectbox("Select Hostel", hostel_list)
            room_number = st.text_input("Room Number")
            if st.button("Add Room"):
                if room_number:
                    if room_number not in st.session_state.hostels[hostel]:
                        st.session_state.hostels[hostel][room_number] = []
                        st.success(f"✅ Room '{room_number}' added to {hostel}.")
                    else:
                        st.warning("⚠️ Room already exists.")
                else:
                    st.error("❌ Please enter a room number.")
        else:
            st.info("ℹ️ No hostels available. Add a hostel first.")

    # Add Bed (Occupant)
    elif menu == "Add Bed":
        st.header("🛌 Add Bed (Occupant) to Room")
        hostel_list = list(st.session_state.hostels.keys())
        if hostel_list:
            hostel = st.selectbox("Select Hostel", hostel_list)
            room_list = list(st.session_state.hostels[hostel].keys())
            if room_list:
                room = st.selectbox("Select Room", room_list)
                occupant_name = st.text_input("Occupant Name")
                contact = st.text_input("Contact Number")
                fee_paid = st.checkbox("Fee Paid?")

                if st.button("Add Bed"):
                    if occupant_name:
                        person = {
                            "name": occupant_name,
                            "contact": contact,
                            "fee_paid": fee_paid
                        }
                        st.session_state.hostels[hostel][room].append(person)

                        # Add to Excel
                        new_row = {
                            "Hostel": hostel,
                            "Room": room,
                            "Occupant": occupant_name,
                            "Contact": contact,
                            "Fee Paid": fee_paid
                        }
                        st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_row])], ignore_index=True)
                        save_data(st.session_state.df)

                        st.success(f"✅ Occupant '{occupant_name}' added to Room {room} in {hostel}.")
                    else:
                        st.error("❌ Please enter occupant name.")
            else:
                st.info("ℹ️ No rooms found in selected hostel. Add a room first.")
        else:
            st.info("ℹ️ No hostels found. Add a hostel first.")

    # View All Data
    elif menu == "View All":
        st.header("📋 View All Hostel Data")
        if not st.session_state.df.empty:
            st.dataframe(st.session_state.df)
        else:
            st.info("No data available yet.")

# Run the app
if st.session_state.logged_in:
    hostel_manager_app()
else:
    login()
