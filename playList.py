from helper_funcs import get_auth_header
import requests

class Playlist:
    """
    A class to create and manage Spotify playlists using the Spotify API.

    Attributes:
        name (str): The name of the playlist.
        description (str): The description of the playlist.
        public (bool): Whether the playlist is public (default is True).
        id (str): The Spotify ID of the created playlist.

    Methods:
        __str__(): Returns a string representation of the playlist.
        add_tracks(episode_uris, token): Adds tracks or episodes to the playlist.
    """

    def __init__(self, owner_id, name, description, token, public=True):
        """
        Initializes the Playlist instance by creating a new Spotify playlist.

        Args:
            owner_id (str): The Spotify user ID of the playlist owner.
            name (str): The name of the playlist.
            description (str): The description of the playlist.
            token (str): The access token for Spotify API authentication.
            public (bool, optional): Whether the playlist is public. Defaults to True.
        """

        self.name = name
        self.description = description
        self.public = public

        # API endpoint to create a new playlist
        endpoint = f'https://api.spotify.com/v1/users/{owner_id}/playlists'
        
        # Prepare authentication headers and data payload
        headers = get_auth_header(token)
        data = {'name': self.name,
                'description': self.description,
                'public': self.public
                }

        # Send POST request to Spotify API to create the playlist
        result = requests.post(endpoint, headers=headers, json=data).json()
        self.id = result['id']

    def __str__(self):
        return f"Playlist `{self.name}` with id {self.id}.\nDescription: {self.description}\npublic: {self.public}"

    def add_tracks(self, episode_uris, token):
        """
        Add podcast episodes to the playlist.

        Args:
            episode_uris (list of str): A list of Spotify URIs for the tracks or episodes to add.
            token (str): The access token for Spotify API authentication.

        Returns:
            None
        """

        # API endpoint to add tracks to a playlist
        endpoint = f'https://api.spotify.com/v1/playlists/{self.id}/tracks'
        headers = get_auth_header(token)
        data = {'uris': episode_uris}

        print('\nProceeding to add these episodes to your playlist.')
        
        # Send POST request and notify of response status
        result = requests.post(endpoint, headers=headers, json=data)
        if result.status_code == 200:
            print('Tracks successfully added')
        else:
            print(result.json())