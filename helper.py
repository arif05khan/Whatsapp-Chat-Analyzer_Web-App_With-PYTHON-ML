from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()

# Chat Analysis Functions
def chat_fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['user'] != 'group_notification'].copy()  # Exclude group notifications
    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())
    num_media_messages = df[df['message'].str.contains('<Media omitted>', na=False)].shape[0]
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(str(message)))
    return num_messages, len(words), num_media_messages, len(links)

def chat_most_busy_users(df):
    df = df[df['user'] != 'group_notification'].copy()
    if df.empty:
        return pd.Series(), pd.DataFrame()
    x = df['user'].value_counts()
    df_percent = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'Name', 'user': 'Percent'})
    return x, df_percent

def chat_create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['user'] != 'group_notification'].copy()
    df = df[~df['message'].str.contains('<Media omitted>', na=False)].copy()
    if df.empty:
        return None
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def chat_most_common_words(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification'].copy()
    temp = temp[~temp['message'].str.contains('<Media omitted>', na=False)].copy()
    if temp.empty:
        return pd.DataFrame()
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def chat_emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['user'] != 'group_notification'].copy()
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in str(message) if c in emoji.EMOJI_DATA])
    if not emojis:
        return pd.DataFrame()
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def emoji_contribution(df):
    df = df[df['user'] != 'group_notification'].copy()
    if df.empty:
        return pd.DataFrame()
    emoji_counts = []
    for user in df['user'].unique():
        user_df = df[df['user'] == user]
        emojis = []
        for message in user_df['message']:
            emojis.extend([c for c in str(message) if c in emoji.EMOJI_DATA])
        emoji_counts.append({'user': user, 'emoji_count': len(emojis)})
    emoji_contribution_df = pd.DataFrame(emoji_counts)
    if not emoji_contribution_df.empty:
        emoji_contribution_df = emoji_contribution_df.sort_values(by='emoji_count', ascending=False)
    return emoji_contribution_df

def chat_monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['user'] != 'group_notification'].copy()
    if df.empty:
        return pd.DataFrame()
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def chat_daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['user'] != 'group_notification'].copy()
    if df.empty:
        return pd.DataFrame()
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def chat_week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['user'] != 'group_notification'].copy()
    if df.empty:
        return pd.Series(), None
    week_activity = df['day_name'].value_counts()
    all_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    week_activity = week_activity.reindex(all_days, fill_value=0)
    most_active_day = week_activity.idxmax() if not week_activity.empty else None
    return week_activity, most_active_day

def chat_month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['user'] != 'group_notification'].copy()
    if df.empty:
        return pd.Series(), None
    month_activity = df['month'].value_counts()
    all_months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    month_activity = month_activity.reindex(all_months, fill_value=0)
    most_active_month = month_activity.idxmax() if not month_activity.empty else None
    return month_activity, most_active_month

def chat_activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['user'] != 'group_notification'].copy()
    if df.empty:
        return pd.DataFrame(), None, None, []
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    max_value = user_heatmap.values.max()
    if max_value == 0:
        return user_heatmap, None, None, []
    max_idx = user_heatmap.stack().idxmax()
    most_active_day, most_active_period = max_idx
    all_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    most_busy_hours = []
    for day in all_days:
        if day in user_heatmap.index:
            day_data = user_heatmap.loc[day]
            if day_data.sum() > 0:
                most_active_hour = day_data.idxmax()
                message_count = int(day_data.max())
            else:
                most_active_hour = "No Activity"
                message_count = 0
        else:
            most_active_hour = "No Activity"
            message_count = 0
        most_busy_hours.append([day, most_active_hour, message_count])
    return user_heatmap, most_active_day, most_active_period, most_busy_hours

def user_activity_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['user'] != 'group_notification'].copy()
    if df.empty:
        return pd.DataFrame()
    timeline = df.groupby('hour').count()['message'].reset_index()
    def convert_to_12hour(hour):
        if hour == 0:
            return "12 AM"
        elif hour == 12:
            return "12 PM"
        elif hour > 12:
            return f"{hour - 12} PM"
        else:
            return f"{hour} AM"
    timeline['hour_12'] = timeline['hour'].apply(convert_to_12hour)
    timeline = timeline.sort_values('hour')
    return timeline

