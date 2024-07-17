from flask import Flask, request, jsonify, render_template
import pandas as pd
import os
import openai
import fitz  # PyMuPDF

# Initialize Flask app
app = Flask(__name__)

# Initialize OpenAI API
openai.api_key = 'your_openai_api_key'  # Replace with your actual OpenAI API key

# Function to extract text from PDFs
def extract_text_from_pdfs(folder_path):
    combined_text = ""
    for pdf_file in os.listdir(folder_path):
        if pdf_file.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, pdf_file)
            document = fitz.open(pdf_path)
            for page_num in range(len(document)):
                page = document.load_page(page_num)
                combined_text += page.get_text()
    return combined_text

# Extract text from all PDFs in the 'docs' folder
context = extract_text_from_pdfs('docs')

def generate_response(question, context):
    prompt = f"{context}\n\nQuestion: {question}\nAnswer:"
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can use other engines like "gpt-3.5-turbo" if available
        prompt=prompt,
        max_tokens=150,
        temperature=0.5
    )
    return response.choices[0].text.strip()

@app.route('/')
def index():
    return render_template('chatbot.html')  # Render the HTML template (no folder needed)

@app.route('/chatbot', methods=['GET'])
def chatbot():
    user_query = request.args.get('query')
    response = generate_response(user_query, context)
    return jsonify(response)

@app.route('/process_questions', methods=['POST'])
def process_questions():
    input_folder = request.json.get('input_folder')
    output_folder = request.json.get('output_folder')

    if not os.path.exists(input_folder):
        return jsonify({"error": "Input folder does not exist"}), 400
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    input_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f)) and f.endswith('.txt')]

    for input_file in input_files:
        with open(os.path.join(input_folder, input_file), 'r') as file:
            questions = file.readlines()
        
        responses = [generate_response(question.strip(), context) for question in questions]

        output_file = os.path.join(output_folder, f"responses_{input_file}")
        with open(output_file, 'w') as file:
            for response in responses:
                file.write(response + "\n")
    
    return jsonify({"message": "Questions processed successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
