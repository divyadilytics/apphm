import streamlit as st

# Initialize session state
if 'hostels' not in st.session_state:
    st.session_state.hostels = {}

st.title("🏨 Hostel Manager App")

menu = st.sidebar.radio("Menu", ["Add Hostel", "Add Room", "Add Bed", "View All"])


# Add a hostel
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

# Add a room
elif menu == "Add Room":
    st.header("🛏️ Add Room to a Hostel")
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
                    st.warning("⚠️ Room already exists in this hostel.")
            else:
                st.error("❌ Please enter a room number.")
    else:
        st.info("ℹ️ No hostels available. Add a hostel first.")

# Add a bed
elif menu == "Add Bed":
    st.header("🛌 Add Bed (Person Info) to a Room")
    hostel_list = list(st.session_state.hostels.keys())

    if hostel_list:
        hostel = st.selectbox("Select Hostel", hostel_list)
        room_list = list(st.session_state.hostels[hostel].keys())

        if room_list:
            room = st.selectbox("Select Room", room_list)
            occupant_name = st.text_input("Occupant Name")
            contact = st.text_input("Contact Number")
            fee_paid = st.checkbox("Fee Paid?")

            if st.button("Add Bed (Occupant)"):
                if occupant_name:
                    person = {
                        "name": occupant_name,
                        "contact": contact,
                        "fee_paid": fee_paid
                    }
                    st.session_state.hostels[hostel][room].append(person)
                    st.success(f"✅ Occupant '{occupant_name}' added to {room} in {hostel}.")
                else:
                    st.error("❌ Enter occupant name.")
        else:
            st.info("ℹ️ No rooms in selected hostel. Add a room first.")
    else:
        st.info("ℹ️ No hostels available. Add a hostel first.")

# View all data
elif menu == "View All":
    st.header("📋 View All Hostel Data")
    if st.session_state.hostels:
        for hostel, rooms in st.session_state.hostels.items():
            st.subheader(f"🏠 {hostel}")
            if rooms:
                for room, beds in rooms.items():
                    st.markdown(f"### Room {room}")
                    if beds:
                        for i, bed in enumerate(beds, 1):
                            st.markdown(
                                f"**Bed {i}**: {bed['name']} | 📞 {bed['contact']} | 💰 {'Paid' if bed['fee_paid'] else 'Unpaid'}"
                            )
                    else:
                        st.write("No occupants in this room.")
            else:
                st.write("No rooms in this hostel.")
    else:
        st.info("No data available. Start by adding hostels and rooms.")

