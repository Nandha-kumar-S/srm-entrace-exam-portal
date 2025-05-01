# SRM Entrance Exam Portal

## Prerequisites
1. Python 3.8+
2. Google Cloud Project with OAuth 2.0 Credentials

## Setup Instructions
1. Create a Google Cloud Project
2. Enable Google OAuth 2.0
3. Download `client_secrets.json` and place in the backend directory
4. Install dependencies: `pip install -r requirements.txt`
5. Run the application: `python backend/app.py`

## Google OAuth Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Navigate to "Credentials"
4. Create OAuth 2.0 Client ID
5. Download the client configuration
6. Rename to `client_secrets.json` and place in `backend/` directory

## Security Notes
- Never commit `client_secrets.json` to version control
- Keep your credentials confidential
