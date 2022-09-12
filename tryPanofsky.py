# click on the arrow, select apri terminale
# use the python -m streamlit run tryPanofsky.py command: it works better

import streamlit as st
import pandas as pd
import altair as alt
$ pip install pymantic
from pymantic import sparql
from graphviz import graphviz # not working

st.title("Data analysis of the Panofsky dataset")

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

st.write("here we upload some data")
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')


st.write("here we try to do a bubbleplot visualization")
data3 = pd.read_csv("mercury_mercury_final.csv")
df3 = data3.sort_values(by=['Date'])
#df4 = df3['Level1Representation'].astype('int')
df4 = pd.DataFrame(df3)

c = alt.Chart(df4).mark_circle().encode(
     x='Century', y='Artwork', size='Level1Representation') # , tooltip=['Century', 'Attribute', 'Frequency']

st.altair_chart(c, use_container_width=True)


#st.heading("The graph visualized") 

# Create a graphlib graph object
#graph = graphviz.Digraph()
#graph.parse("210622_output2.ttl", format="ttl")

#st.graphviz_chart(graph)
st.write("Here we try to visualize some data queried from the Blazegraph endpoint")

server = sparql.SPARQLServer('http://127.0.0.1:9999/bigdata/sparql')

# Loading data to Blazegraph
server.update('load <file:///210622_output2.ttl>')
people_result = []
# Executing query
result = server.query(
         """PREFIX d: <http://icondataset.org/> 
PREFIX icon: <https://w3id.org/icon/ontology/>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT (count(distinct ?people) as ?tot) WHERE {

?people a crm:E21_Person. 

}""")
for b in result['results']['bindings']:
    people_result.append(b["people"]["value"])
d = {'col1': "People", 'col2': people_result[0]}
df5 = pd.DataFrame(d)    

st.write(df5)
