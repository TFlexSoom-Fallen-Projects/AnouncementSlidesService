# Tristan Hilbert
# Simple Flask Server to Serve to an authentication
#   payload and store the credentials

from os import environ
from flask import Flask, request, redirect, url_for, session
import google.oauth2.credentials
import google_auth_oauthlib.flow
from multiprocessing.connection import Connection, PipeConnection

# API INFO FOR REQUEST

CLIENT_SECRETS_FILE = "secrets/client_secret.json"

SCOPES = ['https://www.googleapis.com/auth/presentations']
API_SERVICE_NAME = 'slides'
API_VERSION = 'v1'

# When running locally, disable OAuthlib's HTTPs verification.
# ACTION ITEM for developers:
#     When running in production *do not* leave this option enabled.
environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


# Global Variables to serve back

# A Connection Object
pipe = None

# Google API Credential Dictionary Object
creds = None

# Create Server Variable
app = Flask(__name__)

# Obtain Secret From file
key_file = open("secrets/flask_secret.txt", "r")

# Give it to Server
app.secret_key = key_file.readline()

# Define Server Below
@app.route("/")
def start_auth():
    if creds is None or pipe is None:
        return redirect("/authstart")
    else:
        pipe.send(creds)
        return "Success"
        

# See Code Here for more info : https://developers.google.com/identity/protocols/oauth2/web-server#python
@app.route('/authstart')
def authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)

    flow.redirect_uri = url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    # Store the state so the callback can verify the auth server response.
    session['state'] = state

    return redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    global creds
    creds = flow.credentials
    
    return redirect("/")

def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}

# Run The Server
# Specify a hostname and port that are set as a valid redirect URI
# for your API project in the Google API Console.
"""
Do not use run() in a production setting. It is not intended to meet security and performance requirements for a production server. Instead, see Deployment Options for WSGI server recommendations.
"""

def run_server(pipe_p):
    if not isinstance(pipe_p, (Connection, PipeConnection)):
        print(pipe_p)
        raise TypeError

    global pipe
    pipe = pipe_p
    app.run("localhost", 8080)