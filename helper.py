from collections import Counter
import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_msgs = df.shape[0]
    words = []
    for msg in df['message']:
        words.extend(msg.split())

    num_media_shared = df[df['message'] == '<Media omitted>\n'].shape[0]


    # for total links shared
    extractor = URLExtract()

    links = []

    for link in df['message']:
        links.extend(extractor.find_urls(link))


    return num_msgs, len(words), num_media_shared, len(links)


def most_active_users(df):
    x = df['user'].value_counts().head()
    if len(x) <= 4:
        x = df['user'].value_counts().head(3)

    df = round((df['user'].value_counts()/ df.shape[0])*100, 2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})
    return x, df

def create_worldcloud(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = df[df['message'] != '<Media omitted>\n']

    def remove_stopwords(message):
        y=[]
        for msg in message.lower().split():
            if msg not in stop_words:
                y.append(msg)

        return" ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stopwords)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = df[df['message'] != '<Media omitted>\n']

    words = []
    for msg in temp['message']:
        for word in msg.lower().split():
            if word not in stop_words:
                words.append(word)

    common_df = pd.DataFrame(Counter(words).most_common(20))
    return common_df