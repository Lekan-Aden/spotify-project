# Spotify API Flask Application

This project is a Flask-based application that integrates with the Spotify API to search for music tracks from specified shows, create a playlist,
and then add those tracks to the new playlist. The idea was borne when I had some trouble filtering spotify podcasts for specific episodes that I wanted to listen to.
For example, some of the episodes I wanted to listen to sequentially were buried down in the list, while others were recent. Interestingly, these episodes all had 
similar titles. So instead of searching for them manually, I considered automatically retrieving these episodes based on the similarities they had in their titles, and 
then saving them into a playlist I could play at once. Once done, I could then choose to delete the playlist manually or keep it for future references.


## Features
- **Spotify API Integration**: Search for items using Spotify's search endpoint.
- **Playlist Management**: Create playlist and add specific show episodes to it.
- **Secure Authentication**: Implements OAuth 2.0 for accessing Spotify's API.
- **Environment Configuration**: API keys are managed securely via a `.env` file.

## Technologies Used
- Python, Flask
- Spotify API
- Requests library
- Environment configuration with Python-dotenv

## Other Information
Besides the files in this repository, you'll need a .env file to securely store the following environment variables: `CLIENT_ID`, `CLIENT_SECRET`, and `MY_USER_ID`.

The `CLIENT_ID` and `CLIENT_SECRET` can be obtained after registering your app on Spotify for Developers.
The `MY_USER_ID` is your Spotify user ID, which can be found on your Spotify profile or via the Spotify API.
