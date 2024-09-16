import  streamlit as st
from src import task4

st.title("Detailed Summmary of meeting")

st.write(task4.generate_detailed_summary())


