import spacy
import pickle
from transformers import pipeline
from sentence_transformers import SentenceTransformer


def add_custom_stopwords(nlp, custom_stopwords):
    nlp.Defaults.stop_words |= set(custom_stopwords)

with open("embedding_model.pickle", "wb") as f:
    pickle.dump(SentenceTransformer('flax-sentence-embeddings/all_datasets_v4_MiniLM-L6'), f)

with open("spacy_nlp.pickle", "wb") as f:
    nlp = spacy.load("en_core_web_sm")
    add_custom_stopwords(nlp, {"bring", "know", "come"})
    pickle.dump(nlp, f)