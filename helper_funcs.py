import base64
import requests

def get_token_info(client_id, client_secret, auth_code, redirect_uri):
    """
    Retrieves the access and refresh tokens from Spotify's API using the authorization code.

    Args:
        client_id (str): The Spotify client ID of the application.
        client_secret (str): The Spotify client secret of the application.
        auth_code (str): The authorization code obtained from the Spotify authorization flow.
        redirect_uri (str): The redirect URI used in the Spotify authorization flow.

    Returns:
        tuple: A tuple containing the access token and refresh token.
    """
    # Create base64-encoded authentication string
    auth_string = client_id + ":" + client_secret
    auth_base64 = str(base64.b64encode(auth_string.encode('utf-8')), 'utf-8')
    
    token_endpoint = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + auth_base64,
        'Content-Type': 'application/x-www-form-urlencoded'
                }

    # Data payload for token request
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }

     # Send POST request to obtain tokens
    response = requests.post(token_endpoint, headers=headers, data=data).json()
    access_token = response.get('access_token')
    refresh_token = response.get('refresh_token')

    return access_token, refresh_token

def get_auth_header(access_token):
    """
    Generates the authentication header required for Spotify API requests.

    Args:
        access_token (str): The access token obtained from Spotify's API.

    Returns:
        dict: A dictionary containing the authorization header.
    """
    return {'Authorization': 'Bearer ' + access_token,
            'Content-Type':'application/json'}

def search_for_show(show_to_search_for, acc_token):
     """
    Searches for a Spotify show by name and returns the closest match.

    Args:
        show_to_search_for (str): The name of the show to search for.
        acc_token (str): The access token for Spotify API authentication.

    Returns:
        tuple: A tuple containing the name and ID of the closest matching show.
    """
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(acc_token)
    query = f'?q={show_to_search_for}&type=show&limit=1&market=NG'

    query_url = url + query
    result = requests.get(query_url, headers=headers)

    # Check for API errors
    if result.status_code != 200:
        return 'Encountered an error.'
    json_result = result.json()
    print(f"\nFound {json_result['shows']['total']} shows. Returning the closest match.")
   
    # Extract show name and ID from the response
    show_name, show_id = json_result['shows']['items'][0]['name'], json_result['shows']['items'][0]['id']
    print('Closest match:', show_name)
    return show_name, show_id

def get_particular_episodes(episode_keyword, show_id, acc_token, limit=50):
    """
    Retrieves episodes of a specific show that match a given keyword.

    Args:
        episode_keyword (str): A keyword to filter episodes by name.
        show_id (str): The Spotify ID of the show.
        acc_token (str): The access token for Spotify API authentication.
        limit (int, optional): The maximum number of episodes to retrieve per batch. Defaults to 50.

    Returns:
        list: A list of URIs for episodes matching the keyword.
    """
    # Spotify endpoint for retrieving episodes of a specific show
    show_url = f'https://api.spotify.com/v1/shows/{show_id}/episodes'
    query = f'?limit={limit}&market=NG&offset=0'
    query_url = show_url + query
    headers = get_auth_header(acc_token)
    
    # Store matching episode names and uris
    names_of_desired_episodes = []
    uris_of_desired_episodes = []
    
    while query_url is not None:
        batch = requests.get(query_url, headers=headers).json()
        # Filter episodes based on the keyword
        for item in batch['items']:
            if episode_keyword.lower() in item['name'].lower():
                names_of_desired_episodes.append(item['name'])
                uris_of_desired_episodes.append(item['uri'])
        query_url = batch['next']    # Proceed to the next batch if available
    print(f'Found episode(s):', '\n'.join(names_of_desired_episodes))

    return uris_of_desired_episodes