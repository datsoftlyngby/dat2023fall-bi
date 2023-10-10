# Design
import streamlit as st
from streamlit_option_menu import option_menu

import spacy
from spacy import displacy
import spacy_streamlit

import json
import requests
import pandas as pd
import numpy as np


from io import StringIO
import langdetect
from langdetect import DetectorFactory, detect, detect_langs
from PIL import Image
logo = Image.open('./media/logo.jpeg')

st.set_page_config(
    page_title="Data Science Holodeck",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:tdi@cphbusiness.dk',
        'About': "https://www.innotechspace.dk/holodeck"
    }
)

st.image(logo, width=200)
st.title("Data Science Holodeck")
st.subheader("Demo Sandbox", divider='rainbow')

text = ''

col1, col2 = st.columns((1,4))
with col1: 
    st.subheader('Operations')
                                          
def readMyFile():   
    uploaded_file = col2.file_uploader("Choose a file")   
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

# Design the visualisation
def charts():
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

            tab1, tab2, tab3 = col2.tabs(["tab1", "tab2", 'tab3'])
            with tab1:
                st.vega_lite_chart(sy, chart1, use_container_width=True)
            with tab2:
                st.vega_lite_chart(sy, chart2, theme=None, use_container_width=True)
            with tab3:
                st.bar_chart(sy, x = 'year', y = 'students', color = 'year')   
            #tabs = col2.tabs(["tab1", "tab2", 'tab3'])


st.divider() 
with st.sidebar:
    st.sidebar.title('Try Me')
    st.header('Select Data Source', divider='rainbow')
    
    oper = st.radio(
    "options",
    ["Tabular Data", "Human Language", "Knowledge Graph", ":rainbow[Help]"])
    subheds = ["Tabular Data", "Human Language", "Knowledge Graph",  ":rainbow[Help]"]
    
    if oper == 'Tabular Data':
        col2.subheader(subheds[0])                         
        upload_file = col2.file_uploader("choose a file with tab data (e.g. MS Excel)")
        ddf = pd.read_csv(upload_file)

        # ddf = pd.read_csv('/Users/tdi/Documents/Holodeck/Holodeck/middle.csv')  
        ddf = ddf.astype({"year": str})
        col2.write(ddf)
        
        sy = ddf.groupby(['year', 'company']).size().reset_index(name='students')
        
        if col2.button('Explore'):
            col2.subheader("Aggregate and Show the Data in Diagrams")
            col2.write('Click on tabs to explore')
            container = st.container()
            charts()

    
    if oper == 'Human Language':
        col2.subheader(subheds[1]) 
        # user input
        options = col2.multiselect("select file format",['dir', 'txt', 'doc', 'pdf', 'csv', 'wikipedia', 'youtube'],
                                ['dir','txt'])
        upload_file = col2.file_uploader("choose files with documents in natural language")
        url = col2.text_input('type url and press the button to load the resource')
        col2.link_button(url, url)

        if uploaded_file is not None:
            # Can be used wherever a "file-like" object is accepted:
            # dataframe = pd.read_csv(uploaded_file)
            col2.write(uploaded_file)
            
            
            
    # Q&A
        prompt = col2.chat_input("Say something")
        if prompt:
            st.write(f"User has sent the following prompt: {prompt}")
            
        with col2.chat_message("user"):
            col2.write("Hello 👋")
            col2.line_chart(np.random.randn(30, 3))
            
            message = col2.chat_message("assistant")
            message.write("Hello human")
            message.bar_chart(np.random.randn(30, 3))
            
    if oper == 'Knowledge Graph':
        col2.subheader(subheds[2]) 
        col1.write("The graph contains all collected inforation about the domain.")
        col1.write("The nodes are pieces oif knowledge, while the eddges are the logical relatiuons between them.")
        col1.write("Click on the items to explore them.\n\n")
        col1.write("Click on the arrow box to expand the graph.\n\n")
        col1.write("Put on a head set to explore the graph in virtual reality.\n\n")
        container = st.container()
        import streamlit.components.v1 as components
        p = open("./data/opit5.html")
        with col2:
            components.html(p.read(), height=480)
            # st.components.v1.html(html, width=None, height=None, scrolling=False)


        
    if oper == 'Help':
        st.write("See more at [https://www.innotechspace.dk/holodeck]")
        
    st.divider()
    
    st.header('Language Detected', divider='rainbow')
    option = st.selectbox('options', ('Danish', 'English'))
    st.divider()
    
    st.header('Model Suggested', divider='rainbow')
    option = st.selectbox(
       "How would you like to be contacted?",
       ("Email", "Home phone", "Mobile phone"),
       placeholder="Select contact method...")

    st.caption(' _Data Science Holodeck_ :blue[2023] :sunglasses:')
    

