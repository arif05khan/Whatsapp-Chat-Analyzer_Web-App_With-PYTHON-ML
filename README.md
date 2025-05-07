# 📊 WhatsApp Chat & Sentiment Analyzer Web App

The **WhatsApp Chat & Sentiment Analyzer** is an interactive web application built with Python and Streamlit that allows users to upload and analyze their WhatsApp chat history. It provides valuable insights into messaging behavior, sentiment trends, keyword usage, and message lengths, all presented through an intuitive and user-friendly interface.

The app enables users to analyze both individual and group chats, uncovering patterns in communication, emotional expression, and interaction dynamics. Ideal for individuals, researchers, and social scientists, it helps users explore how conversations evolve over time, identify key sentiment shifts, and track word frequency and emoji usage.

With features like sentiment analysis, keyword tracking, message length analysis, and interactive visualizations, the tool makes it easy to explore and understand the hidden patterns within digital communication.

Ideal for individuals, researchers, and social scientists, this tool helps uncover patterns in digital communication and emotional expression.

---

## 🚀 Deployed Version

Check out the live deployed version of this project here:

[**Live Demo**] ( https://whatsapp-chat-sentiment-analyzer-python-ml.streamlit.app/ ) 
Note-: Copy this link and paste in your browser for proper working app.

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
![WhatsApp Image 2025-05-07 at 21 23 46_00d479bf](https://github.com/user-attachments/assets/00fc79c9-2e9a-48a5-bcf9-214de65d5ceb)
![WhatsApp Image 2025-05-07 at 21 23 46_00d479bf](https://github.com/user-attachments/assets/2fe917da-82b3-40e2-995f-6bb3cfafd0df)
![image](https://github.com/user-attachments/assets/6c14049f-c7b7-4906-b5bb-18d8776b66a2)
![image](https://github.com/user-attachments/assets/bbe14267-0a26-43bd-8c45-ff8f1b9dd1d2)

###Analysis of Chats
![WhatsApp Image 2025-05-07 at 21 23 46_00d479bf](https://github.com/user-attachments/assets/76e6ca16-8e5f-477d-83b0-ff293e15292f)

![image](https://github.com/user-attachments/assets/a93f2fe9-f362-48b4-a443-9875c6828dd5)
![image](https://github.com/user-attachments/assets/19737a14-6ccc-483a-9a25-651056c8dd7b)
![image](https://github.com/user-attachments/assets/72ab38f0-fcc1-4da4-b8ff-312f6f35f8d9)
![image](https://github.com/user-attachments/assets/c68e3364-53f2-4756-b187-9c46f5816cb7)
![image](https://github.com/user-attachments/assets/0bd65263-789f-4a8f-873a-6c64f73443f6)
![image](https://github.com/user-attachments/assets/41150575-7c64-4a82-8611-30b1674efa70)
![image](https://github.com/user-attachments/assets/dfaca751-62ee-4d59-8346-569cdae91ece)
![image](https://github.com/user-attachments/assets/678969cd-34c6-4037-9944-00ca825afe3e)
![image](https://github.com/user-attachments/assets/579a5959-ec4c-4f63-bf50-19a904c8d96e)
![image](https://github.com/user-attachments/assets/f8170c1e-f42b-4b0e-baf2-092891a0378c)
![image](https://github.com/user-attachments/assets/a4684170-0c7e-495b-b0d8-37f9b880817c)
![image](https://github.com/user-attachments/assets/500a00f8-15da-4c98-8175-1445fd5e1476)
![image](https://github.com/user-attachments/assets/21acceb3-2626-4d4c-9005-78f210ab8b1d)

###Sentiment Analysis
![image](https://github.com/user-attachments/assets/8a15c164-8bba-46b6-b562-a949e07a0e44)
![image](https://github.com/user-attachments/assets/6d55cef1-f0de-4d69-a486-d0f8a33eede6)
![image](https://github.com/user-attachments/assets/b1158e49-501c-4eb1-9773-01cb0f0948fc)
![image](https://github.com/user-attachments/assets/8b2464e5-f1dd-4a72-b25c-65fe54d31e5e)
![image](https://github.com/user-attachments/assets/701cb593-d45f-491d-8fd2-4ea1fc2f7c95)
![image](https://github.com/user-attachments/assets/1de66c08-345d-44b8-8d68-569feab7547d)
![image](https://github.com/user-attachments/assets/9cd3287c-dc36-4c8a-82fa-1990b18a8c28)
![image](https://github.com/user-attachments/assets/c7aac42c-d01c-4d26-99b9-1defe3cfa97a)
![image](https://github.com/user-attachments/assets/73cebecf-88d4-4417-9e24-35d3d4a19d33)
![image](https://github.com/user-attachments/assets/aef11d18-c33c-47ba-89f8-78be43c82e2a)
![image](https://github.com/user-attachments/assets/2f1057b2-b0bf-4d21-b159-db716b7c7c4c)

###Keyword Analysis
![image](https://github.com/user-attachments/assets/3f399947-cc5a-4c9f-adf1-27fe17d663df)
![image](https://github.com/user-attachments/assets/2de90fc8-fe95-4b26-99b9-5a290ad9ce78)
![image](https://github.com/user-attachments/assets/bfbfc1ec-c1d4-4198-b346-b9321172fdf7)

###Message Length Analysis
![image](https://github.com/user-attachments/assets/52c2c23a-7571-4f6e-b7c8-ccd406570e7e)
![image](https://github.com/user-attachments/assets/2745bcbc-221e-4b1d-95bd-66af9b20d5c4)
![image](https://github.com/user-attachments/assets/6534e786-a7cc-4e37-a8f1-9e727d622ac8)
![image](https://github.com/user-attachments/assets/9583de72-8c18-4405-bce0-40a0322a3e23)
![image](https://github.com/user-attachments/assets/dbd9715f-425c-4f78-b5dd-860e54577521)
![image](https://github.com/user-attachments/assets/b48ec2a0-d7e3-481b-9de3-21dbfe05a40a)
![image](https://github.com/user-attachments/assets/d9536264-eb16-4650-bec7-98f25a4124fb)
![image](https://github.com/user-attachments/assets/17dda3d9-2ab0-4e61-a70a-3523156e0d88)



📤 Export Options
Download chat statistics and insights as CSV from the sidebar.

📌 Notes
The app supports WhatsApp .txt export format (including 2025 format).

It automatically handles different timestamp and message formats.

Works for both individual and group chats.

👨‍💻 Author
Arif Rasul Khan
📍 Delhi, India
