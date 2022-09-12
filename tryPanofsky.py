# click on the arrow, select apri terminale
# use the python -m streamlit run tryPanofsky.py command: it works better

import streamlit as st
import pandas as pd

data = pd.read_csv("mercury_attr_time4.csv")
# print the first 5 rows
df = data.sort_values(by=['Date'])
# print(df)

st.write("Here's the first visualization of attributes of mercury over time:")
st.write(df)

data2 = pd.read_csv("cupid_attr_time.csv")
df2 = data.sort_values(by=['Date'])
# print(df)

st.write("Here's another example with Cupid")
st.write(df2)


# to do: try a scatterplot visualization with mercury_final.csv

