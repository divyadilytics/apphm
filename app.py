import streamlit as st
import pandas as pd
import os

EXCEL_FILE = "hostel_data.xlsx"
USERS = {"admin": "1234", "manager": "abcd"}

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

# Add custom top-right menu
st.markdown("""
    <style>
    .menu-container {
        position: fixed;
        top: 12px;
        right: 12px;
        z-index: 9999;
    }

    .menu-button {
        font-size: 24px;
        background: #f0f0f0;
        border: none;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        cursor: pointer;
    }

    .dropdown {
        display: none;
        position: absolute;
        right: 0;
        top: 45px;
        background-color: white;
        min-width: 150px;
        border: 1px solid #ccc;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    .dropdown button {
        background: none;
        border: none;
        color: black;
        padding: 10px 16px;
        width: 100%;
        text-align: left;
        cursor: pointer;
        font-size: 14px;
    }

    .dropdown button:hover {
        background-color: #f1f1f1;
    }

    .menu-container:hover .dropdown {
        display: block;
    }
    </style>

    <div class="menu-container">
        <button class="menu-button">⋮</button>
        <div class="dropdown">
            <form action="" method="get">
                <button name="section" value="settings">⚙️ Settings</button>
                <button name="section" value="help">❓ Help</button>
            </form>
        </div>
    </div>
""", unsafe_allow_html=True)

# Get current section
section = st.query_params.get("section", "settings")

# Settings/Login Page
if section == "settings":
    st.subheader("⚙️ Settings")
    if st.session_state.logged_in:
        st.success("✅ Logged in!")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
    else:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username in USERS and USERS[username] == password:
                st.session_state.logged_in = True
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")

# Help Page
elif section == "help":
    st.subheader("❓ Help")
    st.markdown("""
    **Hostel Manager Instructions:**
    - Add Hostels to register buildings
    - Add Rooms under a Hostel
    - Add Bed to assign occupants
    - View All shows the full data
    """)

# Main App Only If Logged In
if st.session_state.logged_in:
    menu = st.sidebar.radio("Menu", ["Add Hostel", "Add Room", "Add Bed", "View All"])
    st.markdown("<h2 style='margin-top: -20px;'>🏨 Hostel Manager</h2>", unsafe_allow_html=True)

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

    if menu == "Add Hostel":
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

    elif menu == "Add Room":
        hostel_list = list(st.session_state.hostels.keys())
        if hostel_list:
            hostel = st.selectbox("Select Hostel", hostel_list)
            room_number = st.text_input("Room Number")
            if st.button("Add Room"):
                if room_number:
                    if room_number not in st.session_state.hostels[hostel]:
                        st.session_state.hostels[hostel][room_number] = []
                        st.success(f"✅ Room '{room_number}' added.")
                    else:
                        st.warning("⚠️ Room already exists.")
                else:
                    st.error("❌ Please enter a room number.")
        else:
            st.info("ℹ️ Add a hostel first.")

    elif menu == "Add Bed":
        hostel_list = list(st.session_state.hostels.keys())
        if hostel_list:
            hostel = st.selectbox("Select Hostel", hostel_list)
            room_list = list(st.session_state.hostels[hostel].keys())
            if room_list:
                room = st.selectbox("Select Room", room_list)
                name = st.text_input("Occupant Name")
                contact = st.text_input("Contact Number")
                fee_paid = st.checkbox("Fee Paid?")
                if st.button("Add Bed"):
                    if name:
                        person = {"name": name, "contact": contact, "fee_paid": fee_paid}
                        st.session_state.hostels[hostel][room].append(person)
                        new_row = {
                            "Hostel": hostel,
                            "Room": room,
                            "Occupant": name,
                            "Contact": contact,
                            "Fee Paid": fee_paid
                        }
                        st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_row])], ignore_index=True)
                        save_data(st.session_state.df)
                        st.success(f"✅ Added {name} to {room} in {hostel}")
                    else:
                        st.error("❌ Enter name")
            else:
                st.info("ℹ️ Add rooms first.")
        else:
            st.info("ℹ️ Add hostels first.")

    elif menu == "View All":
        if not st.session_state.df.empty:
            st.dataframe(st.session_state.df)
        else:
            st.info("📭 No data yet.")
