from urlextract import URLExtract

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
    return x


