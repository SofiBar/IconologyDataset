**Dataset description** <br>
The Iconology dataset is a RDF dataset of a selection of the art historian Erwin Panofsky's iconological studies, described according to the ICON ontology (see the documentation [here](https://w3id.org/icon/docs)) and standards.

It contains interpretations about ca. 400 artworks (see Figure 1) mostly from the Middle Ages and Renaissance Western art, mainly interpreted by Panofsky. The interpretations are divided into three levels, from a more superficial understanding to a deeper one, as described by the art historian's theory, and inter-level links among identified subjects are provided. The subject types recorded include natural elements, actions and emotions (level 1), characters, events, places, objects with a specific identity (e.g. the Bible), personifications, symbols, stories and allegories (level 2), concepts, and cultural phenomena (level 3). For each subject identification a provenance of the assertion can be provided, indicating the author, source, and cited evidence, so as to allow the coexistence of multiple (diverging) interpretations.

**Repository and access to the data** <br>
The current repository contains the dataset dump in RDF format (folder: `data`) serialized both in Turtle and XML/RDF, and the code used for creating, aligning and evaluating the dataset.

  

Further access to the dataset:

- SPARQL endpoint: [https://projects.dharc.unibo.it/icondataset/sparql](https://projects.dharc.unibo.it/icondataset/sparql)
    
- Online dashboard showing an exploratory analysis and allowing an interactive information retrieval and visualization: [https://iconology-dataset.streamlit.app/](https://iconology-dataset.streamlit.app/)
    

  
<br>
The content of this repository is published under a [CC BY-NC-SA 4.0 license](https://creativecommons.org/licenses/by-nc-sa/4.0/).