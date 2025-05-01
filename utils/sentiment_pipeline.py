def sentiment_model(text, sentiment_pipeline):
    sentiment_dict = sentiment_pipeline(text)
    label=sentiment_dict[0]['label']
    d = {'LABEL_0': 'Negative', 'LABEL_1': 'Neutral', 'LABEL_2': 'Positive'}
    label_mapped = d[label]
    return label_mapped

