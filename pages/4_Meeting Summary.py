import  streamlit as st
from src import task4
st.set_option('client.showErrorDetails', False)

st.title("Detailed Summmary of meeting")

st.markdown(task4.generate_detailed_summary())


