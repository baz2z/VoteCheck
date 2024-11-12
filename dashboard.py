import streamlit as st
import pandas as pd
     
st.write("""
# My first app
Hello *world!*
""")


     
df = pd.read_csv("dat/two_combined_data.csv")

st.data_editor(df)