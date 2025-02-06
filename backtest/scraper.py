import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define financial keywords
financial_keywords = ['stock', 'market', 'investment', 'finance', 'economy', 'trading', 'shares']

# Function to filter headlines based on keywords
def is_financial_headline(headline):
    return any(keyword in headline.lower() for keyword in financial_keywords)

# Function to scrape headlines and filter them
def get_headlines(url, tag):
    response = requests.get(url)
    print("The response code is:", response.status_code)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        headlines = soup.find_all(tag)
        return [headline.text.strip() for headline in headlines if is_financial_headline(headline.text.strip())]
    else:
        return []

# List of sites
sites = [
    {'url': 'https://www.livemint.com/', 'tag': 'h2'},
    {'url': 'https://www.livemint.com/', 'tag': 'h3'},
    {'url': 'https://www.moneycontrol.com/news/business/economy/', 'tag':'h2'},
    {'url': 'https://www.moneycontrol.com/news/business/economy/', 'tag':'h3'},
    {'url': 'https://www.moneycontrol.com/news/business/economy/', 'tag':'h1'},
    {'url': 'https://www.bloomberg.com/asia', 'tag':'h1'},
    {'url': 'https://www.bloomberg.com/asia', 'tag':'h2'},
    {'url': 'https://www.bloomberg.com/asia', 'tag':'h3'},
]

# Collect all filtered headlines
all_headlines = []
for site in sites:
    headlines = get_headlines(site['url'], site['tag'])
    print(f"Filtered headlines from {site['url']} with tag {site['tag']}:\n")
    for headline in headlines:
        print(headline, "\n")
    all_headlines.extend(headlines)

# Save filtered headlines to a CSV file
df = pd.DataFrame(all_headlines, columns=['headline'])
df.to_csv('filtered_headlines.csv', index=False)

# Sentiment analysis function (assumed you already have this)
from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Load the pre-trained FinBERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
model = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone')

# Sentiment analysis function
def analyze_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    sentiment = torch.argmax(logits).item()
    sentiment_labels = ['negative', 'neutral', 'positive']
    return sentiment_labels[sentiment]

# Perform sentiment analysis on all headlines
df_all_headlines = pd.DataFrame(all_headlines, columns=['headline'])
df_all_headlines['sentiment'] = df_all_headlines['headline'].apply(analyze_sentiment)

# Calculate the overall sentiment from all headlines
def get_overall_sentiment(df):
    sentiment_counts = df['sentiment'].value_counts()
    overall_sentiment = sentiment_counts.idxmax()  # The most frequent sentiment
    return overall_sentiment

# Calculate overall sentiment
overall_sentiment = get_overall_sentiment(df_all_headlines)

# Save all headlines with their sentiment to a CSV
df_all_headlines.to_csv('headlines_with_sentiment.csv', index=False)

# Get top 5 headlines
top_headlines = df_all_headlines['headline'].value_counts().head(5)

# Return top 5 headlines and overall sentiment (this will be used in the view)
top_5_headlines = top_headlines.tolist()  # Top 5 headlines