def response_time_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['user'] != 'group_notification'].copy()
    if len(df) < 2:
        return pd.DataFrame(), pd.DataFrame()
    df = df.sort_values('date')
    df['time_diff'] = df['date'].diff().dt.total_seconds() / 60
    df['prev_user'] = df['user'].shift(1)
    response_times = df[df['user'] != df['prev_user']].copy()
    if response_times.empty:
        return pd.DataFrame(), pd.DataFrame()
    avg_response_time = response_times.groupby('user')['time_diff'].mean().reset_index()
    avg_response_time['time_diff'] = avg_response_time['time_diff'].round(2)
    avg_response_time.rename(columns={'time_diff': 'avg_response_time_minutes'}, inplace=True)
    timeline = response_times.groupby('only_date')['time_diff'].mean().reset_index()
    timeline['time_diff'] = timeline['time_diff'].round(2)
    timeline.rename(columns={'time_diff': 'avg_response_time_minutes'}, inplace=True)
    return avg_response_time, timeline

# Sentiment Analysis Functions
def sentiment_week_activity_map(selected_user, df, k):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['value'] == k].copy()
    df = df[df['user'] != 'group_notification'].copy()
    if df.empty:
        return pd.Series()
    return df['day_name'].value_counts()

def sentiment_month_activity_map(selected_user, df, k):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['value'] == k].copy()
    df = df[df['user'] != 'group_notification'].copy()
    if df.empty:
        return pd.Series()
    return df['month'].value_counts()

def sentiment_activity_heatmap(selected_user, df, k):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['value'] == k].copy()
    df = df[df['user'] != 'group_notification'].copy()
    if df.empty:
        return pd.DataFrame()
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap

def sentiment_daily_timeline(selected_user, df, k):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['value'] == k].copy()
    df = df[df['user'] != 'group_notification'].copy()
    if df.empty:
        return pd.DataFrame()
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def sentiment_monthly_timeline(selected_user, df, k):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['value'] == k].copy()
    df = df[df['user'] != 'group_notification'].copy()
    if df.empty:
        return pd.DataFrame()
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def sentiment_percentage(df, k):
    df_filtered = df[df['value'] == k].copy()
    df_filtered = df_filtered[df_filtered['user'] != 'group_notification'].copy()
    if df_filtered.empty:
        return pd.DataFrame()
    df_result = round((df_filtered['user'].value_counts() / df_filtered.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return df_result

def sentiment_create_wordcloud(selected_user, df, k):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification'].copy()
    temp = temp[~temp['message'].str.contains('<Media omitted>', na=False)].copy()
    def remove_stop_words(message):
        y = []
        for word in str(message).lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    temp = temp[temp['value'] == k].copy()
    if temp.empty:
        return None
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def sentiment_most_common_words(selected_user, df, k):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification'].copy()
    temp = temp[~temp['message'].str.contains('<Media omitted>', na=False)].copy()
    if temp.empty:
        return pd.DataFrame()
    words = []
    for message in temp['message'][temp['value'] == k]:
        for word in str(message).lower().split():
            if word not in stop_words:
                words.append(word)
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def sentiment_trend(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['user'] != 'group_notification'].copy()
    if df.empty:
        return pd.DataFrame()
    pos = df[df['value'] == 1].groupby(['year', 'month_num', 'month']).count()['message'].reset_index(name='Positive')
    neu = df[df['value'] == 0].groupby(['year', 'month_num', 'month']).count()['message'].reset_index(name='Neutral')
    neg = df[df['value'] == -1].groupby(['year', 'month_num', 'month']).count()['message'].reset_index(name='Negative')
    merged = pos.merge(neu, on=['year', 'month_num', 'month'], how='outer').merge(
        neg, on=['year', 'month_num', 'month'], how='outer').fillna(0)
    time = []
    for i in range(merged.shape[0]):
        time.append(merged['month'][i] + "-" + str(merged['year'][i]))
    merged['time'] = time
    return merged[['time', 'Positive', 'Neutral', 'Negative']]

def sentiment_intensity_distribution(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['user'] != 'group_notification'].copy()
    if df.empty:
        return pd.DataFrame()
    intensity_data = {
        'Positive': df['po'],
        'Negative': df['ne'],
        'Neutral': df['nu']
    }
    return pd.DataFrame(intensity_data)

def sentiment_transition_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['user'] != 'group_notification'].copy()
    if len(df) < 2:
        return pd.DataFrame()
    transitions = []
    sentiment_labels = {1: 'Positive', 0: 'Neutral', -1: 'Negative'}
    for i in range(len(df) - 1):
        current_sentiment = df['value'].iloc[i]
        next_sentiment = df['value'].iloc[i + 1]
        if pd.notna(current_sentiment) and pd.notna(next_sentiment):
            transition = f"{sentiment_labels[current_sentiment]} -> {sentiment_labels[next_sentiment]}"
            transitions.append(transition)
    transition_counts = Counter(transitions)
    transition_df = pd.DataFrame.from_dict(transition_counts, orient='index', columns=['Count']).reset_index()
    transition_df.rename(columns={'index': 'Transition'}, inplace=True)
    transition_df = transition_df.sort_values(by='Count', ascending=False)
    return transition_df

def sentiment_by_message_length(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['user'] != 'group_notification'].copy()
    df = df[~df['message'].str.contains('<Media omitted>', na=False)].copy()
    if df.empty:
        return pd.DataFrame()
    df['msg_length'] = df['message'].str.len()
    sentiment_labels = {1: 'Positive', 0: 'Neutral', -1: 'Negative'}
    df['sentiment_label'] = df['value'].map(sentiment_labels)
    avg_length = df.groupby('sentiment_label')['msg_length'].mean().round(2).reset_index()
    return avg_length

def sentiment_emoji_correlation(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['user'] != 'group_notification'].copy()
    if df.empty:
        return pd.DataFrame()
    sentiment_labels = {1: 'Positive', 0: 'Neutral', -1: 'Negative'}
    results = []
    for sentiment_value, sentiment_label in sentiment_labels.items():
        sentiment_df = df[df['value'] == sentiment_value]
        emojis = []
        for message in sentiment_df['message']:
            emojis.extend([c for c in str(message) if c in emoji.EMOJI_DATA])
        if emojis:
            emoji_counts = Counter(emojis).most_common(5)
            for emoji_char, count in emoji_counts:
                results.append({
                    'Sentiment': sentiment_label,
                    'Emoji': emoji_char,
                    'Count': count
                })
    return pd.DataFrame(results)

# Keyword Analysis Functions
def keyword_search(selected_user, df, keyword):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['user'] != 'group_notification'].copy()
    if df.empty:
        return pd.DataFrame()
    keyword_df = df[df['message'].str.contains(keyword, case=False, na=False)]
    return keyword_df

