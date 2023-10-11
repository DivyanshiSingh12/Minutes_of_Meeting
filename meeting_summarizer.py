import streamlit as st
import requests
import pandas as pd
from get_results import *

uploaded_file = st.file_uploader('Please  upload a file')

if uploaded_file is not None:
    st.audio(uploaded_file, start_time=0)
    polling_endpoint = upload_to_AssemblyAI(uploaded_file)

    status= 'submitted'
    while status != 'completed':
        polling_response = requests.get(polling_endpoint, headers=headers)
        status = polling_response.json()['status']

        if status == 'completed':

            #display categories
            st.subheader('Main themes')

           
            
            with st.expander('Themes'):
                categories =polling_response.json()['iab_categories_result']['summary']
                for cat in categories:
                    st.markdown("* " + cat)

            #display chapter summaries
            st.subheader('Summary notes of this meeting')
            chapters = polling_response.json()['chapters']
            chapters_df = pd.DataFrame(chapters)
            chapters_df['start_str'] = chapters_df['start'].apply(convertMillis)
            chapters_df['end_str'] = chapters_df['end'].apply(convertMillis)

            for index, row in chapters_df.iterrows():
                with st.expander(row['gist']):
                    st.write(row['summary'])
                    st.button(row['start_str'])



            
            st.dataframe(chapters)

            



                     



