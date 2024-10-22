import base64
import requests

def get_token_info(client_id, client_secret, auth_code, redirect_uri):
    auth_string = client_id + ":" + client_secret
    auth_base64 = str(base64.b64encode(auth_string.encode('utf-8')), 'utf-8')
    
    token_endpoint = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + auth_base64,
        'Content-Type': 'application/x-www-form-urlencoded'
                }
    
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(token_endpoint, headers=headers, data=data).json()
    access_token = response.get('access_token')
    refresh_token = response.get('refresh_token')

    return access_token, refresh_token

def get_auth_header(access_token):
    return {'Authorization': 'Bearer ' + access_token,
            'Content-Type':'application/json'}

def search_for_show(show_to_search_for, acc_token):
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(acc_token)
    query = f'?q={show_to_search_for}&type=show&limit=1&market=NG'

    query_url = url + query
    result = requests.get(query_url, headers=headers)
    if result.status_code != 200:
        return 'Encountered an error.'
    json_result = result.json()
    print(f"\nFound {json_result['shows']['total']} shows. Returning the closest match.")
    show_name, show_id = json_result['shows']['items'][0]['name'], json_result['shows']['items'][0]['id']
    print('Closest match:', show_name)
    return show_name, show_id

def get_particular_episodes(episode_keyword, show_id, acc_token, limit=50):
    show_url = f'https://api.spotify.com/v1/shows/{show_id}/episodes'
    query = f'?limit={limit}&market=NG&offset=0'
    query_url = show_url + query
    headers = get_auth_header(acc_token)
    
    names_of_desired_episodes = []
    uris_of_desired_episodes = []
    
    while query_url is not None:
        batch = requests.get(query_url, headers=headers).json()
        for item in batch['items']:
            if episode_keyword.lower() in item['name'].lower():
                names_of_desired_episodes.append(item['name'])
                uris_of_desired_episodes.append(item['uri'])
        query_url = batch['next']
    print(f'Found episode(s):', '\n'.join(names_of_desired_episodes))

    return uris_of_desired_episodes