def keyword_timeline(selected_user, df, keyword):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['user'] != 'group_notification'].copy()
    if df.empty:
        return pd.DataFrame()
    keyword_df = df[df['message'].str.contains(keyword, case=False, na=False)]
    if keyword_df.empty:
        return pd.DataFrame()
    timeline = keyword_df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    timeline['count'] = timeline['message']
    return timeline

# Message Length Analysis Functions
def message_length_by_user(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['user'] != 'group_notification'].copy()
    df = df[~df['message'].str.contains('<Media omitted>', na=False)].copy()
    if df.empty:
        return pd.DataFrame()
    df['msg_length'] = df['message'].str.len()
    length_df = df.groupby('user')['msg_length'].mean().reset_index(name='avg_length').round(2)
    return length_df

def message_length_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['user'] != 'group_notification'].copy()
    df = df[~df['message'].str.contains('<Media omitted>', na=False)].copy()
    if df.empty:
        return pd.DataFrame()
    df['msg_length'] = df['message'].str.len()
    timeline = df.groupby(['year', 'month_num', 'month'])['msg_length'].mean().reset_index(name='avg_length')
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    timeline['avg_length'] = timeline['avg_length'].round(2)
    return timeline

def message_length_distribution(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['user'] != 'group_notification'].copy()
    df = df[~df['message'].str.contains('<Media omitted>', na=False)].copy()
    if df.empty:
        return pd.Series()
    df['msg_length'] = df['message'].str.len()
    return df['msg_length']

def message_length_by_sentiment(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['user'] != 'group_notification'].copy()
    df = df[~df['message'].str.contains('<Media omitted>', na=False)].copy()
    if df.empty:
        return pd.DataFrame()
    df['msg_length'] = df['message'].str.len()
    sentiment_labels = {1: 'Positive', 0: 'Neutral', -1: 'Negative'}
    df['sentiment_label'] = df['value'].map(sentiment_labels)
    avg_length = df.groupby('sentiment_label')['msg_length'].mean().round(2).reset_index()
    return avg_length

def message_length_by_day_of_week(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['user'] != 'group_notification'].copy()
    df = df[~df['message'].str.contains('<Media omitted>', na=False)].copy()
    if df.empty:
        return pd.DataFrame()
    df['msg_length'] = df['message'].str.len()
    all_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    avg_length = df.groupby('day_name')['msg_length'].mean().round(2).reindex(all_days, fill_value=0)
    return avg_length.reset_index()

def extreme_messages(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['user'] != 'group_notification'].copy()
    df = df[~df['message'].str.contains('<Media omitted>', na=False)].copy()
    if df.empty:
        return pd.DataFrame(), pd.DataFrame()
    df['msg_length'] = df['message'].str.len()
    # Longest messages (top 5)
    longest = df.nlargest(5, 'msg_length')[['date', 'user', 'message', 'msg_length']]
    # Shortest messages (top 5, excluding zero-length messages)
    shortest = df[df['msg_length'] > 0].nsmallest(5, 'msg_length')[['date', 'user', 'message', 'msg_length']]
    return longest, shortest
