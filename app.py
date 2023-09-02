import os
from git import Repo
import streamlit as st    
import time
from PIL import Image
import base64
from transformers import pipeline
import spacy
import googleapiclient
import numpy as np
from sentence_transformers import SentenceTransformer
from matplotlib import colormaps
from matplotlib.colors import ListedColormap

GITHUB_PAT = os.environ['GITHUB']
SENTIMENT = os.environ['SENTIMENT']
EMBEDDING = os.environ['EMBEDDING']

if not os.path.exists('repo_directory'):
    try:
        Repo.clone_from(f'https://marcus-t-s:{GITHUB_PAT}@github.com/marcus-t-s/yt-comment-analyser.git', 'repo_directory'  ) 
    except:
        st.error("Error: Oops there's an issue on our end, please wait a moment and try again.")
        st.stop()

from repo_directory.all_utils import *


# Streamlit configuration
st.set_page_config(
    page_title="ViewerVoice | YouTube Comment Analyser",
    layout="wide",
    page_icon=Image.open('page_icon.png')
)


# Define and load cached resources
@st.cache_resource
def load_models():
    sentiment_pipeline = pipeline("sentiment-analysis", model=f'{SENTIMENT}')
    embedding_model = SentenceTransformer(f'{EMBEDDING}')
    spacy_nlp = spacy.load("en_core_web_sm")
    add_custom_stopwords(spacy_nlp, {"bring", "know", "come"})
    return sentiment_pipeline, embedding_model, spacy_nlp


@st.cache_resource
def load_colors_image():
    mask = np.array(Image.open('youtube_icon.jpg'))
    Reds = colormaps['Reds']
    colors = ListedColormap(Reds(np.linspace(0.4, 0.8, 256)))
    with open("viewervoice_logo_crop.png", "rb") as img_file:
        logo_image = base64.b64encode(img_file.read()).decode("utf-8")
    return mask, colors, logo_image


sentiment_pipeline, embedding_model, spacy_nlp = load_models()
mask, colors, logo_image = load_colors_image()


# Hide line at the top and "made with streamlit" text
hide_decoration_bar_style = """
    <style>
        header {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

main_page = st.container()

if 'YouTubeParser' not in st.session_state:
    st.session_state['YouTubeParser'] = YoutubeCommentParser()
if 'comment_fig' not in st.session_state:
    st.session_state["comment_fig"] = None
    st.session_state["wordcloud_fig"] = None
    st.session_state["topic_fig"] = None
    st.session_state["sentiment_fig"] = None
if 'rerun_button' not in st.session_state:
    st.session_state['rerun_button'] = "INIT"
if 'topic_filter' not in st.session_state:
    st.session_state['topic_filter'] = False
if 'sentiment_filter' not in st.session_state:
    st.session_state['sentiment_filter'] = False
if 'filter_state' not in st.session_state:
    st.session_state['filter_state'] = "INIT"
if 'video_link' not in st.session_state:
    st.session_state["video_link"] = None
if 'num_comments' not in st.session_state:
    st.session_state['num_comments'] = None

# Set reference to YouTubeParser object for more concise code
yt_parser = st.session_state['YouTubeParser']


def query_comments_button():
    # Delete larger objects from session state to later replace
    del st.session_state["comment_fig"]
    del st.session_state["wordcloud_fig"]
    del st.session_state["topic_fig"]
    del st.session_state["sentiment_fig"]
    del st.session_state["YouTubeParser"]

    # Reset session state variables back to placeholder values
    st.session_state.rerun_button = "QUERYING"
    st.session_state['filter_state'] = "INIT"
    st.session_state["topic_filter"] = False
    st.session_state["sentiment_filter"] = False
    st.session_state["semantic_filter"] = False
    st.session_state["figures_built"] = False
    st.session_state["comment_fig"] = None
    st.session_state["wordcloud_fig"] = None
    st.session_state["topic_fig"] = None
    st.session_state["sentiment_fig"] = None
    st.session_state["YouTubeParser"] = YoutubeCommentParser()


def filter_visuals_button():
    st.session_state["filter_state"] = "FILTERING"


with st.sidebar:
    st.session_state["api_key"] = st.text_input('YouTube API key', value="", type='password')
    st.session_state["video_link"] = st.text_input('YouTube Video URL', value="")
    st.session_state["max_comments"] = st.slider(label="Maximum number of comments to query",
                                                 min_value=100,
                                                 max_value=3000,
                                                 step=100)
    st.session_state["max_topics"] = st.slider(label="Maximum number of topics",
                                               min_value=5,
                                               max_value=20,
                                               step=1)
    st.button('Query comments :left_speech_bubble:', on_click=query_comments_button)

with main_page:
    # Reduce space at the top
    reduce_header_height_style = """
        <style>
            div.block-container {padding-top:0rem;}
            div.block-container {padding-bottom:1rem;}
            div.block-container {padding-left:1.5rem;}
        </style>
    """
    st.markdown(reduce_header_height_style, unsafe_allow_html=True)

    # Title and intro section
    markdown_content = f"""
    <div style='display: flex; align-items: center; justify-content: center;'>
        <img src='data:image/png;base64,{logo_image}' height='135px';/>
    </div>
    """
    st.markdown(markdown_content, unsafe_allow_html=True)

    # LinkedIn links
    lnk = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">'
    st.markdown(lnk + """
    <div style="display: flex; justify-content: center; align-items: center; flex-direction: column;">
        <br>
        <p style="text-align: center;"><b>Made by</b>
        <b>
        <a href='https://www.linkedin.com/in/afiba-7715ab166/' style="text-decoration: none">
        <i class='fa fa-linkedin-square'></i>&nbsp;<span style='color: #000000'>Afiba Annor</span></a>     
        <a href='https://www.linkedin.com/in/marcus-singh-305927172/' style="text-decoration: none">
        <i class='fa fa-linkedin-square'></i>&nbsp;<span style='color: #000000'>Marcus Singh</span></a>
        </b></p>
        </div>

    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    # Notes section
    st.markdown("<p style='font-size: 1.3rem;'><b>📝 Notes</b></p>", unsafe_allow_html=True)

    html_content = """
    <ul>
        <li style='font-size: 0.95rem;'>This dashboard is still under development; further updates will be implemented 
        in due course.</li>
        <li style='font-size: 0.95rem;'>Kindly refer to the instructions provided in this 
        <a href='https://developers.google.com/youtube/v3/getting-started'>link</a>. 
        This will guide you in acquiring your API key to retrieve comments.</li>
        <li style='font-size: 0.95rem;'>Please be aware that each API key facilitates up to 10,000 API calls within 
        a 24-hour period.</li>
        <li style='font-size: 0.95rem;'>Currently, the dashboard caters to comments in English and does not 
        include comment replies.</li>
        <li style='font-size: 0.95rem;'>Comments undergo cleaning and pre-processing to optimise modelling. As a result, 
        the returned comment count may fall short of the maximum queried amount.</li>
        <li style='font-size: 0.95rem;'>Please note that the sentiment analysis currently does not take emojis into 
        account.</li>
        <li style='font-size: 0.95rem;'>For optimal performance of the current topic model, we recommend retrieving 
        thousands of comments.</li>
        <li style='font-size: 0.95rem;'>Please anticipate that querying comments and running the models may require 
        a few minutes to complete.</li>
    </ul>
    <hr>
    """
    # Display the HTML content using st.markdown()
    st.markdown(html_content, unsafe_allow_html=True)

