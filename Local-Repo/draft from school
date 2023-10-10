# DRAFT

#!/usr/bin/env python
# coding: utf-8
import spacy
from spacy import displacy
import streamlit as st
import spacy_streamlit

import json
import requests
import pandas as pd
import numpy as np

from io import StringIO
import langdetect
from langdetect import DetectorFactory, detect, detect_langs
from streamlit_option_menu import option_menu

text = ''
# Display header
st.title("Data Science Holodeck")
st.subheader("Data Pre-Processing Demo")

def mymenu():
    menu = ["Home","Profile","Status", "Student", "CV", "Tech", "About"]
    subheds = ['H0', 'H1', 'H2', 'H3', 'H4', 'H5', 'HA']
    ch = st.sidebar.selectbox('Select the option',menu)
    if ch == menu[1]:
        st.subheader(subheds[1])                         
        # user input
        option = st.selectbox('select feature', ('size', 'location', 'work', 'techs',))
        st.markdown("Choose profile")
    if ch == menu[2]:
        st.subheader(subheds[2])                         
        # user input
        option = st.selectbox('select measure', ('rank', 'trust', 'sentiment', 'techs',))
        st.markdown("Choose status")
    return menu


mymenu()

with st.sidebar:
    selected = option_menu("Main Menu", ["Home", 'Settings'], 
        icons=['house', 'gear'], menu_icon="cast", default_index=1)
    selected
        
st.header("Tab Data")
st.subheader("Data Ingestion")

upload_file = st.file_uploader("Input data from a file")

ddf = pd.read_csv(upload_file)

# ddf = pd.read_csv('/Users/tdi/Documents/Holodeck/Project/Demos/Praktik/middle.csv')  
ddf = ddf.astype({"year": str})
st.write(ddf)

st.write("Aggregate the data per year and per company")

sy = ddf.groupby(['year', 'company']).size().reset_index(name='students')
st.write("Quantity of students per year and company")
st.write(sy)

st.subheader("Visualize the data in diagrams")


# Design the visualisation
chart1 = {
    "mark": {'type': 'point', 'tooltip': True},
    "encoding": {
        "x": { "field": "company", "type": "nominal"},
        "y": {"field": 'students', "type": "quantitative" },
        "color": {"field": "year", "type": "nominal"},
        "shape": {"field": "year", "type": "nominal"},
    }
}

chart2 = {
    "mark": {'type': 'circle', 'tooltip': True},
    "encoding": {
        "x": { "field": "company",  "type": "nominal" },
        "y": { "field": 'students',  "type": "quantitative" },
        "color": {"field": "year", "type": "nominal"},
        "size": {"field": "students", "type": "quantitative"},
    }
}

tab1, tab2, tab3 = st.tabs(["View One", "View Two", "View Three"])

with tab1:
    st.vega_lite_chart(sy, chart1, use_container_width=True)
with tab2:
    st.vega_lite_chart(sy, chart2, theme=None, use_container_width=True)
with tab3:
    st.bar_chart(sy, x = 'year', y = 'students', color = 'year')   

    
# Display a section header
st.header("Text Data")

def readMyFile():   
    uploaded_file = st.file_uploader("Choose a file")   
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        # st.write(bytes_data)

        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        # st.write(stringio)

        # To read file as string:
        text = stringio.read()
        # st.write(text)

        # Can be used wherever a "file-like" object is accepted:
        # dataframe = pd.read_csv(uploaded_file)
        # st.write(dataframe)
    return text


def lang_detect(text):
    mylang = ''
    mylangprob = 0.0
    try:
        langs = langdetect.detect_langs(text)
        mylang, mylangprop = langs[0].lang, langs[0].prob 
    except langdetect.lang_detect_exception.LangDetectException:
        log.debug('Language not recognised')
    return mylang, mylangprop

text = readMyFile()

# Test: detect the language with accuracy
lang, prob = lang_detect(text)

if lang=='en': 
    models = ['en_core_web_md', 'da_core_news_md']
    default_model = 'en_core_web_md'
elif lang=='da': 
    models = ['da_core_news_md', 'en_core_web_md']
    default_model = 'da_core_news_md'

default_text = text

nlp = spacy.load(default_model)
doc = nlp(text)

myvisualizers = []
spacy_streamlit.visualize(models, default_text, default_model, visualizers=myvisualizers, 
                          show_json_doc=False, show_meta=False, show_config=False,
                          show_visualizer_select=True, sidebar_title='Select Model and Operation')

from spacy_streamlit import visualize_tokens
visualize_tokens(doc,  title='Tokens and Roles')

from spacy_streamlit import visualize_ner
visualize_ner(doc, labels=nlp.get_pipe("ner").labels, title='Named Entities')

# from spacy_streamlit import visualize_textcat
# visualize_textcat(doc)


# visualize_similarity()
from spacy_streamlit import visualize_similarity
similarity_texts = ['Hello', 'Hi']
visualize_similarity(nlp, similarity_texts)

# about
st.sidebar.subheader("About")
st.sidebar.info("Holodeck is testing spaCy-Streamlit")


