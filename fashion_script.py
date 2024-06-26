import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import shopping_items as si 
import os
import streamlit as st

api_key = st.secrets["api_key"]
genai.configure(api_key=api_key)

def vision_model():
    vision_model = genai.GenerativeModel("gemini-pro-vision")
    return vision_model

def text_model():
    text_model = genai.GenerativeModel("gemini-pro")
    return text_model
    

def image_review(user_image, user_query):
    model = vision_model()
    prompt = """
        The user has provided questions and/or images for your review. 
        Carefully review the questions and/or images and provide expert fashion and styling advice.
        Output should be at least 2 paragraphs followed by bullet points.
        You're a very chatty, friendly and caring expert fashion stylist who loves helping people.
        Never insult anyone or say anything is unflattering or unattractive.
        Stay positive and only discuss fashion and style.
        Do not mention looks, body parts, body type, body size, race, national origin, politics, or gender.
      
        
    """
    response = model.generate_content([
        prompt, 
        user_image, 
        user_query
    ], safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    })
    response.resolve()
    add_ons = create_search_phrases(response)
    return response, add_ons

def create_search_phrases(response):
    model = text_model()  
    try:
    # Check if 'candidates' list is not empty
        if response.candidates:
            # Access the first candidate's content if available
            if response.candidates[0].content.parts:
                generated_text = response.candidates[0].content.parts[0].text
                print("Generated Text:", generated_text)
            else:
                print("No generated text found in the candidate.")
        else:
            print("No candidates found in the response.")
    except (AttributeError, IndexError) as e:
        print("Error:", e)

    response_text = generated_text
    parsed_response = model.generate_content(["Generate a single search query to be used to search shopping. The search phrase should be based on the suggestions given in response_text and be no more than 2 words total. Try to combine specific search phrases.  Examples of good queries - 'red scarf', 'grey sandals', 'black jeans', 'silver necklace'", response_text])
    phrase = parsed_response.text
    add_ons = si.find_ionic_items(phrase)
    return add_ons