# Query comments section
if (st.session_state.rerun_button == "QUERYING") and (st.session_state["video_link"] is not None):
    with st.spinner('Querying comments and running models'):
        yt_parser = st.session_state["YouTubeParser"]
        try:
            yt_parser.build_youtube_api(st.session_state['api_key'])
        except:
            st.error("Error: Unable to query comments, please check your API key")
            st.stop()
        try:
            yt_parser.query_comments(st.session_state['video_link'], st.session_state['max_comments'])
        except googleapiclient.errors.HttpError:
            st.error("Error: Unable to query comments, please check your API key.")
            st.stop()
        except:
            st.error("Error: Unable to query comments, incorrect YouTube URL or maximum \
                              API call limit reached.")
            st.stop()

        # Run formatting and models
        yt_parser.format_comments()
        yt_parser.clean_comments()
        yt_parser.run_sentiment_pipeline(sentiment_pipeline)
        yt_parser.run_topic_modelling_pipeline(embedding_model,
                                               nlp=spacy_nlp,
                                               max_topics=st.session_state['max_topics'])
    # Set "QUERY COMPLETE" to bypass running this section on script re-run
    st.session_state.rerun_button = "QUERY COMPLETE"

# Once comments are queried, build charts ready to visualise
if st.session_state.rerun_button == "QUERY COMPLETE":
    # Check for built figures:
    if (not st.session_state["figures_built"]) or (st.session_state.filter_state == "FILTERING"):
        # Select colors for wordcloud

        # If filtering button pressed
        if st.session_state.filter_state == "FILTERING":
            df_filtered = yt_parser.df_comments.copy()
            if st.session_state["topic_filter"]:
                df_filtered = df_filtered.query(f"Topic == {st.session_state.topic_filter}")
            if st.session_state["sentiment_filter"]:
                df_filtered = df_filtered.query(f"Sentiment == {st.session_state.sentiment_filter}")
            if st.session_state["semantic_filter"]:
                df_filtered = semantic_search(df=df_filtered, query=st.session_state["semantic_filter"],
                                              embedding_model=embedding_model,
                                              text_col='Comment_Clean')
            if len(df_filtered) == 0:
                st.session_state['num_comments'] = 0

            else:
                st.session_state['num_comments'] = len(df_filtered)
                # Build filtered table figure
                st.session_state["table_fig"] = comments_table(df_filtered,
                                                               ['publishedAt', 'Comment_Formatted', 'Likes',
                                                                'Sentiment', 'Topic'],
                                                               {'publishedAt': 'Date', 'Comment_Formatted': 'Comment'})

                # Build filtered wordcloud figure
                st.session_state["wordcloud_fig"] = comment_wordcloud(df_filtered, mask, colors)

                # Build filtered topic figure
                st.session_state["topic_fig"] = topic_treemap(df_filtered, "Topic")

                # Build filtered sentiment figure
                st.session_state["sentiment_fig"] = sentiment_chart(df_filtered, "Sentiment")

                st.session_state["figures_built"] = True

                st.session_state.filter_state = "FILTERED"

        # No filtering selected
        else:
            st.session_state['num_comments'] = len(yt_parser.df_comments)

            # Can only build graphs if we have comments
            if st.session_state['num_comments'] > 0:
                try:
                    # Build unfiltered table figure
                    st.session_state["table_fig"] = comments_table(yt_parser.df_comments,
                                                                   ['publishedAt', 'Comment_Formatted', 'Likes',
                                                                    'Sentiment', 'Topic'],
                                                                   {'publishedAt': 'Date',
                                                                    'Comment_Formatted': 'Comment'})
                    # Build unfiltered wordcloud figure
                    st.session_state["wordcloud_fig"] = comment_wordcloud(yt_parser.df_comments,
                                                                          mask, colors)
                    # Build unfiltered topic figure
                    st.session_state["topic_fig"] = topic_treemap(yt_parser.df_comments, "Topic")
                    # Build unfiltered sentiment figure
                    st.session_state["sentiment_fig"] = sentiment_chart(yt_parser.df_comments, "Sentiment")

                    st.session_state["figures_built"] = True
                except:
                    st.error("Error: Oops there's an issue on our end, please wait a moment and try again.")
                    st.stop()

