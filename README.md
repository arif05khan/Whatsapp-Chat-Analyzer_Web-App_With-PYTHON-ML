# 📊 WhatsApp Chat & Sentiment Analyzer Web App

The **WhatsApp Chat & Sentiment Analyzer** is an interactive web application built with Python and Streamlit that allows users to upload and analyze their WhatsApp chat history. It provides valuable insights into messaging behavior, sentiment trends, keyword usage, and message lengths, all presented through an intuitive and user-friendly interface.

The app enables users to analyze both individual and group chats, uncovering patterns in communication, emotional expression, and interaction dynamics. Ideal for individuals, researchers, and social scientists, it helps users explore how conversations evolve over time, identify key sentiment shifts, and track word frequency and emoji usage.

With features like sentiment analysis, keyword tracking, message length analysis, and interactive visualizations, the tool makes it easy to explore and understand the hidden patterns within digital communication.

Ideal for individuals, researchers, and social scientists, this tool helps uncover patterns in digital communication and emotional expression.

---

## 🚀 Deployed Version

Check out the live deployed version of this project here:

[**Live Demo**] ( https://whatsapp-chat-sentiment-analyzer-python-ml.streamlit.app/ ) 
Note: Copy this link and paste it into your browser for the proper functioning of the app. It is mobile-friendly as well as desktop-compatible.

---

## 🚀 Key Features

### 📈 Chat Analysis
- Total messages, words, media, links, emojis, and stickers
- Most active users (group chats)
- Word frequency (bar charts + WordCloud)
- Emoji contribution and usage analysis
- Daily and monthly message timelines
- Weekly/monthly activity maps
- Heatmaps of message activity (day vs hour)
- Response time analysis between users
- CSV export for all chat stats

### 😊 Sentiment Analysis
- Positive, neutral, and negative classification using **VADER (NLTK)**
- Sentiment distribution and trends over time
- Sentiment transitions between messages
- Sentiment intensity histograms
- Correlation between sentiments and emojis
- Sentiment-based word clouds
- Sentiment-wise message length analysis
- Weekly and monthly sentiment heatmaps

### 🔍 Keyword Analysis
- Keyword search with user and timestamp
- Keyword frequency timeline

### 📝 Message Length Analysis
- Avg. message length per user
- Length trends over time (monthly)
- Distribution histograms
- Message length by sentiment and weekday
- Top 5 longest and shortest messages

---

## ⚙️ Additional Features
- Date range filter for focused analysis
- User-specific or group-level filtering
- Light/dark mode toggle
- Robust error handling and user feedback

---

## 🛠️ Tech Stack & Tools

| **Category**         | **Tool/Library**         |
|----------------------|--------------------------|
| **Language**         | Python 3.x               |
| **Web Framework**    | Streamlit                |
| **Data Analysis**    | Pandas                   |
| **Visualization**    | Matplotlib, Plotly       |
| **NLP / Sentiment**  | NLTK (VADER)             |
| **Emoji Handling**   | Emoji (Python)           |
| **Text Processing**  | Regular Expressions      |
| **UI/UX Features**   | Streamlit Components     |
| **IDE**              | PyCharm / VS Code        |

---

## 📂 Project Structure

```bash
📦 WhatsApp_Chat_Sentiment_Analyzer
├── app.py              # Main Streamlit app
├── helper.py           # Chat analysis functions
├── preprocessor.py     # Parsing and cleaning logic
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation


🚀 Getting Started
Prerequisites
Python 3.8+

pip

Installation
Clone the repository:
git clone https://github.com/arif05khan/Whatsapp-Chat-Analyzer_Web-App_With-PYTHON-ML.git
cd Whatsapp-Chat-Analyzer_Web-App_With-PYTHON-ML


Install the required packages:
pip install -r requirements.txt


Run the app:
streamlit run app.py
Upload your exported WhatsApp .txt file and explore the insights!


##📸 **Screenshots**
###Dashboard
WhatsApp Image 2025-05-07 at 21.23.46_00d479bf.jpg


###Analysis of Chats


###Sentiment Analysis


###Keyword Analysis


###Message Length Analysis




📤 Export Options
Download chat statistics and insights as CSV from the sidebar.

📌 Notes
The app supports WhatsApp .txt export format (including 2025 format).

It automatically handles different timestamp and message formats.

Works for both individual and group chats.

👨‍💻 Author
Arif Rasul Khan
📍 Delhi, India
