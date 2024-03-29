from flask import Flask, render_template, request
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
from difflib import SequenceMatcher
import time
from flask_frozen import Freezer
freezer = Freezer(app)

app = Flask(__name__)

def calculate_similarity(text1, text2):
    # Using SequenceMatcher to calculate the similarity ratio between two texts
    return SequenceMatcher(None, text1, text2).ratio()

def estimate_ai_percentage(input_text, ai_generated_text):
    similarity_ratio = calculate_similarity(input_text, ai_generated_text)
    # Assuming higher similarity indicates more AI-written content
    ai_percentage = (1 - similarity_ratio) * 100
    return round(ai_percentage, 2)  # Round to two decimal places

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('About.html')

@app.route('/contact')
def contact():
    return render_template('Contact.html')

@app.route('/pricing')
def pricing():
    return render_template('Pricing.html')

@app.route('/blog')
def blog():
    return render_template('Blog.html')

@app.route('/check', methods=['POST'])
def check():
    input_text = request.form['input_text']

    # Load pre-trained GPT2 tokenizer and model
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")

    # Tokenize input text
    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    attention_mask = torch.ones_like(input_ids)

    # Generate text using GPT2 model
    max_length = len(input_text) + 50  # Adjust this value based on your preference
    ai_generated_ids = model.generate(input_ids, attention_mask=attention_mask, max_length=max_length, do_sample=True, temperature=0.7)
    ai_generated_text = tokenizer.decode(ai_generated_ids[0], skip_special_tokens=True)

    ai_percentage = estimate_ai_percentage(input_text, ai_generated_text)
    human_percentage = round(100 - ai_percentage, 2)  # Round to two decimal places

    time.sleep(2)  # Simulating delay for demonstration (remove this in production)

    return render_template('index.html', ai_percentage=ai_percentage, human_percentage=human_percentage)

if __name__ == "__main__":
    app.run(debug=True)
    freezer.freeze()
