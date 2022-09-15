# click on the arrow, select apri terminale
# use the python -m streamlit run tryPanofsky.py command: it works better
import rdflib
from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
                           PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, \
                           VOID, XMLNS, XSD
from rdflib import Namespace
from rdflib import URIRef


import streamlit as st
import pandas as pd
import altair as alt
# !pip install pymantic
from pymantic import sparql
import graphviz # not working

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


# st.write("The graph visualized") 

# Create a graphlib graph object
# g= rdflib.Graph()
# g.parse("210622_output2.ttl", format="ttl")
#graph = graphviz.Digraph()

# st.graphviz_chart(g)

st.write("subject level 1 and 2 frequency per cultural phenomenon") 
df6 = pd.read_csv("subj_frequency_per_cf.csv")
df6.sort_values(by=['Cultural Phenomenon'])
st.write(df6)

st.write("Here we try to visualize some data queried from the Blazegraph endpoint")

server = sparql.SPARQLServer('http://127.0.0.1:9999/bigdata/sparql')

#Loading data to Blazegraph
# error: HTTPConnectionPool(host='127.0.0.1', port=9999): Max retries exceeded with url: /bigdata/sparql (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7f00d0417f10>: Failed to establish a new connection: [Errno 111] Connection refused')) 

# server.update('load <file:///210622_output2.ttl>')
people_result = []
# Executing query
result = server.query(
         """PREFIX d: <http://icondataset.org/> 
PREFIX icon: <https://w3id.org/icon/ontology/>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT distinct (?rel) WHERE {

d:ART1001 ?rel ?o. 

}

""")
for b in result['results']['bindings']:
    people_result.append(b["people"]["value"])
d = {'col1': "People", 'col2': people_result[0]}
df5 = pd.DataFrame(d)    

st.write(df5)
