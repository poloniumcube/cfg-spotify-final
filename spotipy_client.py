from dotenv import load_dotenv
import os
import base64
import json
import urllib.parse
import requests
import webbrowser

# limit at N-requests an hour, I think 60 or so? commented out so I don't go over the limit while testing
 
load_dotenv()

client_id = os.getenv('CLIENT_ID') # could've made it static, but best practices are still a thing 
client_secret = os.getenv('CLIENT_SECRET')

def get_token(): 
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = requests.post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return{"Authorization": "Bearer " + token}

def search_track(token, track_name, artist_name):
    url = "https://api.spotify.com/v1/search" # base endpoint
    headers = get_auth_header(token)

    # URL encode 
    track_name_encoded = urllib.parse.quote(track_name)
    artist_name_encoded = urllib.parse.quote(artist_name)
    
    # query with encoded parameters
    query = f"?q=track:{track_name_encoded}%20&artist:{artist_name_encoded}&type=track&limit=1"
    query_url = url + query
    
    # get request + parsing the JSON response to get the track ID
    result = requests.get(query_url, headers=headers)
    json_result = result.json()
    items = json_result['tracks']['items']
    if items:
        track_id = items[0]['id']
        query_url = f"https://open.spotify.com/track/{track_id}"
        webbrowser.open(query_url) 

token = get_token()
