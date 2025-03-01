from flask import Flask, request, jsonify
from PIL import Image
import pytesseract

import io
import firebase_admin
from firebase_admin import credentials, firestore, storage

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'certificateverification-a6ff8.appspot.com'
})

db = firestore.client()
bucket = storage.bucket()

@app.route('/upload', methods=['POST'])
def upload_certificate():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    image = Image.open(file)

    # Extract text using OCR
    text = pytesseract.image_to_string(image)

    # Upload to Firebase Storage
    blob = bucket.blob(f'certificates/{file.filename}')
    blob.upload_from_file(file)
    file_url = blob.public_url

    # Store details in Firestore
    certificate_data = {
        "student_name": "John Doe",  # Extract from text
        "certificate_id": "12345",  # Generate unique ID
        "issue_date": "2023-10-01",  # Extract from text
        "verified": True,
        "image_url": file_url
    }

    db.collection("certificates").document("12345").set(certificate_data)

    return jsonify({
        "message": "Certificate uploaded",
        "certificate_id": "12345",
        "verified": True,
        "image_url": file_url
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
