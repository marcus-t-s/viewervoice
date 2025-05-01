import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from matplotlib import colormaps
from matplotlib.colors import ListedColormap


def comments_table(df, column_list, rename_dict=None, height=320, width=600, column_widths_ratio = [0.175,0.35,0.1,0.175, 0.2]):
    df = df[column_list]
    if rename_dict != None:
        df = df.rename(columns=rename_dict)
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    fill_color='#2661eb',
                    align='left',
                    font=dict(color='white')),
        cells=dict(values=[df[col] for col in df.columns],
                fill_color='#d9e9fc',
                align='left'),
        columnwidth=column_widths_ratio
    )])

    fig.update_layout(
        margin=dict(t=10, b=10, l=10, r=10),  # Adjust margins to fit the table within the figure
        width=width,  # Specify the width of the table
        height=height,  # Specify the height of the table
        paper_bgcolor='#eaf8ff',
        autosize = True
    )
    return fig


def generate_wordcloud(tokens, mask, colors):
    return WordCloud(mask=mask, colormap=colors, background_color='#eaf8ff', random_state=1999, width=300, height=300)\
        .generate_from_text(tokens)

def comment_wordcloud(df, mask, colors,  token_col='BERT_Token'):
    # Sample comment data for word cloud(
    comments = df[token_col].tolist()
    # Combine comments into a single string
    comment_text = " ".join(comments)
    # Generate a word cloud using ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        wordcloud_future = executor.submit(generate_wordcloud, comment_text, mask, colors)
        wordcloud = wordcloud_future.result()
    # Display the word cloud using matplotlib
    # fig, ax = plt.subplots(figsize=(12,8))
    # plt.figure(figsize=(6.25,3))
    plt.figure(frameon=False)
    # plt.gcf().patch.set_facecolor('#eaf8ff')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")  # Hide axes
    return plt.gcf()


def topic_treemap(df, topic_col, height=320, width=600):
    # Sample data (replace this with your actual dataset)
    value_counts_result = df[topic_col].value_counts()
    value_counts_df = pd.DataFrame({'Topic': value_counts_result.index, 'Count': value_counts_result.values})
    total_count = value_counts_df['Count'].sum()
    value_counts_df['Percentage'] = (value_counts_df['Count'] / total_count) * 100
    
    if value_counts_df['Topic'].nunique() == 1:
        value_counts_df = pd.DataFrame({'Topic': ['Root', value_counts_df['Topic'].iloc[0]], 'Count': [0, value_counts_df['Count'].iloc[0]], 'Percentage': [0, value_counts_df['Percentage'].iloc[0]]})

    fig = go.Figure(go.Treemap(
        labels=value_counts_df['Topic'],
        parents=[''] * len(value_counts_df),  # All topics are at the same level
        values=value_counts_df['Count'],
        root_color="#eaf8ff",
        hoverinfo='label+value+text',  # Display label, value, text, and customdata (percentage) in hover labels
        text=[f"{percentage:.2f}%" for percentage in value_counts_df['Percentage']],
        hovertemplate='<b>Topic:</b> %{label}<br><b>Count:</b> %{value}<br><b>Percentage:</b> %{customdata:.2f}%<extra></extra>',
        customdata=value_counts_df['Percentage'],
    ))
    fig.update_layout(coloraxis_showscale=False,
    margin=dict(t=0, b=0, l=0, r=0),  # Adjust the margins to fill the space
        width=width,  # Adjust the width of the chart
        height=height, # Adjust the height of the chart)
        paper_bgcolor='#eaf8ff',
        treemapcolorway =['#2b67e0','#17bece','#77e6d4','#abe0ff', '#2692f0','#2849bf', '#3acf96', '#2aad9e','#b6f5fc', '#68cbfc' ],
    )
    fig.data[0].hovertemplate = ''
    return fig


def sentiment_chart(df, sentiment_col, height=320, width=400):
    # Create a dataframe
    value_counts_result = df[sentiment_col].value_counts()
    value_counts_df = pd.DataFrame({'Sentiment': value_counts_result.index, 'Count': value_counts_result.values})
    total_count = value_counts_df['Count'].sum()
    value_counts_df['Percentage'] = (value_counts_df['Count'] / total_count) * 100
    # Create a figure with custom color mapping and template
    fig = px.pie(
        value_counts_df,
        values='Count',
        names='Sentiment',
        hole=0.7,
        color='Sentiment',
        color_discrete_map={'Positive': '#00cc96', 'Neutral': '#ffee58', 'Negative': '#ef553b'},
        template='plotly'  # Use the 'plotly' template
    )
    fig.update_traces(
        textinfo='percent+label+value',  # Display percentage, label, and value
        hovertemplate='%{label}<br>Count: %{value}<br>Percentage: %{percent}',
        textposition='outside',    # Place labels outside the chart
        textfont=dict(size=14)
    )
    fig.update_layout(showlegend=False,
                width=width,  # Adjust the width of the chart
                height=height, # Adjust the height of the chart
                paper_bgcolor='#eaf8ff'
    )
    return fig