with main_page:
    if st.session_state.rerun_button == "QUERY COMPLETE":
        st.subheader(f"{yt_parser.title}")
        st.markdown("<hr><br>", unsafe_allow_html=True)

        if st.session_state['num_comments'] > 0:
            table_col, word_cloud_col = st.columns([0.55, 0.45])
            with table_col:
                st.markdown(f"""<p style='font-size: 1.3rem;
                display: flex; align-items: center; justify-content: center;'><b>
                                                    Comments</b></p>""", unsafe_allow_html=True)
                st.plotly_chart(st.session_state["table_fig"], use_container_width=True)

            with word_cloud_col:
                st.markdown(f"""<p style='font-size: 1.3rem;
                display: flex; align-items: center; justify-content: center;'><b>
                                                               Word Cloud</b></p>""", unsafe_allow_html=True)

                st.pyplot(st.session_state["wordcloud_fig"], use_container_width=True)

            treemap_col, sentiment_donut_col = st.columns([0.55, 0.45])

            with treemap_col:
                st.markdown(f"""<p style='font-size: 1.3rem;
                display: flex; align-items: center; justify-content: center;'><b>
                                                                Topic Proportions</b></p>""", unsafe_allow_html=True)

                st.plotly_chart(st.session_state["topic_fig"], use_container_width=True)

            with sentiment_donut_col:
                st.markdown(f"""<p style='font-size: 1.3rem;
                display: flex; align-items: center; justify-content: center;'><b>
                                                        Sentiment Distribution</b></p>""", unsafe_allow_html=True)
                st.plotly_chart(st.session_state["sentiment_fig"], use_container_width=True)

            # st.table(yt_parser.df_comments.head())
        else:
            st.write("Unfortunately we couldn't find any comments for this set of filters, please try "
                     "editing the filters and try again")

with st.sidebar:
    # Define the HTML and CSS for the button-style container
    if st.session_state['num_comments'] is not None:
        num_comments = st.session_state['num_comments']
    else:
        num_comments = 0
    htmlstr = f"""
                <p style='background-color: rgb(255, 255, 255, 0.75); 
                color: rgb(0, 0, 0, 0.75); 
                font-size: 40px;    
                border-radius: 7px; 
                padding-top: 25px; 
                padding-bottom: 25px;
                padding-right: 25px; 
                padding-left: 25px; 
                line-height:25px;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);'>
                &nbsp;{num_comments}</p>
                """
    # Display the button-style container with number of comments
    st.subheader("Number of comments")
    st.markdown(htmlstr, unsafe_allow_html=True)

    # Filters section
    st.subheader("Filters")

    if yt_parser.df_comments is not None:
        st.session_state["topic_filter"] = st.multiselect("Topic",
                                                          options=sorted(list(yt_parser.df_comments['Topic'].unique())))
        st.session_state["sentiment_filter"] = st.multiselect("Sentiment",
                                                              options=list(yt_parser.df_comments['Sentiment'].unique()))
        st.session_state["semantic_filter"] = st.text_input("Keyword search",
                                                            max_chars=30)
        st.button('Filter visualisations :sleuth_or_spy:', on_click=filter_visuals_button)

    else:
        st.multiselect("Topic",
                       options=["Please query comments from a video"],
                       disabled=True)
        st.multiselect("Sentiment",
                       options=["Please query comments from a video"],
                       disabled=True)
        st.text_input("Keyword search",
                      disabled=True)
        st.button('Please query comments before filtering',
                  disabled=True)