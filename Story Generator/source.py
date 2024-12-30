from flask import Flask, jsonify, request
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

app = Flask(__name__)

# Load the Hugging Face model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

@app.route('/sentiment', methods=['POST'])
def sentiment_analysis():
    text = request.json['text']
    inputs = tokenizer(text, return_tensors='pt')
    outputs = model(**inputs)
    sentiment = torch.argmax(outputs.logits) + 1
    return jsonify({'sentiment': sentiment})

if __name__ == '__main__':
    app.run(debug=True)
