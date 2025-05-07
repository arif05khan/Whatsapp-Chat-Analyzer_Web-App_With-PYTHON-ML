import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import nltk
import plotly.express as px
from datetime import datetime
import re
import plotly.graph_objects as go
import plotly.figure_factory as ff

# Download NLTK data for VADER
nltk.download('vader_lexicon')

# Initialize session state for theme and analysis
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'show_analysis' not in st.session_state:
    st.session_state.show_analysis = False

# Custom CSS for styling with light/dark mode
st.markdown(
    """
    <style>
    .title-container {
        background-color: var(--title-bg);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .app-title {
        font-size: 48px;
        font-weight: bold;
        color: var(--text-color);
        margin-bottom: 10px;
        font-family: 'Arial', sans-serif;
    }
    .app-tagline {
        font-size: 18px;
        color: var(--tagline-color);
        font-style: italic;
        margin-bottom: 20px;
    }
    .custom-table {
        width: 50%;
        margin: 0 auto;
        border-collapse: collapse;
        font-size: 18px;
        font-family: 'Arial', sans-serif;
    }
    .custom-table th, .custom-table td {
        padding: 12px 15px;
        text-align: left;
        border-bottom: 1px solid var(--border-color);
    }
    .custom-table th {
        background-color: var(--table-header-bg);
        font-weight: bold;
        color: var(--text-color);
    }
    .custom-table td {
        color: var(--text-color);
    }
    .custom-table tr:hover {
        background-color: var(--table-hover-bg);
    }
    div.stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    div.stTabs [data-baseweb="tab"] {
        font-size: 20px;
        font-weight: bold;
        padding: 15px 30px;
        background-color: var(--tab-bg);
        color: var(--tab-text);
        border-radius: 10px;
        border: 2px solid var(--tab-border);
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    div.stTabs [data-baseweb="tab"]:hover {
        background-color: var(--tab-hover-bg);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    div.stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: var(--tab-active-bg);
        color: white;
        border: 2px solid var(--tab-active-border);
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    }
    .emoji-section-title {
        font-size: 28px;
        font-weight: bold;
        color: var(--text-color);
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    :root {
        --title-bg: #f0f2f6;
        --text-color: #2c3e50;
        --tagline-color: #7f8c8d;
        --border-color: #ddd;
        --table-header-bg: #f0f2f6;
        --table-hover-bg: #f5f5f5;
        --tab-bg: #e0e7ff;
        --tab-text: #1e3a8a;
        --tab-border: #c7d2fe;
        --tab-hover-bg: #c7d2fe;
        --tab-active-bg: #4f46e5;
        --tab-active-border: #4338ca;
        --bg-color: #ffffff;
        --sidebar-bg: #f8f9fa;
    }
    [data-theme="dark"] {
        --title-bg: #1e293b;
        --text-color: #e2e8f0;
        --tagline-color: #94a3b8;
        --border-color: #4b5563;
        --table-header-bg: #334155;
        --table-hover-bg: #475569;
        --tab-bg: #3b82f6;
        --tab-text: #dbeafe;
        --tab-border: #60a5fa;
        --tab-hover-bg: #2563eb;
        --tab-active-bg: #1e40af;
        --tab-active-border: #1e3a8a;
        --bg-color: #0f172a;
        --sidebar-bg: #1e293b;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Apply theme
st.markdown(
    f'<body data-theme="{st.session_state.theme}"></body>',
    unsafe_allow_html=True
)

# Theme toggle
st.sidebar.checkbox(
    "Dark Mode",
    value=st.session_state.theme == 'dark',
    on_change=lambda: st.session_state.update(
        theme='dark' if st.session_state.theme == 'light' else 'light'
    )
)

# Styled title section with image
st.markdown(
    """
    <div class="title-container">
        <div class="app-title">WhatsApp Chat & Sentiment Analyzer</div>
        <div class="app-tagline">Analyze chats, sentiments, keywords, and activity patterns with ease!</div>
    </div>
    """,
    unsafe_allow_html=True
)

# Add the WhatsApp logo image below the title
st.image("WhatsApp_SCREEN.png")

# Sidebar
st.sidebar.title("WhatsApp Chat & Sentiment Analyzer")

# File uploader
uploaded_file = st.sidebar.file_uploader(
    "Choose a WhatsApp chat file (.txt)",
    type="txt"
)

# Cache the preprocessing function
@st.cache_data
def cached_preprocess(chat_data):
    return preprocessor.preprocess(chat_data)

# Date range filter and keyword search
st.sidebar.subheader("Date Range Filter")
min_date = datetime(2010, 1, 1)
max_date = datetime.now()
start_date = st.sidebar.date_input(
    "Start Date", min_date, min_value=min_date, max_value=max_date
)
end_date = st.sidebar.date_input(
    "End Date", max_date, min_value=min_date, max_value=max_date
)
keyword = st.sidebar.text_input("Search for a keyword (optional)", "")

# Main logic
df = None
if uploaded_file is not None:
    try:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        df = cached_preprocess(data)
    except UnicodeDecodeError as e:
        st.error(
            f"Error decoding file: {str(e)}. Please ensure the file is a "
            "valid WhatsApp chat export in .txt format with UTF-8 encoding."
        )
        st.stop()
    except ValueError as e:
        st.error(
            f"Error processing file: {str(e)}. Please ensure the file format "
            "matches WhatsApp chat export format."
        )
        st.stop()

    # Apply date range filter
    if start_date and end_date:
        df = df[(df['only_date'] >= start_date) & (df['only_date'] <= end_date)]
        if df.empty:
            st.warning("No messages found in the selected date range. Please adjust the dates.")
            st.stop()

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    user_list = [user for user in user_list if user != 'group_notification']
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis for", user_list)

    # Show Analysis button
    if st.sidebar.button("Show Analysis"):
        st.session_state.show_analysis = True

    # Always render tabs to ensure reactivity
    tab1, tab2, tab3, tab4 = st.tabs([
        "Chat Analysis", "Sentiment Analysis",
        "Keyword Analysis", "Message Length Analysis"
    ])

    # Chat Analysis Tab
    with tab1:
        if st.session_state.show_analysis:
            st.title("Top Statistics")
            try:
                num_messages, words, num_media_messages, num_links = helper.chat_fetch_stats(selected_user, df)
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.header("Total Messages")
                    st.title(num_messages)
                with col2:
                    st.header("Total Words")
                    st.title(words)
                with col3:
                    st.header("Media Shared")
                    st.title(num_media_messages)
                with col4:
                    st.header("Links Shared")
                    st.title(num_links)
            except Exception as e:
                st.error(f"Error computing top statistics: {str(e)}")
                num_messages, words, num_media_messages, num_links = 0, 0, 0, 0

            # User Activity Timeline
            st.title("User Activity Timeline")
            try:
                activity_timeline = helper.user_activity_timeline(selected_user, df)
                if not activity_timeline.empty:
                    fig = px.bar(
                        activity_timeline, x='hour_12', y='message',
                        title='Messages by Hour of Day',
                        color='message', color_continuous_scale='Blues'
                    )
                    fig.update_layout(xaxis_title='Hour of Day', yaxis_title='Message Count')
                    st.plotly_chart(fig)
                else:
                    st.info("No activity data available for the selected user.")
            except Exception as e:
                st.error(f"Error generating user activity timeline: {str(e)}")

            # Response Time Analysis
            st.title("Response Time Analysis")
            st.markdown("This shows the average time (in minutes) between responses for each user, indicating their responsiveness.")
            try:
                avg_response_df, timeline_df = helper.response_time_analysis(selected_user, df)
                if not avg_response_df.empty:
                    avg_response_df.index = avg_response_df.index + 1
                    fig = px.bar(
                        avg_response_df,
                        x='user',
                        y='avg_response_time_minutes',
                        title='Average Response Time per User',
                        color='avg_response_time_minutes',
                        color_continuous_scale='Reds'
                    )
                    fig.update_layout(
                        xaxis_title='User',
                        yaxis_title='Average Response Time (Minutes)',
                        xaxis_tickangle=45
                    )
                    st.plotly_chart(fig)

                    st.header("Response Time Over Time")
                    fig = px.line(
                        timeline_df,
                        x='only_date',
                        y='avg_response_time_minutes',
                        title='Average Response Time Over Time',
                        color_discrete_sequence=['purple']
                    )
                    fig.update_layout(
                        xaxis_title='Date',
                        yaxis_title='Average Response Time (Minutes)',
                        xaxis_tickangle=45
                    )
                    st.plotly_chart(fig)

                    st.subheader("Response Time Details")
                    st.dataframe(avg_response_df, use_container_width=True)
                else:
                    st.info("Not enough data to compute response times (requires at least two messages with user interactions).")
            except Exception as e:
                st.error(f"Error generating response time analysis: {str(e)}")

            # Activity Maps
            st.title('Activity Maps')
            st.header("Weekly Activity Chart")
            try:
                busy_day, most_active_day = helper.chat_week_activity_map(selected_user, df)
                if not busy_day.empty:
                    fig = go.Figure()
                    colors = ['#FF9999' if day != most_active_day else '#FF3333' for day in busy_day.index]
                    fig.add_trace(go.Bar(
                        x=busy_day.index,
                        y=busy_day.values,
                        marker_color=colors,
                        text=[f'{val}' if day == most_active_day else '' for day, val in zip(busy_day.index, busy_day.values)],
                        textposition='auto'
                    ))
                    fig.update_layout(
                        title=f'Most Active Day: {most_active_day}',
                        xaxis_title='Day of Week',
                        yaxis_title='Message Count',
                        xaxis_tickangle=45
                    )
                    st.plotly_chart(fig)
                else:
                    st.info("No weekly activity data available.")
            except Exception as e:
                st.error(f"Error generating weekly activity chart: {str(e)}")

            st.header("Monthly Activity Chart")
            try:
                busy_month, most_active_month = helper.chat_month_activity_map(selected_user, df)
                if not busy_month.empty:
                    fig = go.Figure()
                    colors = ['#99CCFF' if month != most_active_month else '#3366CC' for month in busy_month.index]
                    fig.add_trace(go.Bar(
                        x=busy_month.index,
                        y=busy_month.values,
                        marker_color=colors,
                        text=[f'{val}' if month == most_active_month else '' for month, val in zip(busy_month.index, busy_month.values)],
                        textposition='auto'
                    ))
                    fig.update_layout(
                        title=f'Most Active Month: {most_active_month}',
                        xaxis_title='Month',
                        yaxis_title='Message Count',
                        xaxis_tickangle=45
                    )
                    st.plotly_chart(fig)
                else:
                    st.info("No monthly activity data available.")
            except Exception as e:
                st.error(f"Error generating monthly activity chart: {str(e)}")

            # Weekly Activity Heatmap
            st.header("Weekly Activity Heatmap")
            try:
                user_heatmap, most_active_day, most_active_period, most_busy_hours = helper.chat_activity_heatmap(selected_user, df)
                if not user_heatmap.empty:
                    fig = go.Figure(data=go.Heatmap(
                        z=user_heatmap.values,
                        x=user_heatmap.columns,
                        y=user_heatmap.index,
                        colorscale='Viridis',
                        text=user_heatmap.values,
                        texttemplate="%{text}",
                        textfont={"size": 12}
                    ))
                    fig.update_layout(
                        title=f'Most Active Time: {most_active_day} {most_active_period}' if most_active_day else 'No Activity',
                        xaxis_title='Time Period',
                        yaxis_title='Day of Week',
                        xaxis_tickangle=45,
                        height=500
                    )
                    st.plotly_chart(fig)

                    # Display Most Busy Hour for Each Day
                    st.subheader("Most Active Hour for Each Day")
                    most_busy_hours_df = pd.DataFrame(most_busy_hours, columns=['Day', 'Most Active Hour', 'Message Count'])
                    most_busy_hours_df.index = most_busy_hours_df.index + 1
                    st.dataframe(most_busy_hours_df, use_container_width=True)
                else:
                    st.info("No activity data available for heatmap.")
            except Exception as e:
                st.error(f"Error generating weekly activity heatmap: {str(e)}")

            # Busiest Users (Group Level)
            if selected_user == 'Overall':
                st.markdown(
                    '<div class="emoji-section-title">Most Busy Users</div>',
                    unsafe_allow_html=True
                )
                try:
                    x, _ = helper.chat_most_busy_users(df)
                    if not x.empty:
                        total_messages = x.sum()
                        percentages = (x / total_messages * 100).round(2)
                        top_n = 10
                        major_users = x.head(top_n)
                        others_count = x.iloc[top_n:].sum() if len(x) > top_n else 0
                        if others_count > 0:
                            plot_series = pd.Series(
                                data=list(major_users.values) + [others_count],
                                index=list(major_users.index) + ['Others']
                            )
                        else:
                            plot_series = major_users
                        colors = [
                            '#4B0082', '#8B008B', '#FF4040', '#FF8C00', '#1E90FF',
                            '#00CED1', '#228B22', '#FFD700', '#FF69B4', '#4682B4',
                            '#800000'
                        ]
                        fig, ax_busy_users = plt.subplots(figsize=(12, 6))
                        bars = ax_busy_users.bar(
                            range(len(plot_series)),
                            plot_series.values,
                            color=colors[:len(plot_series)]
                        )
                        ax_busy_users.set_xticks(range(len(plot_series)))
                        ax_busy_users.set_xticklabels(
                            plot_series.index,
                            rotation=45,
                            ha='right',
                            fontsize=10
                        )
                        for bar in bars:
                            height = bar.get_height()
                            ax_busy_users.text(
                                bar.get_x() + bar.get_width()/2.,
                                height + 2,
                                f'{int(height)}',
                                ha='center',
                                va='bottom',
                                fontsize=10
                            )
                        ax_busy_users.set_xlabel('Users', fontsize=12)
                        ax_busy_users.set_ylabel('Message Count', fontsize=12)
                        ax_busy_users.set_title('Top 10 Most Busy Users', fontsize=14, pad=15)
                        plt.tight_layout()
                        st.pyplot(fig)

                        st.subheader("Busy Users Details")
                        table_df = pd.DataFrame({
                            'User': x.index,
                            'Message Count': x.values,
                            'Percent': percentages
                        }).reset_index(drop=True)
                        table_df.index = table_df.index + 1
                        table_df = table_df.sort_values(by='Message Count', ascending=False)
                        st.dataframe(table_df, use_container_width=True)
                    else:
                        st.info("No user activity data available.")
                except Exception as e:
                    st.error(f"Error generating most busy users: {str(e)}")

            # Emoji Contribution
            if selected_user == 'Overall':
                st.markdown(
                    '<div class="emoji-section-title">Emoji Contribution by User</div>',
                    unsafe_allow_html=True
                )
                try:
                    emoji_contribution_df = helper.emoji_contribution(df)
                    if not emoji_contribution_df.empty:
                        total_emojis = emoji_contribution_df['emoji_count'].sum()
                        emoji_contribution_df['percentage'] = (emoji_contribution_df['emoji_count'] / total_emojis * 100).round(2)
                        threshold = 5.0
                        major_df = emoji_contribution_df[emoji_contribution_df['percentage'] >= threshold]
                        others_df = emoji_contribution_df[emoji_contribution_df['percentage'] < threshold]
                        if not others_df.empty:
                            others_count = others_df['emoji_count'].sum()
                            others_percentage = (others_count / total_emojis * 100).round(2)
                            others_row = pd.DataFrame({
                                'user': ['Others'],
                                'emoji_count': [others_count],
                                'percentage': [others_percentage]
                            })
                            plot_df = pd.concat([major_df, others_row], ignore_index=True)
                        else:
                            plot_df = emoji_contribution_df
                        fig, ax_emoji = plt.subplots(figsize=(10, 8))
                        explode = [0.05] * len(plot_df)
                        ax_emoji.pie(
                            plot_df['emoji_count'],
                            labels=None,
                            autopct='%1.2f%%',
                            colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f'][:len(plot_df)],
                            startangle=90,
                            explode=explode,
                            pctdistance=0.85,
                            textprops={'fontsize': 12}
                        )
                        ax_emoji.legend(
                            labels=plot_df['user'],
                            title="Users",
                            loc="center left",
                            bbox_to_anchor=(1, 0, 0.5, 1),
                            fontsize=12
                        )
                        ax_emoji.set_title('Number of Emojis Sent by Each User', fontsize=16, pad=20)
                        plt.tight_layout()
                        st.pyplot(fig)

                        st.subheader("Emoji Contribution Details")
                        emoji_table_df = emoji_contribution_df.sort_values(by='emoji_count', ascending=False)
                        emoji_table_df = emoji_table_df[['user', 'emoji_count']].rename(
                            columns={'user': 'User', 'emoji_count': 'Emoji Count'}
                        ).reset_index(drop=True)
                        emoji_table_df.index = emoji_table_df.index + 1
                        st.dataframe(emoji_table_df, use_container_width=True)
                    else:
                        st.info("No emojis found in the chat.")
                except Exception as e:
                    st.error(f"Error generating emoji contribution: {str(e)}")

            # WordCloud
            st.title("Wordcloud")
            try:
                df_wc = helper.chat_create_wordcloud(selected_user, df)
                if df_wc:
                    fig, ax_wordcloud = plt.subplots()
                    ax_wordcloud.imshow(df_wc)
                    ax_wordcloud.axis('off')
                    st.pyplot(fig)
                else:
                    st.info("No words available to generate a wordcloud.")
            except Exception as e:
                st.error(f"Error generating wordcloud: {str(e)}")

            # Most Common Words
            st.title('Most Common Words')
            try:
                most_common_df = helper.chat_most_common_words(selected_user, df)
                if not most_common_df.empty:
                    most_common_df.index = most_common_df.index + 1
                    fig, ax_common_words = plt.subplots()
                    ax_common_words.barh(most_common_df[0], most_common_df[1])
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                else:
                    st.info("No common words found.")
            except Exception as e:
                st.error(f"Error generating most common words: {str(e)}")

            # Emoji Analysis
            st.title("Emoji Analysis")
            try:
                emoji_df = helper.chat_emoji_helper(selected_user, df)
                if not emoji_df.empty:
                    emoji_df.index = emoji_df.index + 1
                    col1, col2 = st.columns(2)
                    with col1:
                        st.dataframe(emoji_df)
                    with col2:
                        fig, ax_emoji = plt.subplots()
                        ax_emoji.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%1.2f%%")
                        st.pyplot(fig)
                else:
                    st.info("No emojis found in the chat.")
            except Exception as e:
                st.error(f"Error generating emoji analysis: {str(e)}")

            # Monthly Timeline
            st.title("Monthly Timeline")
            try:
                timeline = helper.chat_monthly_timeline(selected_user, df)
                if not timeline.empty:
                    fig = px.line(
                        timeline, x='time', y='message', title='Messages Over Time',
                        color_discrete_sequence=['green']
                    )
                    fig.update_layout(xaxis_tickangle=45)
                    st.plotly_chart(fig)
                else:
                    st.info("No monthly timeline data available.")
            except Exception as e:
                st.error(f"Error generating monthly timeline: {str(e)}")

            # Daily Timeline
            st.title("Daily Timeline")
            try:
                daily_timeline = helper.chat_daily_timeline(selected_user, df)
                if not daily_timeline.empty:
                    fig, ax_daily = plt.subplots()
                    ax_daily.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                else:
                    st.info("No daily timeline data available.")
            except Exception as e:
                st.error(f"Error generating daily timeline: {str(e)}")

            # Export Chat Analysis
            st.title("Export Chat Analysis")
            try:
                chat_stats = pd.DataFrame({
                    'Metric': ['Total Messages', 'Total Words', 'Media Shared', 'Links Shared'],
                    'Value': [num_messages, words, num_media_messages, num_links]
                })
                chat_stats.index = chat_stats.index + 1
                csv = chat_stats.to_csv(index=False)
                st.download_button(
                    label="Download Chat Stats as CSV",
                    data=csv,
                    file_name="chat_stats.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"Error exporting chat analysis: {str(e)}")

        else:
            st.info("Click 'Show Analysis' to view the chat analysis.")

    # Sentiment Analysis Tab
    with tab2:
        if st.session_state.show_analysis:
            # Sentiment Trend Over Time
            st.title("Sentiment Trend Over Time")
            try:
                sentiment_trend = helper.sentiment_trend(selected_user, df)
                if not sentiment_trend.empty:
                    fig = px.area(
                        sentiment_trend, x='time', y=['Positive', 'Neutral', 'Negative'],
                        title='Sentiment Distribution Over Time',
                        color_discrete_map={'Positive': 'green', 'Neutral': 'grey', 'Negative': 'red'}
                    )
                    fig.update_layout(xaxis_tickangle=45, yaxis_title='Message Count')
                    st.plotly_chart(fig)
                else:
                    st.info("No sentiment trend data available.")
            except Exception as e:
                st.error(f"Error generating sentiment trend: {str(e)}")

            # Sentiment Intensity Distribution
            st.title("Sentiment Intensity Distribution")
            st.markdown("This shows the distribution of sentiment intensity scores (0 to 1) for each sentiment category.")
            try:
                intensity_df = helper.sentiment_intensity_distribution(selected_user, df)
                if not intensity_df.empty:
                    fig = px.histogram(
                        intensity_df,
                        nbins=20,
                        title='Distribution of Sentiment Intensity Scores',
                        color_discrete_map={'Positive': 'green', 'Negative': 'red', 'Neutral': 'grey'},
                        opacity=0.6
                    )
                    fig.update_layout(
                        xaxis_title='Intensity Score',
                        yaxis_title='Frequency',
                        barmode='overlay'
                    )
                    st.plotly_chart(fig)
                else:
                    st.info("No sentiment intensity data available.")
            except Exception as e:
                st.error(f"Error generating sentiment intensity distribution: {str(e)}")

            # Sentiment Transition Analysis
            st.title("Sentiment Transition Analysis")
            st.markdown("This shows how sentiment changes between consecutive messages (e.g., Positive to Negative).")
            try:
                transition_df = helper.sentiment_transition_analysis(selected_user, df)
                if not transition_df.empty:
                    transition_df.index = transition_df.index + 1
                    fig = px.bar(
                        transition_df,
                        x='Count',
                        y='Transition',
                        title='Sentiment Transitions Between Consecutive Messages',
                        color='Count',
                        color_continuous_scale='Blues',
                        orientation='h'
                    )
                    fig.update_layout(
                        xaxis_title='Number of Transitions',
                        yaxis_title='Transition Type'
                    )
                    st.plotly_chart(fig)
                    st.subheader("Transition Details")
                    st.dataframe(transition_df, use_container_width=True)
                else:
                    st.info("No sentiment transitions found (possibly too few messages).")
            except Exception as e:
                st.error(f"Error generating sentiment transition analysis: {str(e)}")

            # Sentiment by Message Length
            st.title("Sentiment by Message Length")
            st.markdown("This shows the average message length for each sentiment category.")
            try:
                length_df = helper.sentiment_by_message_length(selected_user, df)
                if not length_df.empty:
                    fig = px.bar(
                        length_df,
                        x='sentiment_label',
                        y='msg_length',
                        title='Average Message Length by Sentiment',
                        color='msg_length',
                        color_continuous_scale='Viridis'
                    )
                    fig.update_layout(
                        xaxis_title='Sentiment',
                        yaxis_title='Average Message Length (Characters)'
                    )
                    st.plotly_chart(fig)
                else:
                    st.info("No messages available to compute message length by sentiment.")
            except Exception as e:
                st.error(f"Error generating sentiment by message length: {str(e)}")

            # Sentiment and Emoji Correlation
            st.title("Sentiment and Emoji Correlation")
            st.markdown("This shows the top emojis associated with each sentiment category.")
            try:
                emoji_corr_df = helper.sentiment_emoji_correlation(selected_user, df)
                if not emoji_corr_df.empty:
                    emoji_corr_df.index = emoji_corr_df.index + 1
                    fig = px.bar(
                        emoji_corr_df,
                        x='Count',
                        y='Emoji',
                        color='Sentiment',
                        color_discrete_map={'Positive': 'green', 'Neutral': 'grey', 'Negative': 'red'},
                        title='Top Emojis by Sentiment Category',
                        orientation='h',
                        facet_col='Sentiment'
                    )
                    fig.update_layout(
                        xaxis_title='Emoji Count',
                        yaxis_title='Emoji',
                        height=600
                    )
                    st.plotly_chart(fig)
                    st.subheader("Emoji Correlation Details")
                    st.dataframe(emoji_corr_df, use_container_width=True)
                else:
                    st.info("No emojis found to correlate with sentiments.")
            except Exception as e:
                st.error(f"Error generating sentiment and emoji correlation: {str(e)}")

            # Monthly Activity Maps
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(
                    "<h3 style='text-align: center; color: var(--text-color);'>"
                    "Monthly Activity Map (Positive)</h3>",
                    unsafe_allow_html=True
                )
                try:
                    busy_month = helper.sentiment_month_activity_map(selected_user, df, 1)
                    if not busy_month.empty:
                        fig, ax_month_pos = plt.subplots()
                        ax_month_pos.bar(busy_month.index, busy_month.values, color='green')
                        plt.xticks(rotation='vertical')
                        st.pyplot(fig)
                    else:
                        st.info("No positive monthly activity data available.")
                except Exception as e:
                    st.error(f"Error generating positive monthly activity map: {str(e)}")
            with col2:
                st.markdown(
                    "<h3 style='text-align: center; color: var(--text-color);'>"
                    "Monthly Activity Map (Neutral)</h3>",
                    unsafe_allow_html=True
                )
                try:
                    busy_month = helper.sentiment_month_activity_map(selected_user, df, 0)
                    if not busy_month.empty:
                        fig, ax_month_neu = plt.subplots()
                        ax_month_neu.bar(busy_month.index, busy_month.values, color='grey')
                        plt.xticks(rotation='vertical')
                        st.pyplot(fig)
                    else:
                        st.info("No neutral monthly activity data available.")
                except Exception as e:
                    st.error(f"Error generating neutral monthly activity map: {str(e)}")
            with col3:
                st.markdown(
                    "<h3 style='text-align: center; color: var(--text-color);'>"
                    "Monthly Activity Map (Negative)</h3>",
                    unsafe_allow_html=True
                )
                try:
                    busy_month = helper.sentiment_month_activity_map(selected_user, df, -1)
                    if not busy_month.empty:
                        fig, ax_month_neg = plt.subplots()
                        ax_month_neg.bar(busy_month.index, busy_month.values, color='red')
                        plt.xticks(rotation='vertical')
                        st.pyplot(fig)
                    else:
                        st.info("No negative monthly activity data available.")
                except Exception as e:
                    st.error(f"Error generating negative monthly activity map: {str(e)}")

            # Daily Activity Maps
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(
                    "<h3 style='text-align: center; color: var(--text-color);'>"
                    "Daily Activity Map (Positive)</h3>",
                    unsafe_allow_html=True
                )
                try:
                    busy_day = helper.sentiment_week_activity_map(selected_user, df, 1)
                    if not busy_day.empty:
                        fig, ax_day_pos = plt.subplots()
                        ax_day_pos.bar(busy_day.index, busy_day.values, color='green')
                        plt.xticks(rotation='vertical')
                        st.pyplot(fig)
                    else:
                        st.info("No positive daily activity data available.")
                except Exception as e:
                    st.error(f"Error generating positive daily activity map: {str(e)}")
            with col2:
                st.markdown(
                    "<h3 style='text-align: center; color: var(--text-color);'>"
                    "Daily Activity Map (Neutral)</h3>",
                    unsafe_allow_html=True
                )
                try:
                    busy_day = helper.sentiment_week_activity_map(selected_user, df, 0)
                    if not busy_day.empty:
                        fig, ax_day_neu = plt.subplots()
                        ax_day_neu.bar(busy_day.index, busy_day.values, color='grey')
                        plt.xticks(rotation='vertical')
                        st.pyplot(fig)
                    else:
                        st.info("No neutral daily activity data available.")
                except Exception as e:
                    st.error(f"Error generating neutral daily activity map: {str(e)}")
            with col3:
                st.markdown(
                    "<h3 style='text-align: center; color: var(--text-color);'>"
                    "Daily Activity Map (Negative)</h3>",
                    unsafe_allow_html=True
                )
                try:
                    busy_day = helper.sentiment_week_activity_map(selected_user, df, -1)
                    if not busy_day.empty:
                        fig, ax_day_neg = plt.subplots()
                        ax_day_neg.bar(busy_day.index, busy_day.values, color='red')
                        plt.xticks(rotation='vertical')
                        st.pyplot(fig)
                    else:
                        st.info("No negative daily activity data available.")
                except Exception as e:
                    st.error(f"Error generating negative daily activity map: {str(e)}")

            # Weekly Activity Heatmaps
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(
                    "<h3 style='text-align: center; color: var(--text-color);'>"
                    "Weekly Activity Map (Positive)</h3>",
                    unsafe_allow_html=True
                )
                try:
                    user_heatmap = helper.sentiment_activity_heatmap(selected_user, df, 1)
                    if not user_heatmap.empty:
                        fig = plt.figure()
                        sns.heatmap(user_heatmap, ax=plt.gca())
                        st.pyplot(fig)
                    else:
                        st.info("No positive weekly activity data available.")
                except Exception as e:
                    st.error(f"Error generating positive weekly activity heatmap: {str(e)}")
            with col2:
                st.markdown(
                    "<h3 style='text-align: center; color: var(--text-color);'>"
                    "Weekly Activity Map (Neutral)</h3>",
                    unsafe_allow_html=True
                )
                try:
                    user_heatmap = helper.sentiment_activity_heatmap(selected_user, df, 0)
                    if not user_heatmap.empty:
                        fig = plt.figure()
                        sns.heatmap(user_heatmap, ax=plt.gca())
                        st.pyplot(fig)
                    else:
                        st.info("No neutral weekly activity data available.")
                except Exception as e:
                    st.error(f"Error generating neutral weekly activity heatmap: {str(e)}")
            with col3:
                st.markdown(
                    "<h3 style='text-align: center; color: var(--text-color);'>"
                    "Weekly Activity Map (Negative)</h3>",
                    unsafe_allow_html=True
                )
                try:
                    user_heatmap = helper.sentiment_activity_heatmap(selected_user, df, -1)
                    if not user_heatmap.empty:
                        fig = plt.figure()
                        sns.heatmap(user_heatmap, ax=plt.gca())
                        st.pyplot(fig)
                    else:
                        st.info("No negative weekly activity data available.")
                except Exception as e:
                    st.error(f"Error generating negative weekly activity heatmap: {str(e)}")

            # Daily Timelines
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(
                    "<h3 style='text-align: center; color: var(--text-color);'>"
                    "Daily Timeline (Positive)</h3>",
                    unsafe_allow_html=True
                )
                try:
                    daily_timeline = helper.sentiment_daily_timeline(selected_user, df, 1)
                    if not daily_timeline.empty:
                        fig, ax_daily_pos = plt.subplots()
                        ax_daily_pos.plot(daily_timeline['only_date'], daily_timeline['message'], color='green')
                        plt.xticks(rotation='vertical')
                        st.pyplot(fig)
                    else:
                        st.info("No positive daily timeline data available.")
                except Exception as e:
                    st.error(f"Error generating positive daily timeline: {str(e)}")
            with col2:
                st.markdown(
                    "<h3 style='text-align: center; color: var(--text-color);'>"
                    "Daily Timeline (Neutral)</h3>",
                    unsafe_allow_html=True
                )
                try:
                    daily_timeline = helper.sentiment_daily_timeline(selected_user, df, 0)
                    if not daily_timeline.empty:
                        fig, ax_daily_neu = plt.subplots()
                        ax_daily_neu.plot(daily_timeline['only_date'], daily_timeline['message'], color='grey')
                        plt.xticks(rotation='vertical')
                        st.pyplot(fig)
                    else:
                        st.info("No neutral daily timeline data available.")
                except Exception as e:
                    st.error(f"Error generating neutral daily timeline: {str(e)}")
            with col3:
                st.markdown(
                    "<h3 style='text-align: center; color: var(--text-color);'>"
                    "Daily Timeline (Negative)</h3>",
                    unsafe_allow_html=True
                )
                try:
                    daily_timeline = helper.sentiment_daily_timeline(selected_user, df, -1)
                    if not daily_timeline.empty:
                        fig, ax_daily_neg = plt.subplots()
                        ax_daily_neg.plot(daily_timeline['only_date'], daily_timeline['message'], color='red')
                        plt.xticks(rotation='vertical')
                        st.pyplot(fig)
                    else:
                        st.info("No negative daily timeline data available.")
                except Exception as e:
                    st.error(f"Error generating negative daily timeline: {str(e)}")

            # Monthly Timelines
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(
                    "<h3 style='text-align: center; color: var(--text-color);'>"
                    "Monthly Timeline (Positive)</h3>",
                    unsafe_allow_html=True
                )
                try:
                    timeline = helper.sentiment_monthly_timeline(selected_user, df, 1)
                    if not timeline.empty:
                        fig = px.line(
                            timeline, x='time', y='message',
                            title='Positive Messages Over Time',
                            color_discrete_sequence=['green']
                        )
                        fig.update_layout(xaxis_tickangle=45)
                        st.plotly_chart(fig)
                    else:
                        st.info("No positive monthly timeline data available.")
                except Exception as e:
                    st.error(f"Error generating positive monthly timeline: {str(e)}")
            with col2:
                st.markdown(
                    "<h3 style='text-align: center; color: var(--text-color);'>"
                    "Monthly Timeline (Neutral)</h3>",
                    unsafe_allow_html=True
                )
                try:
                    timeline = helper.sentiment_monthly_timeline(selected_user, df, 0)
                    if not timeline.empty:
                        fig = px.line(
                            timeline, x='time', y='message',
                            title='Neutral Messages Over Time',
                            color_discrete_sequence=['grey']
                        )
                        fig.update_layout(xaxis_tickangle=45)
                        st.plotly_chart(fig)
                    else:
                        st.info("No neutral monthly timeline data available.")
                except Exception as e:
                    st.error(f"Error generating neutral monthly timeline: {str(e)}")
            with col3:
                st.markdown(
                    "<h3 style='text-align: center; color: var(--text-color);'>"
                    "Monthly Timeline (Negative)</h3>",
                    unsafe_allow_html=True
                )
                try:
                    timeline = helper.sentiment_monthly_timeline(selected_user, df, -1)
                    if not timeline.empty:
                        fig = px.line(
                            timeline, x='time', y='message',
                            title='Negative Messages Over Time',
                            color_discrete_sequence=['red']
                        )
                        fig.update_layout(xaxis_tickangle=45)
                        st.plotly_chart(fig)
                    else:
                        st.info("No negative monthly timeline data available.")
                except Exception as e:
                    st.error(f"Error generating negative monthly timeline: {str(e)}")

            # Sentiment Contribution
            if selected_user == 'Overall':
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(
                        "<h3 style='text-align: center; color: var(--text-color);'>"
                        "Most Positive Contribution</h3>",
                        unsafe_allow_html=True
                    )
                    try:
                        x = helper.sentiment_percentage(df, 1)
                        if not x.empty:
                            x.index = x.index + 1
                            st.dataframe(x)
                        else:
                            st.info("No positive contributions found.")
                    except Exception as e:
                        st.error(f"Error generating positive contribution: {str(e)}")
                with col2:
                    st.markdown(
                        "<h3 style='text-align: center; color: var(--text-color);'>"
                        "Most Neutral Contribution</h3>",
                        unsafe_allow_html=True
                    )
                    try:
                        x = helper.sentiment_percentage(df, 0)
                        if not x.empty:
                            x.index = x.index + 1
                            st.dataframe(x)
                        else:
                            st.info("No neutral contributions found.")
                    except Exception as e:
                        st.error(f"Error generating neutral contribution: {str(e)}")
                with col3:
                    st.markdown(
                        "<h3 style='text-align: center; color: var(--text-color);'>"
                        "Most Negative Contribution</h3>",
                        unsafe_allow_html=True
                    )
                    try:
                        x = helper.sentiment_percentage(df, -1)
                        if not x.empty:
                            x.index = x.index + 1
                            st.dataframe(x)
                        else:
                            st.info("No negative contributions found.")
                    except Exception as e:
                        st.error(f"Error generating negative contribution: {str(e)}")

            # Sentiment WordClouds
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(
                    "<h3 style='text-align: center; color: var(--text-color);'>"
                    "Wordcloud (Positive)</h3>",
                    unsafe_allow_html=True
                )
                try:
                    df_wc = helper.sentiment_create_wordcloud(selected_user, df, 1)
                    if df_wc:
                        fig, ax_wc_pos = plt.subplots()
                        ax_wc_pos.imshow(df_wc)
                        ax_wc_pos.axis('off')
                        st.pyplot(fig)
                    else:
                        st.info("No positive words available to generate a wordcloud.")
                except Exception as e:
                    st.error(f"Error generating positive wordcloud: {str(e)}")
            with col2:
                st.markdown(
                    "<h3 style='text-align: center; color: var(--text-color);'>"
                    "Wordcloud (Neutral)</h3>",
                    unsafe_allow_html=True
                )
                try:
                    df_wc = helper.sentiment_create_wordcloud(selected_user, df, 0)
                    if df_wc:
                        fig, ax_wc_neu = plt.subplots()
                        ax_wc_neu.imshow(df_wc)
                        ax_wc_neu.axis('off')
                        st.pyplot(fig)
                    else:
                        st.info("No neutral words available to generate a wordcloud.")
                except Exception as e:
                    st.error(f"Error generating neutral wordcloud: {str(e)}")
            with col3:
                st.markdown(
                    "<h3 style='text-align: center; color: var(--text-color);'>"
                    "Wordcloud (Negative)</h3>",
                    unsafe_allow_html=True
                )
                try:
                    df_wc = helper.sentiment_create_wordcloud(selected_user, df, -1)
                    if df_wc:
                        fig, ax_wc_neg = plt.subplots()
                        ax_wc_neg.imshow(df_wc)
                        ax_wc_neg.axis('off')
                        st.pyplot(fig)
                    else:
                        st.info("No negative words available to generate a wordcloud.")
                except Exception as e:
                    st.error(f"Error generating negative wordcloud: {str(e)}")

            # Most Common Words by Sentiment
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(
                    "<h3 style='text-align: center; color: var(--text-color);'>"
                    "Most Common Words (Positive)</h3>",
                    unsafe_allow_html=True
                )
                try:
                    most_common_df = helper.sentiment_most_common_words(selected_user, df, 1)
                    if not most_common_df.empty:
                        most_common_df.index = most_common_df.index + 1
                        fig, ax_common_pos = plt.subplots()
                        ax_common_pos.barh(most_common_df[0], most_common_df[1], color='green')
                        plt.xticks(rotation='vertical')
                        st.pyplot(fig)
                    else:
                        st.info("No positive common words found.")
                except Exception as e:
                    st.error(f"Error generating positive common words: {str(e)}")
            with col2:
                st.markdown(
                    "<h3 style='text-align: center; color: var(--text-color);'>"
                    "Most Common Words (Neutral)</h3>",
                    unsafe_allow_html=True
                )
                try:
                    most_common_df = helper.sentiment_most_common_words(selected_user, df, 0)
                    if not most_common_df.empty:
                        most_common_df.index = most_common_df.index + 1
                        fig, ax_common_neu = plt.subplots()
                        ax_common_neu.barh(most_common_df[0], most_common_df[1], color='grey')
                        plt.xticks(rotation='vertical')
                        st.pyplot(fig)
                    else:
                        st.info("No neutral common words found.")
                except Exception as e:
                    st.error(f"Error generating neutral common words: {str(e)}")
            with col3:
                st.markdown(
                    "<h3 style='text-align: center; color: var(--text-color);'>"
                    "Most Common Words (Negative)</h3>",
                    unsafe_allow_html=True
                )
                try:
                    most_common_df = helper.sentiment_most_common_words(selected_user, df, -1)
                    if not most_common_df.empty:
                        most_common_df.index = most_common_df.index + 1
                        fig, ax_common_neg = plt.subplots()
                        ax_common_neg.barh(most_common_df[0], most_common_df[1], color='red')
                        plt.xticks(rotation='vertical')
                        st.pyplot(fig)
                    else:
                        st.info("No negative common words found.")
                except Exception as e:
                    st.error(f"Error generating negative common words: {str(e)}")

        else:
            st.info("Click 'Show Analysis' to view the sentiment analysis.")

    # Keyword Analysis Tab
    with tab3:
        if st.session_state.show_analysis:
            if keyword:
                st.title(f"Keyword Search: '{keyword}'")
                try:
                    keyword_df = helper.keyword_search(selected_user, df, keyword)
                    if not keyword_df.empty:
                        keyword_df.index = keyword_df.index + 1
                        st.dataframe(keyword_df[['date', 'user', 'message']], use_container_width=True)
                    else:
                        st.info(f"No messages found containing the keyword '{keyword}' for the selected user and date range.")
                except Exception as e:
                    st.error(f"Error performing keyword search: {str(e)}")

                st.title(f"Keyword Timeline: '{keyword}'")
                try:
                    keyword_timeline = helper.keyword_timeline(selected_user, df, keyword)
                    if not keyword_timeline.empty:
                        fig = px.line(
                            keyword_timeline, x='time', y='count',
                            title=f"Occurrences of '{keyword}' Over Time",
                            color_discrete_sequence=['blue']
                        )
                        fig.update_layout(xaxis_tickangle=45)
                        st.plotly_chart(fig)
                    else:
                        st.info(f"No timeline data available for the keyword '{keyword}'.")
                except Exception as e:
                    st.error(f"Error generating keyword timeline: {str(e)}")
            else:
                st.info("Please enter a keyword in the sidebar to perform a search.")
        else:
            st.info("Click 'Show Analysis' to view the keyword analysis.")

    # Message Length Analysis Tab
    with tab4:
        if st.session_state.show_analysis:
            # Average Message Length by User
            st.title("Average Message Length by User")
            st.markdown("This shows the average length of messages (in characters) sent by each user.")
            try:
                length_df = helper.message_length_by_user(selected_user, df)
                if not length_df.empty:
                    length_df.index = length_df.index + 1
                    fig = px.bar(
                        length_df,
                        x='user',
                        y='avg_length',
                        title='Average Message Length per User',
                        color='avg_length',
                        color_continuous_scale='Blues'
                    )
                    fig.update_layout(
                        xaxis_title='User',
                        yaxis_title='Average Message Length (Characters)',
                        xaxis_tickangle=45
                    )
                    st.plotly_chart(fig)
                    st.subheader("Details")
                    st.dataframe(length_df, use_container_width=True)
                else:
                    st.info("No messages available to compute average message length (possibly due to media messages or group notifications).")
            except Exception as e:
                st.error(f"Error generating average message length by user: {str(e)}")

            # Message Length Over Time
            st.title("Message Length Over Time")
            st.markdown("This shows the average message length over time (by month).")
            try:
                length_timeline = helper.message_length_timeline(selected_user, df)
                if not length_timeline.empty:
                    fig = px.line(
                        length_timeline,
                        x='time',
                        y='avg_length',
                        title='Average Message Length Over Time',
                        color_discrete_sequence=['purple']
                    )
                    fig.update_layout(
                        xaxis_title='Time',
                        yaxis_title='Average Message Length (Characters)',
                        xaxis_tickangle=45
                    )
                    st.plotly_chart(fig)
                else:
                    st.info("No messages available to compute message length timeline.")
            except Exception as e:
                st.error(f"Error generating message length timeline: {str(e)}")

            # Message Length Distribution
            st.title("Message Length Distribution")
            st.markdown("This shows the distribution of message lengths (in characters).")
            try:
                length_distribution = helper.message_length_distribution(selected_user, df)
                if not length_distribution.empty:
                    fig = px.histogram(
                        length_distribution,
                        x=length_distribution,
                        nbins=30,
                        title='Distribution of Message Lengths',
                        color_discrete_sequence=['teal']
                    )
                    fig.update_layout(
                        xaxis_title='Message Length (Characters)',
                        yaxis_title='Frequency'
                    )
                    st.plotly_chart(fig)
                else:
                    st.info("No messages available to compute message length distribution.")
            except Exception as e:
                st.error(f"Error generating message length distribution: {str(e)}")

            # Message Length by Sentiment
            st.title("Message Length by Sentiment")
            st.markdown("This shows the average message length for each sentiment category.")
            try:
                length_sentiment = helper.message_length_by_sentiment(selected_user, df)
                if not length_sentiment.empty:
                    fig = px.bar(
                        length_sentiment,
                        x='sentiment_label',
                        y='msg_length',
                        title='Average Message Length by Sentiment',
                        color='msg_length',
                        color_continuous_scale='Viridis'
                    )
                    fig.update_layout(
                        xaxis_title='Sentiment',
                        yaxis_title='Average Message Length (Characters)'
                    )
                    st.plotly_chart(fig)
                else:
                    st.info("No messages available to compute message length by sentiment.")
            except Exception as e:
                st.error(f"Error generating message length by sentiment: {str(e)}")

            # Message Length by Day of Week
            st.title("Message Length by Day of Week")
            st.markdown("This shows the average message length for each day of the week.")
            try:
                length_day = helper.message_length_by_day_of_week(selected_user, df)
                if not length_day.empty:
                    fig = px.bar(
                        length_day,
                        x='day_name',
                        y='msg_length',
                        title='Average Message Length by Day of Week',
                        color='msg_length',
                        color_continuous_scale='Oranges'
                    )
                    fig.update_layout(
                        xaxis_title='Day of Week',
                        yaxis_title='Average Message Length (Characters)',
                        xaxis_tickangle=45
                    )
                    st.plotly_chart(fig)
                else:
                    st.info("No messages available to compute message length by day of week.")
            except Exception as e:
                st.error(f"Error generating message length by day of week: {str(e)}")

            # Longest and Shortest Messages
            st.title("Longest and Shortest Messages")
            st.markdown("This shows the top 5 longest and shortest messages by character count.")
            try:
                longest, shortest = helper.extreme_messages(selected_user, df)
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Longest Messages")
                    if not longest.empty:
                        longest.index = longest.index + 1
                        st.dataframe(longest, use_container_width=True)
                    else:
                        st.info("No messages available to display longest messages.")
                with col2:
                    st.subheader("Shortest Messages")
                    if not shortest.empty:
                        shortest.index = shortest.index + 1
                        st.dataframe(shortest, use_container_width=True)
                    else:
                        st.info("No messages available to display shortest messages (excluding zero-length messages).")
            except Exception as e:
                st.error(f"Error generating longest and shortest messages: {str(e)}")

        else:
            st.info("Click 'Show Analysis' to view the message length analysis.")

else:
    st.info("Please upload a WhatsApp chat file to begin analysis.")
