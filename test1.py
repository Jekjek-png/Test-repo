import pandas as pd
import streamlit as st

st.title("Test Streamlit App")

df = pd.DataFrame({"A": [1,2,3]})
st.write(df)