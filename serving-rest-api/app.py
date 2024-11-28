from flask import Flask, request, jsonify
import pickle
import re
from flask_cors import CORS

# Load model, vectorizer, and label encoder
with open("/app/model.pkl", "rb") as f:
    loaded_data = pickle.load(f)

model = loaded_data['model']
vectorizer = loaded_data['vectorizer']
label_encoder_classes = loaded_data['label_encoder']

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Preprocessing function for text
def preprocess_text(text):
    text = re.sub(r'[!@#$(),\n"%^*?\:;~`0-9]', '', text)  # Remove special characters and digits
    text = re.sub(r'[[]]', '', text)  # Remove square brackets
    text = text.lower()  # Convert to lowercase
    return text

@app.route('/predict', methods=['POST'])
def predict_language():
    data = request.get_json()  # Get input data in JSON format
    if 'text' not in data:
        return jsonify({"error": "No text provided"}), 400
    
    input_text = data['text']
    input_text = preprocess_text(input_text)  # Preprocess input text
    input_vector = vectorizer.transform([input_text])  # Vectorize the input text
    
    # Predict the class
    predicted_class = model.predict(input_vector)
    
    # Decode the predicted class to the original label
    predicted_label = label_encoder_classes[predicted_class[0]]
    
    return jsonify({"predicted_language": predicted_label})

if __name__ == '__main__':
    app.run(debug=True)