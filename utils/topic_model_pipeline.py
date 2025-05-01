from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer
from bertopic import BERTopic
from bertopic.representation import MaximalMarginalRelevance
from bs4 import BeautifulSoup
import re
import string
import contractions
import html

## CLEANING
#video link id
def extract_video_id(url):
    # Regular expression pattern to match video IDs in various formats
    pattern = r'^(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/v\/)([A-Za-z0-9_-]+)'
    
    match = re.match(pattern, url)
    if match:
        return match.group(1)
    else:
        return None

#comment cleaning
def remove_punctuation(text, added_punc_to_remove = None, punc_kept = None):
    text = re.sub("’" , "'", text)
    text = re.sub("“" , '"', text)
    text = re.sub("”" , '"', text)
    remove = string.punctuation
    if added_punc_to_remove != None:
        for x in added_punc_to_remove:
            remove = remove + x
    if punc_kept != None:        
        for x in punc_kept:
            remove = remove.replace(x, "")
    pattern = r"[{}]".format(remove)
    text = re.sub(pattern, " ", text)
    return text

def remove_extra_space(text):
    text = re.sub("\s\s+" , " ", text)
    text = text.strip()
    return text

def non_ascii(s):
    return "".join(i for i in s if  ord(i)<128)#ord(i)>31 and

def html_to_string(text):
    text = html.unescape(text)
    text = BeautifulSoup(text, "html.parser").text
    return text

def expand_contractions(text):
    return contractions.fix(text)

def remove_digits(text):
    return re.sub(r"\d+", "", text)

def remove_new_lines(text):
    text = re.sub(r"\n", " ", text)
    text = re.sub(r"\r", " ", text)
    return text

def word_count(text):
    return len(text.split())

def char_length(text):
    return len(text)

def reduce_repeated_characters(text):
    # Define a regular expression pattern to match words with three or more repeated characters
    pattern = r'(\w+)\1{2,}'

    # Split the text into words 
    words = [x for x in text.split(' ')]

    # Replace three or more repeated characters with two repeated characters
    new_words = [re.sub(pattern, r'\1\1', word) for word in words]

    # Reconstruct the corrected text
    new_text = " ".join(new_words)

    return(new_text)

#topic model cleaning
def add_custom_stopwords(nlp, custom_stopwords):
    nlp.Defaults.stop_words |= set(custom_stopwords)

def remove_stopwords(text, nlp):
    doc = nlp(text)
    text = [token.text for token in doc if not token.is_stop] 
    text = " ".join(i for i in text)
    return text
def lemmatized_tokens(text, nlp):
    doc = nlp(text)
    text = [token.lemma_ if token.pos_ in ['NOUN', 'ADJ', 'VERB', 'ADV'] else token.text for token in doc]
    text = " ".join(i for i in text)
    return text
def minimum_length_cap(text, min_str_length = 3):
    text = [x for x in text.split(' ') if len(x) > min_str_length]
    text = " ".join(i for i in text)
    return text

## TOPIC MODELLING

def preprocess_topics(df, source_col, target_col, nlp, min_word_count = None):
    if min_word_count is not None:
        df[target_col] = df[source_col]
        df["Text_Len"] = df[target_col].apply(lambda x: word_count(x))
        df = df[df["Text_Len"] >= min_word_count]
        df.drop(columns = ["Text_Len"], inplace = True)
        df.reset_index(inplace=True, drop = True)
    
    df[target_col] = df[target_col].apply(lambda x: remove_punctuation(x))
    df[target_col] = df[target_col].apply(lambda x: lemmatized_tokens(x, nlp))
    df[target_col] = df[target_col].apply(lambda x: remove_stopwords(x, nlp))

    df[target_col] = df[target_col].apply(lambda x: minimum_length_cap(x))
    df[target_col] = df[target_col].apply(lambda x: " ".join(i for i in [x]))
    df[target_col] = df[target_col].apply(lambda x: x.replace('yt', ""))
    df[target_col] = df[target_col].apply(lambda x: x.replace('youtube', ""))
    df[target_col] = df[target_col].apply(lambda x: remove_extra_space(x))
    df = df[df[target_col] != '']
    df.reset_index(inplace=True)
    return df

def profanity_list(file_path = 'en_profane_words.txt'):
    try:
        with open(file_path, 'r') as file:
            # Step 3: Read the file line by line into a list
            word_list = [line.strip() for line in file]
    except FileNotFoundError:
        print("The specified file was not found.")
    except Exception as e:
        print("An error occurred:", e)
    return word_list


def bert_topic_model(data, tokens, embedding_model, max_topics = None):
    
    representation_model = MaximalMarginalRelevance(diversity=0.5)

    vectorizer = CountVectorizer(stop_words="english")
    umap_model = UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine', random_state = 7)
    hbscan_model = HDBSCAN(min_cluster_size=15, min_samples=2, metric='euclidean', cluster_selection_method='eom', prediction_data = True)
    model = BERTopic(representation_model=representation_model, embedding_model = embedding_model, umap_model = umap_model, hdbscan_model = hbscan_model, vectorizer_model=vectorizer)#, calculate_probabilities=True)
    embedded_data = embedding_model.encode(data[tokens])

    topics, probs = model.fit_transform(data[tokens], embedded_data)
    
    if -1 in topics:
        new_topics = model.reduce_outliers(data[tokens], topics, strategy="distributions")
        model.update_topics(data[tokens], topics=new_topics)
        topics, probs = model.topics_, model.probabilities_
    
    if max_topics < len(set(topics)):
        model.reduce_topics(data[tokens], nr_topics = max_topics)
        topics, probs = model.topics_, model.probabilities_
        
    model.update_topics(data[tokens],representation_model=representation_model)
    topic_labels = model.generate_topic_labels(nr_words=5, topic_prefix=False, separator=", ")
    if -1 in topics:
        topic_map = dict(zip(range(-1, len(topics)-1), topic_labels))
    else:
        topic_map = dict(zip(range(len(topics)), topic_labels))

    model.set_topic_labels(topic_map)
    topic_info = model.get_topic_info()
    
    return (topic_info, topic_map, topics, probs, model)
