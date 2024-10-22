import os
from dotenv import load_dotenv
import base64
import requests
import urllib.parse
from flask import Flask, redirect, request
from helper_funcs import get_token_info, get_auth_header, search_for_show, get_particular_episodes
from playList import Playlist

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
user_id = os.getenv('MY_USER_ID')
redirect_uri = 'http://localhost:5000/callback'
access_token = refresh_token = None

app = Flask(__name__)

@app.route('/')
def home():
	return redirect('/login')  # Automatically redirect to the /login route

@app.route('/login')
def login():
	auth_endpoint = 'https://accounts.spotify.com/authorize?'
	scopes = ['playlist-modify-public', 'playlist-modify-private']

	params = {
	    'client_id': client_id,
	    'response_type': 'code',
	    'redirect_uri': redirect_uri,
	    'scope': ' '.join(scopes),
	    'show_dialog': 'false'
	}

	auth_url = f'{auth_endpoint}{urllib.parse.urlencode(params)}'

	# Redirect the user to the Spotify authorization page
	return redirect(auth_url)

@app.route('/callback')
def callback():
	# Get the authorization code from the query string
	authorization_code = request.args.get('code')
	if authorization_code:
		global access_token, refresh_token
		access_token, refresh_token = get_token_info(client_id, client_secret, authorization_code, redirect_uri)
		return f"Successful. Tokens Received."
	else:
		return "Error: No authorization code provided."

if __name__ == '__main__':
	app.run(port=5000)

playlist_name = str(input('Enter playlist name: '))
playlist_description = str(input('Enter playlist description: '))
playlist = Playlist(user_id, playlist_name, playlist_description, access_token)
print(playlist)
print()

show_of_interest = str(input('Enter the show you are looking for: '))
show_name, show_id = search_for_show(show_of_interest, access_token)
if show_of_interest.lower() not in show_name.lower():
	print('Show names do not match! Quitting...')
	quit()
else:
	episode_keyword = str(input('Enter the episode keyword: '))
	episode_uris = get_particular_episodes(episode_keyword, show_id, access_token)
	playlist.add_tracks(episode_uris, access_token)