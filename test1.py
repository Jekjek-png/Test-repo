import pandas as pd
import streamlit as st

st.title("Hello Bisaya" )
st.write("This is a simple Streamlit app to demonstrate how bisaya is roy is.")

# Create a DataFrame
df = pd.DataFrame({
    "Fruit": ["Apple", "Banana", "Orange", "Mango"],
    "Quantity": [10, 25, 17, 8]
})

# Plot with x and y specified
st.bar_chart(df, x="Fruit", y="Quantity")
