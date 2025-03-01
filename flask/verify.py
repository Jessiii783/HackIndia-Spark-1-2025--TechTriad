import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate("D:\web")  # Replace with the correct path
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

@app.route('/verify/<certificate_id>', methods=['GET'])
def verify_certificate(certificate_id):
    doc_ref = db.collection("certificates").document(certificate_id)
    doc = doc_ref.get()

    if doc.exists:
        return jsonify(doc.to_dict()), 200
    else:
        return jsonify({"error": "Certificate not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)

