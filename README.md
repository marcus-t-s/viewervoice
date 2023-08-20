# ViewerVoice
## 🏁Introduction  
Welcome to ViewerVoice, the tool that allows you to gain insights into what viewers have commented under a YouTube video. We created this dashboard particularly to help YouTubers better understand their audience and allow for data-driven decision making, enabling them to strategise and build their brand. As well as to help brands understand the audience of potential Creators they are looking to partner with.

This dashboard is still under development; further updates will be implemented in due course. Please note that at present the source code is not public however, please feel free to raise suggestions or issues you encounter here. To try out ViewerVoice firsthand please refer to the following link.  
https://viewervoice.streamlit.app/

## 🚶‍♂️Walkthrough  
### 🗨️Retrieving YouTube Comments  
To retrieve comments we used the YouTube Data API which provides various functionalities, including retrieving YouTube comments. At present we do not read in comment replies. Please refer to the instructions provided in the following link to acquire your unique API key. Please be aware that each API key facilitates up to 10,000 API calls within a 24-hour period.  
https://developers.google.com/youtube/v3/getting-started

### 👩‍💻Implementing Natural Language Processing Models  
ViewerVoice covers the following areas of NLP driven by BERT based models.

**Topic modelling** groups the comments into topics so that you can gain clearer insights into the key themes viewers are discussing in the comment section. For optimal performance of the current topic model, we recommend retrieving thousands of comments.

**Sentiment analysis** identifies whether comments are positive, negative or neutral. This provides you with an overview of viewers feel toward aspects of the content. Please note that at present, the sentiment analysis does not take emojis into account.

**Semantic search** allows you to not only search for comments with exact matches to input words or phrases, but also for comments that contain similar words. For example, if you search for the word 'music', comments containing 'music' as well as 'song' and 'vinyl' can show up. This feature enables you to search for specifics in a comment section. For example, perhaps you are a YouTuber that has collaborated with another Creator or advertised for a brand you have partnered with, you can search for the name of the Creator or brand in your comments to see how your viewers reacted to this.

### 📊Creating a Streamlit WebApp   - Marcus

## 🔍Results  
We hope the insights provided by ViewerVoice will enable YouTubers to cater to their audience and use data-derived observations to negotiate opportunities and aid brands in gaining a deeper understanding of the intended audience of prospective partnerships. Future developments look to include but are not limited to improving the UI/UX design and implementing LLMs to give enhanced and more comprehensible results.
