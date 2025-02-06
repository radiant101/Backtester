from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Load the pre-trained FinBERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
model = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone')

# Sentiment analysis function
def analyze_sentiment(text):
    # Tokenize input text
    inputs = tokenizer(text, return_tensors="pt")

    # Run through the model
    with torch.no_grad():
        outputs = model(**inputs)

    # Get sentiment prediction (logits)
    logits = outputs.logits
    sentiment = torch.argmax(logits).item()

    # Map logits to sentiment (e.g., 0 = negative, 1 = neutral, 2 = positive)
    sentiment_labels = ['negative', 'neutral', 'positive']
    return sentiment_labels[sentiment]

