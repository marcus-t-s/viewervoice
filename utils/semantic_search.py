# import streamlit as st
import numpy as np
from sentence_transformers import SentenceTransformer, util

# Define a function for semantic search
def semantic_search(df, query, embedding_model, text_col, threshold=0.40):
    # Encode the search query
    query_embedding = embedding_model.encode(query, convert_to_tensor=True)

    # Encode all comments
    comment_embeddings = embedding_model.encode(df[text_col].tolist(), convert_to_tensor=True)

    # Compute cosine similarities between query and comments
    cosine_scores = util.pytorch_cos_sim(query_embedding, comment_embeddings)[0]

    # Convert cosine_scores to a NumPy array
    cosine_scores_np = cosine_scores.cpu().numpy()

    # Find indices of comments above the similarity threshold
    similar_indices = np.where(cosine_scores_np > threshold)[0]

    # Select similar comments using the indices
    similar_text = df.iloc[similar_indices]

    return similar_text
