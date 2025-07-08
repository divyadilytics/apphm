import streamlit as st
import pandas as pd
import os

EXCEL_FILE = "hostel_data.xlsx"

# Dummy users
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

# Inject custom CSS for top-right menu
st.markdown("""
    <style>
    .dropdown {
        position: fixed;
        top: 12px;
        right: 12px;
        display: inline-block;
    }
    .dropbtn {
        background-color: #f1f1f1;
        color: black;
        padding: 6px 12px;
        font-size: 18px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
    }
    .dropdown-content {
        display: none;
        position: absolute;
        right: 0;
        background-color: white;
        min-width: 160px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.2);
        border-radius: 8px;
        z-index: 1;
    }
    .dropdown-content button {
        color: black;
        padding: 10px 16px;
        text-align: left;
        border: none;
        background: none;
        width: 100%;
        cursor: pointer;
    }
    .dropdown-content button:hover {
        background-color: #f5f5f5;
    }
    .dropdown:hover .dropdown-content {
        display: block;
    }
    </style>
""", unsafe_allow_html=True)

# Menu HTML
st.markdown("""
    <div class="dropdown">
      <button class="dropbtn">⋮</button>
      <div class="dropdown-content">
        <form action="#" method="post">
            <button onclick="window.location.href='#settings'">Settings</button>
            <button onclick="window.location.href='#help'">Help</button>
        </form>
      </div>
    </div>
""", unsafe_allow_html=True)

# Handle anchor scroll simulation
if st.query_params.get("anchor") == "settings" or st.query_params.get("anchor") is None:
    st.subheader("⚙️ Settings")

    if st.session_state.logged_in:
        st.success("✅ Logged in!")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
    else:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if username in USERS and USERS[username] == password:
                st.session_state.logged_in = True
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials")

elif st.query_params.get("anchor") == "help":
    st.subheader("❓ Help")
    st.markdown("""
        - **Add Hostel**: Register your building  
        - **Add Room**: Assign room numbers  
        - **Add Bed**: Add people in rooms  
        - **View All**: See all hostel data  
    """)

# Only show app when logged in
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
