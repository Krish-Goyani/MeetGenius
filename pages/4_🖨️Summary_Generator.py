import  streamlit as st
from src import task4
st.set_option('client.showErrorDetails', False)
with st.sidebar:
    st.markdown("\n")
    st.markdown("\n")
    st.markdown("""Simply wait a few seconds and you will receive an abbreviated version of the meeting.""")
st.header("Detailed Summmary of meeting", divider="rainbow")

st.markdown(task4.generate_detailed_summary())


