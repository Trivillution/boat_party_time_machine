import streamlit as st
from PIL import Image

st.title('CCS Alumni Boat Party 2022')

image = Image.open('/data/logo.PNG')

st.image(image)