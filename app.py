import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sn
import matplotlib.font_manager as font_manager
import emoji


st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        #Stats Area
        num_msgs, words, num_media_msgs, links = helper.fetch_stats(selected_user, df)
        st.title('Top Statistics')

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_msgs)

        with col2:
            st.header("Total words")
            st.title(words)

        with col3:
            st.header("Total Media Shared")
            st.title(num_media_msgs)

        with col4:
            st.header("Total Links Shared")
            st.title(links)


        #Timeline

        st.title('Daily Activity')
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title('Monthly Activity')
        timeline = helper.monthly_timeline(selected_user, df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'], color='purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Activity map

        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Active Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Active Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        #HeatMap
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots(figsize=(8,8))
        ax = sn.heatmap(user_heatmap)
        st.pyplot(fig)

        # For most active users (Group level only)
        if selected_user == 'Overall':
            st.title('Most Active Users')
            x, new_df = helper.most_active_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color = 'green')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        st.title("WordCloud")
        df_wc = helper.create_worldcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words

        st.title('Common Words')
        common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(common_df[0], common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #emoji analysis

        st.title('Emoji Analysis')
        emoji_df = helper.emoji_helper(selected_user, df)

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)



