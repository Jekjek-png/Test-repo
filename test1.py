import pandas as pd
import streamlit as st

st.title("Hello Streamlit!")

df = pd.DataFrame({
    'Column 1': [1, 2, 3, 4],
    'Column 2': ['A', 'B', 'C', 'D']
})
st.write(df)
st.line_chart(df['Column 1'])
st.bar_chart(df['Column 1'])
st.map(df.assign(lat=[37.76, 37.77, 37.78, 37.79], lon=[-122.4, -122.41, -122.42, -122.43]))
st.checkbox("Check me out!")
st.radio("Choose one:", ['Option 1', 'Option 2', 'Option 3'])    
st.selectbox("Select an option:", ['Option A', 'Option B', 'Option C'])
st.multiselect("Select multiple options:", ['Option X', 'Option Y', 'Option Z'])
st.slider("Select a range:", 0, 100, (25, 75))
st.text_input("Enter some text:")
st.text_area("Enter a longer text:")
st.date_input("Select a date:")
st.time_input("Select a time:")