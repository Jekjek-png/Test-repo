import pandas as pd
import streamlit as st

st.title("Hello Ubuntu")

df = pd.DataFrame({"A": [1,2,3]})
st.write(df)