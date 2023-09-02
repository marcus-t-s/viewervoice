# ViewerVoice

<p align="center">
<img width="606" alt="image" src="https://github.com/marcus-t-s/viewervoice/assets/40894018/6391080a-d6da-45cc-9467-4159b0b74423">
</p>

## 🏁Introduction  
Welcome to ViewerVoice, the tool that allows you to gain insights into what viewers have commented under a YouTube video. We created this dashboard particularly to help YouTubers better understand their audience and allow for data-driven decision making, enabling them to strategise and build their brand. As well as to help brands understand the audience of potential creators they are looking to partner with.

This dashboard is still under development; further updates will be implemented in due course. To try out ViewerVoice firsthand please refer to the following link.  
https://viewervoice-analytics-viewervoice.hf.space/

Please note that the source code is written to support deployment on Hugging Face Spaces, please feel free to raise suggestions or issues you encounter here. 
https://huggingface.co/spaces/viewervoice-analytics/viewervoice/discussions

## 🚶‍♂️Walkthrough  
### 🗨️Retrieving YouTube Comments  
To retrieve comments we used the YouTube Data API which provides various functionalities, including retrieving YouTube comments. At present we do not read in comment replies. Please refer to the instructions provided in the following link to acquire your unique API key. Please be aware that each API key facilitates up to 10,000 API calls within a 24-hour period.  
[https://medium.com/beyond-the-views-how-viewervoice-enriches-content-performance-analytics](https://medium.com/@afibannor/beyond-the-views-how-viewervoice-enriches-content-performance-analytics-3c46854db697?source=friends_link&sk=042267d3c0ed460c3ad0743ec4e16456)

### 👩‍💻Implementing Natural Language Processing Models  
ViewerVoice covers the following areas of NLP driven by BERT based models.

- **Topic modelling** groups the comments into topics so that you can gain clearer insights into the key themes viewers are discussing in the comment section. For optimal performance of the current topic model, we recommend retrieving thousands of comments.

- **Sentiment analysis** identifies whether comments are positive, negative or neutral. This provides you with an overview of what viewers feel toward aspects of the content. Please note that at present, the sentiment analysis does not take emojis into account.

- **Semantic search** allows you to not only search for comments with exact matches to words, but also for comments that contain similar words. For example, if you search for 'music', comments containing 'music' as well as 'song' and 'vinyl' can show up. This feature enables you to search for specifics in a comment section - for example, perhaps you are a YouTuber that has collaborated with another creator or advertised for a brand you have partnered with, you can search for the name of the creator or brand in your comments to see how your viewers reacted to this.

### 📊Creating a Streamlit WebApp
Streamlit is an open-source Python library that enables the creation and sharing of data driven web applications. Leveraging Streamlit's versatile functions, we've tailored our dashboard to cover a range of essential features, such as:

- Interactive input widgets: allowing users to query their preferred videos and apply personalised filters.
- Comprehensive Python graphs: seamlessly integrating a variety of visualisations into the app.
- Custom HTML and CSS: offering the freedom to fine-tune the application's style to our preferences.

## 🔍Results  
We hope the insights provided by ViewerVoice will enable YouTubers to cater to their audience and use data-derived observations to negotiate opportunities and aid brands in gaining a deeper understanding of the intended audience of prospective partnerships. Future developments look to include but are not limited to improving the UI/UX design and implementing LLMs to give enhanced and more comprehensible results.
