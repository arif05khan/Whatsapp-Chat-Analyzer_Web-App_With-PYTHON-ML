import re
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def preprocess(data):
    # Regular expression for WhatsApp chat format
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    # Validate file format
    if not re.search(pattern, data):
        raise ValueError(
            "Invalid WhatsApp chat format. Expected format: 'MM/DD/YY, HH:MM - User: Message' or 'DD/MM/YY, HH:MM - User: Message'")

    # Split text into messages and dates
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Ensure messages and dates align
    if len(messages) != len(dates):
        raise ValueError("Mismatch between messages and dates in chat file.")

    # Create DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Convert date, supporting both formats
    try:
        df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ')
    except:
        try:
            df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %H:%M - ')
        except:
            raise ValueError("Date format not recognized. Use 'MM/DD/YY, HH:MM - ' or 'DD/MM/YY, HH:MM - '.")
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Extract user and message
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:  # User name exists
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:  # Group notification
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Extract time-based columns
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Create period column for heatmap
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period

    # Sentiment analysis with VADER
    sentiments = SentimentIntensityAnalyzer()
    df["po"] = df["message"].apply(lambda x: sentiments.polarity_scores(x)["pos"])
    df["ne"] = df["message"].apply(lambda x: sentiments.polarity_scores(x)["neg"])
    df["nu"] = df["message"].apply(lambda x: sentiments.polarity_scores(x)["neu"])

    # Determine overall sentiment value
    def sentiment(row):
        if row["po"] >= row["ne"] and row["po"] >= row["nu"]:
            return 1
        if row["ne"] >= row["po"] and row["ne"] >= row["nu"]:
            return -1
        if row["nu"] >= row["po"] and row["nu"] >= row["ne"]:
            return 0

    df['value'] = df.apply(sentiment, axis=1)

    return df
