import datetime
import requests
import streamlit as st
from fake_useragent import UserAgent

st.set_page_config(layout='wide', initial_sidebar_state='collapsed')
st.title('Covid19 Vaccination Slot Availability Tracker')

left_column_1, right_column_1 = st.beta_columns(2)
with left_column_1:
    numdays = st.slider('Select next how many days you want to search for slots!', 1, 30, 5)

with right_column_1:
    pincode = int(st.number_input('Enter your PinCode', value=110001))

base = datetime.datetime.today()
date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]
date_str = [x.strftime("%d-%m-%Y") for x in date_list]

st.header("Results")
if len(str(pincode)) < 6 or len(str(pincode)) > 6:
    st.error("Please enter a valid 6 digit Pincode.")
else:
    ua = UserAgent()
    header = {'User-Agent':str(ua.chrome)}
    for INP_DATE in date_str:
        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(
            pincode, INP_DATE)
        response = requests.get(URL, headers=header)
        if response.ok:
            resp_json = response.json()
            st.subheader("Date: {}".format(INP_DATE))
            if resp_json["centers"]:
                count = 0
                itr = 0             
                for center in resp_json["centers"]:                               
                    for session in center["sessions"]:
                        if session["available_capacity"] > 0 and session["date"] == INP_DATE:
                            itr += 1
                            address_hospital = str(itr)+". **"+center["name"] + "," + center["address"] + "," + center[
                                "district_name"] + "," + center["state_name"] + "-" + str(center["pincode"])+"**"
                            st.markdown("{}".format(address_hospital))
                            st.text("Price: {}".format(center["fee_type"]))
                            st.text("Available Capacity: {}".format(session["available_capacity"]))
                            st.text("Age Group: {}+".format(session["min_age_limit"]))
                            if (session["vaccine"] != ''):
                                st.text("Vaccine: {}".format(session["vaccine"]))
                            st.text("Available Slots: {}".format(session["slots"]))
                            st.text("\n\n")
                            count += 1
                if count == 0:
                    st.text("No available slots on this day.")
    
            else:
                st.text("No available slots on this day.")
        else:
            st.text("No available slots on this day.")


#st.markdown("_- Vikrant Malik_")