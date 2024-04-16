import google.generativeai as genai
import os
import streamlit as st
import fashion_script as fs
from PIL import Image
import io
import base64
import markdown 
st.set_page_config(page_title="Fashion Assistant", page_icon="👗", layout="wide")

api_key = st.secrets["api_key"]
genai.configure(api_key=api_key)

def main():
    banner_css = """
    <style>
    @import url('https://fonts.googleapis.com/css?family=Montserrat:400,700');
    @import url('https://fonts.googleapis.com/css?family=Lato:300');
    header {
        background-color: #69908d;
        color: white;
        text-align: center;
        padding: 10px 0 20px;
    }
    header h1 {
        text-align: center;
        text-transform: uppercase;
        color: white;
        font-size: 65px;
        font-weight: 400;
        letter-spacing: 3px;
        line-height: 0.8;
        padding-top: 50px;
        font-family: "Montserrat", sans-serif;
    }
    header h1 span {
        text-transform: uppercase;
        letter-spacing: 7px;
        font-size: 25px;
        line-height: 1;
    }
    header p {
        padding-top: 30px;
    }
    .wrapper {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        padding: 15px;
    }

    .header-card {
        width: 30%;
        border-radius: 20px;
        box-shadow: 10px 10px 10px 0px rgba(255,255,255,0.05), -3px -3px 3px 0px rgba(255,255,255,0.1);
        display: flex; 
        padding: 0px 20px 0px 20px;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .header-title {
        font-family: "Montserrat", sans-serif;
        font-size: 18px;
        font-weight: 600;
        color: white;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }

    .header-text {
        font-family: "Montserrat", sans-serif;
        font-size: 16px;
        color: #F8F8FF;
        margin-bottom: 10px;
        padding-bottom: 10px;
        text-align: center;
    }
    </style>
    """

    banner_html = """
    <header>
        <h1>Google Gemini<br> <span>[ Fashion and Technology ]</span></h1>
    <div class="wrapper">
        <div class="header-card">
            <p class="header-title">Photo Analysis
        </p>
            <p class="header-text">Upload photos of your outfits, accessories, or even color schemes to get an expert AI analysis of your items and style.</p>
        </div>
        
        <div class="header-card">
            <p class="header-title">Recommendations</p>
            <p class="header-text">Google Gemini will create personalized, custom recommendations tailored to you based on your photos.</p>
        </div>
        
        <div class="header-card">
            <p class="header-title">Shopping</p>
            <p class="header-text">Seamlessly shop recommendations tailored to your style and needs. Discover something new and exciting today!

        </p>
        </div>
    </header>
    """

    st.html(banner_css + banner_html)


    bottom_bar_css = """
        <style>
        .top_flexbar {
            display: flex;
            flex-direction: row;
            justify-content: space-between;
            align-items: stretch; /* cross axis behaviour */
            align-content: center; *//* cross axis only multiple lines */
            background: #425a58;
            box-shadow: 0 0 5px 5px rgba(128, 128, 128, 0.3);
            position: relative;
            align-items: center;
            transform: rotate(0deg);
            transition: all 0.25s;
            font-family: sans-serif;
            font-feature-settings: "smcp", "zero";
            font-weight: bold;
            margin-left: 200px;
            margin-right: 200px;
            text-align: center;
            }

            .top_flexbar__first,
            .top_flexbar__middle,
            .top_flexbar__last {
            padding: 1em;
            }

            .top_flexbar__first {
            min-width: 33%;
            color: white;
            background: #425a58;
            }
            .top_flexbar__middle {
            min-width: 33%;
            color: white;
            background: #425a58;
            }
            .top_flexbar__last {
            min-width: 33%;
            color: white;
            background: #425a58;
            }


        </style>
    """

    bottom_bar_html = """
    <div class="top_flexbar">
    <div class="top_flexbar__first">
        Step One: Upload your photo. 
    </div>
    <div class="top_flexbar__middle"> Step Two: Enter your question. </div>
    <div class="top_flexbar__last"> Step Three: Enjoy your style. </div>
    </div>
    """

    st.html(bottom_bar_css + bottom_bar_html)
    form_markdown = st.markdown("""
                    <style>
                    div.stForm {
                        align-items: center;
                    }
                    </style>""", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([.5, 1, .5])
    with col1:
         st.empty()
    with col2:
        with st.form(key="my_form"):

            uploaded_file = st.file_uploader("Upload an image", label_visibility='hidden',type=["jpg", "png", "jpeg"], key="image")

            t = st.markdown("""<style>
                            div.stTextInput > div > div:first-child {
                            background-color: lightgray; 
                            }
                            </style>""", unsafe_allow_html=True)
            user_query = st.text_input("Question", label_visibility='hidden', value="Ask Gemini...", key="query")

        
            submit =  st.form_submit_button("Generate Suggestions", type="primary")
            if submit:
                with st.spinner("Analyzing your image and questions..."):
                    user_image = Image.open(io.BytesIO(uploaded_file.read()))
                    buffered = io.BytesIO()
                    user_image.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    img_data_url = f"data:image/jpeg;base64,{img_str}"
                    result, add_ons = fs.image_review(user_image, user_query)
                    
        with col3:
            st.empty()

        
    if 'result' in locals() and 'add_ons' in locals() and 'img_data_url' in locals():
        display_results(result, add_ons, img_data_url)

def display_results(result, add_ons, img_data_url):
            results_css = """
            <style>

                @import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&display=swap');
                @import url('https://fonts.googleapis.com/css2?family=Josefin+Sans:ital,wght@0,100..700;1,100..700&display=swap');
                :root {
                    --font-family-title: 'Permanent Marker', sans-serif;
                    --font-family-secondary: 'Josefin Sans', sans-serif;
                    --font-size-title: 64px;
                    --line-height-title: 1.4;
                    --font-size-caption: 24px;
                    --line-height-caption: 1.2;
                    --color-text: #222022;
                    --color-highlight-primary: #fadba9;
                    --color-highlight-secondary: #efdcfc;
                    --border-radius-primary: 64px; 
                }

                body {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    width: 75%;
                    height: 100vh; /* viewport height */
                    padding: 0;
                    margin: 0;
                    font-family: var(--font-family-primary);
                }

                .main_card {
                    max-width: 85%;
                    border-radius: var(--border-radius-primary);
                    box-shadow: 10px 10px 10px 20px rgba(100,100,100,.15);
                    padding: 20px 20px 28px 20px;
                    box-sizing: border-box;
                    margin: 40px;
                    display: flex;
                    color: var(--color-text);
                    flex-direction: column;
                    background-color: white;
                }

                @media (min-width: 576px) {
                    .main_card {
                        flex-direction: row;
                    }
                
                    .main_card__image {
                        width: 50%;
                        height: 100%;
                        height: auto; 
                        object-fit: cover; 
                        margin-bottom: 0;
                        margin-right: 20px;
                        border-radius: 20px;
                    }
                
                    .Main_card__content {
                        width: 50%;
                        padding-left: 40px;
                    }
                
                    .main_card__title {
                        margin-bottom: 8px;
                        font-family: var(--font-family-title);
                        font-size: var(--font-size-title);
                    }
                
                    .main_card__text {
                        font-family: var(--font-family-secondary);
                        margin-left: 5px;
                        font-size: 24px;
                        line-height: var(--line-height-caption);
                        font-weight: 500;
                        padding: 20px 0;
                    }
                }
            </style>
        
            """
            result = result.text
            result = markdown.markdown(result)
            new_html = results_css + f"""
                <div class="main_card">
                <img src={img_data_url} class="main_card__image"  />
                <div class="main_card__content">
                    <span class="main_card__title">Gemini Says..</span>
                    <div class="main_card__text">{result}</div>
                </div>
                </div>  
            """
            st.html(new_html)
            display_cards(add_ons)
           
def display_cards(add_ons):
    st.divider()
   

    x_bar_html = """
        <style>
            .flexbar {
                display: flex;
                flex-direction: row;
                align-content: center; 
                margin: 1rem;
                box-shadow: 0 0 10px 5px rgba(128, 128, 128, 0.3);
                position: relative;
                align-items: center;
                transform: rotate(0deg);
                transition: all 0.25s;
                font-family: sans-serif;
                font-feature-settings: "smcp", "zero";
                font-weight: bold;
                height: 50px;
            }
            .flexbar__first {
                color: black;
                align-items: center;
                justify-content: center;
                font-size: 24px;
            }

        </style>
        <div class="flexbar">

            <div class="flexbar__first"> Add-Ons We Think Would Look Great With Your Choices and Style </div>

        </div>
    """
    st.html(x_bar_html)
    st.divider()

    card_css = """
    <style>
        .grid {
            display: flex;  /* Change to flex */
            justify-content: center;  /* Add this line */
            flex-wrap: wrap;  /* Add this line */
            gap: 20px;  /* Add space between items */
        }   
        img {
            display: block;
            width: 100%;
        }

        h2 {
            margin: 0;
            font-size: 1.4rem;
        }

        @media (min-width: 50em) {
            h2 {
                font-size: 1.8rem;
            }
        }

        .cta {
            --shadowColor: 330 90% 5%;
            display: flex;
            flex-wrap: wrap;
            background: hsl(341 80% 71%);

            max-width: 25vw;
            width: 100%;
            box-shadow: 0.65rem 0.65rem 0 hsl(var(--shadowColor) / 1);
            border-radius: 0.8rem;
            overflow: hidden;
            border: 0.5rem solid;
        }

        .cta img {
            aspect-ratio: 3 / 2;
            object-fit: contain;
            flex: 1 1 300px;
            outline: 0.5rem solid;
        }

        .cta__text-column {
            padding: min(2rem, 5vw) min(2rem, 5vw) min(2.5rem, 5vw);
            flex: 1 0 50%;
        }

        .cta__text-column > * + * {
            margin: min(1.5rem, 2.5vw) 0 0 0;
        }

        .cta a {
            display: inline-block;
            color: black;
            padding: 0.5rem 1rem;
            text-decoration: none;
            background: hsl(330 100% 40%);
            border-radius: 0.6rem;
            font-weight: 700;
            border: 0.35rem solid;
        }
        </style>
        """

    # Card HTML
    card_html = "<div class='grid'>"
    for item in add_ons:
        card_html += f"""
        <article class="cta">
            <img src={item['thumbnail']}>
            <div class="cta__text-column">
                <h2>{item['title']}</h2>
                <p>{item['price']}</p>
                
                <a href='{item['link']}' target='_blank'>Go Now</a>
            </div>
        </article>
        """
    card_html += "</div>"

    # Display cards
    st.html(card_css + card_html)


if __name__ == "__main__":
    main()