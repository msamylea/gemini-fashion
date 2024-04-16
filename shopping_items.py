from typing import List
import requests
import os
import streamlit as st

def find_ionic_items(user_query: str) -> List[dict]:
    url = "https://api.ioniccommerce.com/query"

    payload = {"query": {
            "query": user_query,
            "num_results": 5
        }}
    headers = {
        "x-api-key": os.environ.get(st.secrets["ionic_api_key"]),
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    data = response.json()

    add_ons = []
    for result in data['results']:
        for index, shopping_result in enumerate(result['products']):
            add_on = {  # Create a new dictionary for each shopping result
                "title": shopping_result['name'],
                "price": shopping_result['price'],
                "link": shopping_result['links'][0]['url'],  # Assuming 'links' is a list of dictionaries
                "thumbnail": shopping_result['thumbnail']
            }
            add_ons.append(add_on)  # Append the new dictionary to the add_ons list

    return add_ons
    
