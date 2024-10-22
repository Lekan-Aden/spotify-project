from helper_funcs import get_auth_header
import requests

class Playlist:
    def __init__(self, owner_id, name, description, token, public=True):
        self.name = name
        self.description = description
        self.public = public

        endpoint = f'https://api.spotify.com/v1/users/{owner_id}/playlists'
        headers = get_auth_header(token)
        data = {'name': self.name,
                'description': self.description,
                'public': self.public
                }

        result = requests.post(endpoint, headers=headers, json=data).json()
        self.id = result['id']

    def __str__(self):
        return f"Playlist `{self.name}` with id {self.id}.\nDescription: {self.description}\npublic: {self.public}"

    def add_tracks(self, episode_uris, token):  
        endpoint = f'https://api.spotify.com/v1/playlists/{self.id}/tracks'
        headers = get_auth_header(token)
        data = {'uris': episode_uris}

        print('\nProceeding to add these episodes to your playlist.')
        result = requests.post(endpoint, headers=headers, json=data)
        if result.status_code == 200:
            print('Tracks successfully added')
        else:
            print(result.json())