📊 WhatsApp Chat & Sentiment Analyzer Web App
The WhatsApp Chat & Sentiment Analyzer is a robust and interactive web application that allows users to upload and analyze their WhatsApp chat history. It provides deep insights into messaging behavior, sentiment trends, keyword usage, and message lengths, all through a user-friendly interface built with Python and Streamlit.

Ideal for individuals, researchers, and social scientists, this tool helps uncover patterns in digital communication and emotional expression.

🚀 Key Features
📈 Chat Analysis
Total messages, words, media, links, emojis, and stickers

Most active users (group chats)

Word frequency (bar charts + WordCloud)

Emoji contribution and usage analysis

Daily and monthly message timelines

Weekly/monthly activity maps

Heatmaps of message activity (day vs hour)

Response time analysis between users

CSV export for all chat stats

😊 Sentiment Analysis
Positive, neutral, and negative classification using VADER (NLTK)

Sentiment distribution and trends over time

Sentiment transitions between messages

Sentiment intensity histograms

Correlation between sentiments and emojis

Sentiment-based word clouds

Sentiment-wise message length analysis

Weekly and monthly sentiment heatmaps

🔍 Keyword Analysis
Keyword search with user and timestamp

Keyword frequency timeline

📝 Message Length Analysis
Avg. message length per user

Length trends over time (monthly)

Distribution histograms

Message length by sentiment and weekday

Top 5 longest and shortest messages

⚙️ Additional Features
Date range filter for focused analysis

User-specific or group-level filtering

Light/dark mode toggle

Robust error handling and user feedback

🛠️ Tech Stack   &   Tools
Category	        Tool/Library
Language	         Python 3.x
Web Framework	     Streamlit
Data Analysis	     Pandas
Visualization	     Matplotlib, Plotly
NLP / Sentiment	   NLTK (VADER)
Emoji Handling	   Emoji (Python)
Text Processing	   Regular Expressions
UI/UX Features	   Streamlit Components
IDE	               PyCharm / VS Code

📂 Project Structure
bash
Copy
Edit
📦 WhatsApp_Chat_Sentiment_Analyzer
├── app.py              # Main Streamlit app
├── helper.py           # Chat analysis functions
├── preprocessor.py     # Parsing and cleaning logic
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
📸 Screenshots
Dashboard	Sentiment	WordCloud
		

🚀 Getting Started
Prerequisites
Python 3.8+

pip

Installation
Clone the repository:

bash
Copy
Edit
git clone https://github.com/arif05khan/Whatsapp-Chat-Analyzer_Web-App_With-PYTHON-ML.git
cd Whatsapp-Chat-Analyzer_Web-App_With-PYTHON-ML
Install the required packages:

bash
Copy
Edit
pip install -r requirements.txt
Run the app:

bash
Copy
Edit
streamlit run app.py
Upload your exported WhatsApp .txt file and explore the insights!

📤 Export Options
Download chat statistics and insights as CSV from the sidebar.

📌 Notes
The app supports WhatsApp .txt export format (including 2025 format).

It automatically handles different timestamp and message formats.

Works for both individual and group chats.

👨‍💻 Author
Arif Rasul
📍 Delhi, India
