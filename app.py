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

const photoInput = document.getElementById('photoInput');
const preview = document.getElementById('preview');
const result = document.getElementById('result');

let file; // siin hoiame valitud faili

photoInput.addEventListener('change', (e) => {
    file = e.target.files[0];
    preview.src = URL.createObjectURL(file);
});

document.getElementById('sendBtn').addEventListener('click', async () => {
    if (!file) return alert('Vali foto!');

    // 1️⃣ loe fail Base64 stringina
    const reader = new FileReader();
    reader.onload = async () => {
        const base64 = reader.result.split(',')[1]; // eemaldab "data:image/..." osa

        // 2️⃣ tee OCR (Tesseract.js)
        const { data: { text } } = await Tesseract.recognize(file, 'eng');

        result.textContent = text;

        // 3️⃣ saada Google Apps Scripti URL-ile
        fetch('SINU_WEB_APP_URL', {
            method: 'POST',
            body: JSON.stringify({ tekst: text, pilt: base64 }),
            headers: { 'Content-Type': 'application/json' }
        })
        .then(res => res.json())
        .then(res => alert('Tekst ja pilt saadetud Google Docsi!'))
        .catch(err => alert('Viga Google Docsi saatmisel: ' + err));
    };
    reader.readAsDataURL(file); // loeb faili Base64 stringina
});
