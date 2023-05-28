from flask import Flask, request, jsonify, send_file
from werkzeug.exceptions import BadRequest
import openai
import math
import csv

# Flask app initialization
app = Flask(__name__)

openai.api_key = "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"
questions = []

# Split text into chunks
def split_text(text, max_chars=3000):
    # The rest of your function here

# Generate questions from text
def create_direct_questions(text, n):
    # The rest of your function here

# Write the generated questions to a CSV file
def create_csv(questions, output_file='output.csv'):
    # The rest of your function here

# Generate questions and return them in JSON format
@app.route('/api/generate-questions', methods=['POST'])
def generate_questions():
    data = request.get_json()
    try:
        text = data['text_input']
        n = data['number_input']
    except (TypeError, KeyError):
        raise BadRequest('Request body must be JSON with "text_input" and "number_input" fields')
    split_texts = split_text(text)
    m = len(split_texts)
    n_per_text = math.ceil(n / m)
    all_questions = []
    for split_text in split_texts:
        questions = create_direct_questions(split_text, n_per_text)
        all_questions.extend(questions)
    create_csv(all_questions)
    return jsonify(all_questions)

# Serve the CSV file
@app.route('/api/download-csv', methods=['GET'])
def download_csv():
    return send_file('output.csv', as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
