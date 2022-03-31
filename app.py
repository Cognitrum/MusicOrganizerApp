import requests
import json
import time
from flask import Flask, redirect, url_for, request
post_array = []
access_token = ''

app = Flask(__name__)

@app.route('/')
def index():
    
    return '<a href="https://accounts.spotify.com/authorize?client_id=d6a10720dd914d058cfd78d9fa6c7e1d&scope=user-library-read&response_type=code&redirect_uri=http://localhost:5000/callback">Click Me!</a>'

@app.route('/callback')
def callback():
    callback_code = request.args.get("code")
    authentication_array(callback_code)
    
    return redirect('/tracks')

@app.route('/tracks')
def tracks(): 
    
    tracklist_array = user_artist_ids()
    show_array = get_genre_data(tracklist_array)
    
    return {"result":show_array}

def get_genre_data(tracklist_array):

    parsed_token = access_token
    token_str = "Bearer " + parsed_token

    index = 0
    genre_array = []

    genre_array2 = set([])
    start_time = time.time()
    while index in range(len(tracklist_array)):
        print(index)
        url = 'https://api.spotify.com/v1/artists/' + tracklist_array[index]

        response = requests.get(
            url,
            headers = {
                'Authorization': token_str
            },
            params={
                'market':"US",
                'limit': 50
            }
        )

        response_json = response.json()
        index += 1


        for obj in response_json.get("genres"):
            if obj not in genre_array:
                genre_array.append(obj)
        
            # genre_array2.add(obj)
    end_time = start_time - time.time()
    print(end_time)
    return genre_array





def user_artist_ids(): 
    
    parsed_token = access_token(post_array)
    token_str = "Bearer " + parsed_token
    response = requests.get(
        'https://api.spotify.com/v1/me/tracks',
        headers = {
            'Authorization': token_str
        },
        params={
            'market':"US",
            'limit': 50
        }
    )
    
    response_json = response.json()

    tracklist_array = []
    index = 0

    while (response_json.get("next") != None) and (index <= 13*50):

        response = requests.get(
            "https://api.spotify.com/v1/me/tracks",
            headers={
                'Authorization': token_str
            },
            params={
                'market':"US",
                'limit': 50,
                'offset': index
            }
        )
        response_json2 = response.json()
        index += 50
        for obj in response_json2.get("items"):
            for temp in obj.get("track").get("artists"):
                tracklist_array.append(temp.get("id"))
        
    return tracklist_array
    
def authentication_array(callback_code):
    global post_array

    response = requests.post(
        'https://accounts.spotify.com/api/token',
        headers={
            'Content-Type': "application/x-www-form-urlencoded"
        },
        data={
            'client_id': "d6a10720dd914d058cfd78d9fa6c7e1d",
            'client_secret': "8ea84b2f05f34b7b9f056b41f87b8b57",
            'grant_type': "authorization_code",
            'code': callback_code,
            'redirect_uri': "http://localhost:5000/callback"
        }
    )
    post_array = response.json()
    return

def access_token(post_array):

    global access_token
    access_token = post_array.get("access_token")

    return access_token

def refresh_token(post_array):

    refresh_token = post_array.get("refresh_token")

    response = requests.post(
        'https://accounts.spotify.com/api/token',
        headers={
            'Content-Type': "application/x-www-form-urlencoded"
        },
        data={
            'client_id': "d6a10720dd914d058cfd78d9fa6c7e1d",
            'grant_type': "refresh_token",
            'refresh_token': refresh_token
        }
    )
    response_json = response.json()
    print(refresh_token)
    print(response_json)
    new_token = response_json.get("access_token")
    print(new_token)
    return refresh_token
