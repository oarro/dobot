from flask import Flask, request, render_template, jsonify
from PIL import Image
import pytesseract
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'photo' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['photo']
    img = Image.open(file.stream)
    text = pytesseract.image_to_string(img)
    return jsonify({'text': text})

if __name__ == '__main__':
    app.run(debug=True)
