from flask import Flask, jsonify
from config.settings import configure_app
import firebase_admin
from firebase_admin import credentials, firestore
import os

app = Flask(__name__)
configure_app(app)

# Firebase Admin SDK setup
cred = credentials.Certificate("firebase-auth.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Register blueprints
from routes.auth import auth_bp
from routes.public import public_bp
from routes.dashboard import dashboard_bp
from routes.pdf_summarizer import pdf_bp
from routes.profile import profile_bp

app.register_blueprint(auth_bp)
app.register_blueprint(public_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(pdf_bp, url_prefix='/pdf')
app.register_blueprint(profile_bp)


# Firebase config endpoint
@app.route('/api/firebase-config')
def get_firebase_config():
    # 이 정보들은 public하게 공개해도 됩니다 (Firebase 보안 규칙으로 보호됨)
    config = {
        "apiKey": os.getenv('FIREBASE_API_KEY'),
        "authDomain": os.getenv('FIREBASE_AUTH_DOMAIN'),
        "projectId": os.getenv('FIREBASE_PROJECT_ID'),
        "storageBucket": os.getenv('FIREBASE_STORAGE_BUCKET'),
        "messagingSenderId": os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
        "appId": os.getenv('FIREBASE_APP_ID')
    }
    return jsonify(config)

if __name__ == '__main__':
    app.run(debug=True)