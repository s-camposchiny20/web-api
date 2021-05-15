import numpy as np
import pandas as pd
import requests
import json
from datetime import datetime
import streamlit as st
import pydeck as pdk


def get_people():
    response = requests.get('http://api.open-notify.org/astros.json')
    data = json.loads(response.text)
    number = data['number']
    people = [person['name'] for person in data['people']]
    return number, people


def get_location():
    response = requests.get('http://api.open-notify.org/iss-now.json')
    data = json.loads(response.text)
    latitude = float(data['iss_position']['latitude'])  # -21.4682
    longitude = float(data['iss_position']['longitude'])  # -156.9924
    timestamp = data['timestamp']
    date_time = datetime.fromtimestamp(timestamp)
    return latitude, longitude, date_time


def render_map(latitude, longitude):
    return pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=latitude,
            longitude=longitude,
            zoom=1.5,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=pd.DataFrame(np.array([[latitude, longitude]]), columns=['lat', 'lon']),
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=100000,
            ),
        ],
    )


st.title('ISS Crew & Location')
st.write('Below you can see the name of the people aboard the International Space Station (ISS), '
         'as well as its current location.')

left_column, right_column = st.beta_columns(2)

number, people = get_people()
left_column.subheader('Current Number of People: {}'.format(number))
left_column.write('Names:')
for name in people:
    left_column.markdown('- {}'.format(name))

right_column.subheader('Current Location:')

latitude, longitude, date_time = get_location()
right_column.write(date_time)
geo = render_map(latitude, longitude)
right_column.pydeck_chart(geo)
