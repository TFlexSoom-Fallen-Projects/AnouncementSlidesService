# Sour_Tooth and TFlexSoom
# 4/30/2020
# Entry Script For Application

"""
Later on we should create files for these processes but for now I will
post them underneath commented sections to allow for seperation
"""


### First Start a Flask Server to Handle OAuth so we can snag crednetials
import flask
from flask import request as req
import os
import requests
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from multiprocessing import Process
from time import sleep

# Create Server Variabel
app = flask.Flask(__name__)

# Obtain Secret From file
key_file = open("secrets/flask_secret.txt", "r")

# Give it to Server
app.secret_key = key_file.readline()

# API INFO FOR REQUEST

CLIENT_SECRETS_FILE = "secrets/client_secret.json"


SCOPES = ['https://www.googleapis.com/auth/presentations']
API_SERVICE_NAME = 'slides'
API_VERSION = 'v1'


# ------------------



# The server's job is to populate this variable:
creds = None

# Then send it to this process
nextProcess = None

# Define Server Below
@app.route("/")
def start_auth():
    if creds == None:
        return flask.redirect("/authstart")
    else:
        func = req.environ.get('werkzeug.server.shutdown')
        func()
        nextProcess.run()
        return "Success"
        

# See Code Here for more info : https://developers.google.com/identity/protocols/oauth2/web-server#python
@app.route('/authstart')
def authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)

    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    # Store the state so the callback can verify the auth server response.
    flask.session['state'] = state

    return flask.redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = flask.session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    global creds
    creds = flow.credentials
    

    return flask.redirect("/")

def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


### Next Do Stuff With Credentials

def run():
    if creds == None:
        print("No OAuth Credentials!")
    else:
        derp = open("log.txt", "w")
        derp.write("Success!\n")
        derp.write(repr(creds))


### Run it all
def main():
    # When running locally, disable OAuthlib's HTTPs verification.
    # ACTION ITEM for developers:
    #     When running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    # Specify a hostname and port that are set as a valid redirect URI
    # for your API project in the Google API Console.
    """
    Do not use run() in a production setting. It is not intended to meet security and performance requirements for a production server. Instead, see Deployment Options for WSGI server recommendations.
    """

    global nextProcess
    nextProcess = Process(target=run)

    app.run("localhost", 8080, debug=True)

if __name__ == "__main__":
    main()
