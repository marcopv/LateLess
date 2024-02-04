import os
import string
import joblib
import sklearn
import numpy as np
import pandas as pd
import streamlit as st
from pathlib import Path
import streamlit.components.v1 as components
from streamlit_extras.no_default_selectbox import selectbox
from streamlit_folium import st_folium
import folium.features
import requests
import folium
import base64
from pathlib import Path

# set page info
st.set_page_config(
    page_title="US airlines delays App",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# import dataset
dataset = Path(__file__).parent / "../data/examples.csv"
df = pd.read_csv(dataset)

# import model
filename = Path(__file__).parent /  '../models/VotingClassifier.sav'
model =  joblib.load(open(filename, 'rb'))

# import inverse dictionary
path = Path(__file__).parent / '../models/inverse.sav'
inverse_dictionary =  joblib.load(open(path, 'rb'))

### Code To Plot The Map
state = Path(__file__).parent / "../map/airportsall.csv"
STATE_DATA = pd.read_csv(state)

# set title
st.title('⏳Welcome to USA Airlines Delays Prediction⌛')
st.caption('\n_Your airlines delays app accessibile everywhere to make\
                prediction on flight delays!_')

@st.cache_data
def _get_all_state_bounds() -> dict:
    url = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"
    data = requests.get(url).json()
    return data

@st.cache_data
def get_state_bounds(state: str) -> dict:
    data = _get_all_state_bounds()

    state_entry = [f for f in data["features"] if f["properties"]["name"] == state]
    return {"type": "FeatureCollection", "features": [state_entry]}

def get_state_from_lat_lon(lat: float, lon: float) -> str:
    state_row = STATE_DATA[
        STATE_DATA.latitude.between(lat - 0.0001, lat + 0.0001)
        & STATE_DATA.longitude.between(lon - 0.0001, lon + 0.0001)
    ].iloc[0]
    return state_row["state"]

def map_plot():
    if "last_object_clicked" not in st.session_state:
        st.session_state["last_object_clicked"] = None
        st.session_state["selected_airport"] = None
    if "selected_state" not in st.session_state:
        st.session_state["selected_state"] = ""
        st.session_state["selected_airport_iata"] = ""
        st.session_state["selected_airport_name"] = ""

    bounds = get_state_bounds(st.session_state["selected_state"])


    center = None
    m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)

    # If you want to dynamically add or remove items from the map,
    # add them to a FeatureGroup and pass it to st_folium
    fg = folium.FeatureGroup(name="State bounds")
    fg.add_child(folium.features.GeoJson(bounds))


    # Plot the color in the Map
    url = (
        "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data"
    )
    state_geo = f"{url}/us-states.json"
    state_unemployment = f"{url}/US_Unemployment_Oct2012.csv"
    state_data = pd.read_csv(state_unemployment)

    choropleth = folium.Choropleth(
        geo_data=state_geo,
        name="choropleth",
        data=state_data,
        columns=["State", "Unemployment"],
        key_on="feature.id",
        fill_color="YlGn",
        fill_opacity=0.7,
        line_opacity=0.2,

    )
    for key in choropleth._children:
        if key.startswith('color_map'):
            del(choropleth._children[key])

    choropleth.add_to(m)

    capitals = STATE_DATA

    for capital in capitals.itertuples():
        fg.add_child(
            folium.Marker(
                location=[capital.latitude, capital.longitude],
                popup=f"{capital.airport}, {capital.iata}",
                tooltip=f"{capital.capital}, {capital.airport}",
                icon=folium.Icon(color="green",icon='plane', prefix='fa')
                if capital.state == st.session_state["selected_state"]
                else folium.Icon(color="blue",icon='plane', prefix='fa'),
            )
        )

    out = st_folium(
        m,
        feature_group_to_add=fg,
        center=center,
        width=940,
        height=420,
    )

    if (
        out["last_object_clicked"]
        and out["last_object_clicked"] != st.session_state["last_object_clicked"]
    ):
        st.session_state["last_object_clicked"] = out["last_object_clicked"]
        state = get_state_from_lat_lon(*out["last_object_clicked"].values())
        st.session_state["selected_state"] = state

        for capital in capitals.itertuples():
            if capital.state == st.session_state["selected_state"]:
                st.session_state["selected_airport_iata"] = capital.iata
                st.session_state["selected_airport_name"] = capital.airport

        st.rerun()

    # if st.session_state['selected_airport_name'] == "":
    #     pass
    # else:
    #     st.write(f"### Airport name: {st.session_state['selected_airport_name']}")
    #     st.write(f"#### Airport Code: {st.session_state['selected_airport_iata']}")

    return st.session_state['selected_airport_iata']

def departure_period(time):
  if ((time/60 >= 5) & (time/60 < 12)):      
      return 0
  elif ((time/60 >= 12) & (time/60 < 17)):    
      return 1
  elif ((time/60 >= 17) & (time/60 < 21)): 
      return 2
  else: 
      return 3

def holiday(dayofweek):
  if ((dayofweek == 6) | (dayofweek == 7)):      
      return 1
  else: 
      return 0

def arrival_time(time, length):
  if (time/60 + length/60 >= 24):
    return time/60 + length/60 - 24
  else:
    return time/60 + length/60 

