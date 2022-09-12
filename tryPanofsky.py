# click on the arrow, select apri terminale
# use the python -m streamlit run tryPanofsky.py command: it works better

import streamlit as st
import pandas as pd
import altair as alt

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


# to do: try a scatterplot visualization with mercury_mercury_final.csv
data3 = pd.read_csv("mercury_mercury_final.csv")
df3 = data3.sort_values(by=['Date'])


c = alt.Chart(df3).mark_circle().encode(
     x='Century', y='Attribute', size='Frequency', tooltip=['Century', 'Attribute', 'Frequency'])

st.altair_chart(c, use_container_width=True)
