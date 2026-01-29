import streamlit as st
import pandas as pd
from const import SOURCE_DATAFRAME
import json

def display(attributes: json):
    # Extract the data from json object to streamlit table.
    # json format is: [{id: 1, value:value1}, {id:2, value:value2}]
    if not attributes or not isinstance(attributes, list):
        print("No data to display.")
        return

    # Defensive: check every item is a dict
    cleaned = [item for item in attributes if isinstance(item, dict)]

    if not cleaned:
        print("No valid data records to display.")
        return

    # Create DataFrame for pretty table rendering
    df = pd.DataFrame(cleaned)
    df_source = pd.DataFrame(SOURCE_DATAFRAME, columns=['id1', 'attr_type', 'category_name', 'name', 'tier_desc'])
    result_df = pd.merge(df, df_source, left_on='id', right_on='id1', how='left').drop('id1', axis=1)
    result_df = result_df[['id', 'attr_type', 'category_name', 'name', 'tier_desc', 'value', 'confidence']]
    st.table(result_df)