def arrival_period(arrival_time):
    if ((arrival_time >= 5) & (arrival_time < 12)):      
        return 0
    elif ((arrival_time >= 12) & (arrival_time < 17)):    
        return 1
    elif ((arrival_time >= 17) & (arrival_time < 21)): 
        return 2
    else: 
        return 3

def air2num(inverse_dictionary, airl, airfrom,airto):
  return inverse_dictionary['airlines'][airl], inverse_dictionary['airportfrom'][airfrom], inverse_dictionary['airportto'][airto]


# init state variables
pred = -1
iata = None


# read and apply css
style = ""
css_path = Path(__file__).parent / "../style/style.txt"

with open(css_path, "r") as fstyle:
  style = fstyle.read()

st.markdown(style, unsafe_allow_html=True)

# set page background
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True)

add_bg_from_local(Path(__file__).parent / "../style/dddepth-308.jpg")

#create columns under the title that will contain graphic elements
t_col1, t_col2  = st.columns([0.45, 1])

col1, col2, col3 = st.columns([0.20,0.20, 1] ,  gap='Large')

with col1:
    st.markdown("""**Airline**<br>
    <p class="cbox">**Flight**</p>
    <p class="cbox">**From**</p>
    <p class="cbox">**To**</p>
    <p class="cbox">**Day of Week**</p>
    <p class="cbox">**Departure (hr)**</p>
    <p class="cbox">**Flight Duration (hr)**</p>"""
    , unsafe_allow_html=True )

    st.markdown("<br>", unsafe_allow_html=True )

    go = st.button('Take off!')

with col2:
    Airline = selectbox('Airline', df['Airline'].tolist(), label_visibility = 'collapsed')
    Flight = selectbox('Flight Code', df['Flight'].tolist(), label_visibility = 'collapsed')
    AirportFrom = selectbox('From', df['AirportFrom'].tolist(), label_visibility = 'collapsed')
    AirportTo = selectbox('To', df['AirportTo'].tolist(), label_visibility = 'collapsed')
    DayOfWeek = selectbox('Day of week', df['DayOfWeek'].tolist(), label_visibility = 'collapsed') # change in date selector and automagically get dow
    Time = selectbox('Departure (hr)', df['Time'].tolist(), label_visibility = 'collapsed')
    Length = selectbox('Flight Duration (hr)', df['Length'].tolist(), label_visibility = 'collapsed')

    if go:   
        if not (Airline is None or
        Flight is None or
        AirportFrom is None or
        AirportTo is None or
        DayOfWeek is None or
        Time is None or
        Length is None):

            airl, airfrom, airto = air2num(inverse_dictionary, Airline, AirportFrom, AirportTo)
            length_by_hours = int(Length) # int(Length)/60
            time_by_hour = int(Time) # int(Time)/60
            arrival_t = arrival_time(int(Time), int(Length))
            arrival_p = arrival_period(arrival_t)
            departure_p = departure_period(int(Time))
            hol = holiday(int(DayOfWeek))

            # [Airline, Flight, AirportFrom, AirportTo, DayOfWeek, Length_by_hours, time_by_hour, departure_period, holiday, arrival_time, arrival_period]
            data = {'Airline': airl,             
                    'Flight': int(Flight),             
                    'AirportFrom': airfrom,          
                    'AirportTo': airto,            
                    'DayOfWeek': int(DayOfWeek),
                    'Length_by_hours': length_by_hours,      
                    'Time_by_hour': time_by_hour,         
                    'Departure_period' :departure_p,     
                    'Holiday' :hol,              
                    'Arrival_Time' :arrival_t,         
                    'Arrival_period' :arrival_p}

            ser = pd.DataFrame(data=data, index=[0])
            # model = torch.hub.load()        
            pred = model.predict(ser)[0]
        else:
            pred = 10

with col3:
    iata = map_plot()

with t_col1:
    st.header("Insert :blue[_flight_] to check")

with t_col2:
    if pred not in [0,1]:
        st.header('Press The Button! To make a prediction')
    else:
        if pred:
            # st.header('Prediction: :red[Your flight will arrive late!]')   
            st.error('### :red[Your flight will arrive late!]')         
        else:
            # st.header('Prediction: :green[Your flight will arrive on time!]')    
            st.success('### :green[Your flight will arrive on time!]')

    if pred == 10:
        st.error('\nInsert a valid Value!', icon="🚨")
        
                    
# generate a dynamic iframe based on the airport selection
iata = iata.lower()
if iata:
    components.html(f"""<div class="airportia-widget">
    <iframe scrolling="no" frameborder="0" style="border:0; width: 100%; height: 95%; min-height: 650px; margin:0; padding:0;" src="https://www.flightera.net/en/widgets/airport?iata={iata}&depArr=dep&nrFlights=5&airlineIata=">
    </iframe>
    <div style="font-family: arial,sans-serif; font-size:12px; color:#3f9bdc; width: 100%; text-align: center; margin-top: 2px; padding-top: 5px; border-top: 1px solid #65747e;">
    <a style="text-decoration:none; color:#3f9bdc;" href="https://www.airportia.com/united-states/roberts-field-airport/arrivals/" title="Redmond Municipal Airport Arrivals" target="_top">
    Redmond Municipal Airport Arrivals
    </a>
    powered by
    <a style="text-decoration:none; color:#3f9bdc;" href="https://www.airportia.com/" target="_top" title="flight tracker">
    Airportia Flight Tracker
    </a>
    </div>
    </div>""",
    height=500)
