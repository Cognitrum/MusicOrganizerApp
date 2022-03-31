import requests
import os

clear = lambda: os.system('cls')
clear()

redirect_uri = 'https://accounts.spotify.com/authorize?client_id=d6a10720dd914d058cfd78d9fa6c7e1d&scope=user-library-read&response_type=code&redirect_uri=http://localhost:5000/callback\n'

print('Please paste this link into your browser and complete authorization:\n\n',redirect_uri, '\n')

code_uri = input('Please enter new URL: \n\n')

code_uri_parsed = code_uri.split("=")

callback_code = code_uri_parsed[1]

# print(callback_code)

response = requests.post(
    'https://accounts.spotify.com/api/token',
    params={
        'grant_type': "authorization_code",
        'code': callback_code,
        'redirect_uri': "http://localhost:5000/callback"
    },
    headers={
        'Content-Type': "application/x-www-form-urlencoded"
    },
    data={
        'client_id': "ZDZhMTA3MjBkZDkxNGQwNThjZmQ3OGQ5ZmE2YzdlMWQ",
        'client_secret': "OGVhODRiMmYwNWYzNGI3YjlmMDU2YjQxZjg3YjhiNTc"
    }
)

response.encoding = "application/x-www-form-urlencoded"

# response_str = 'https://accounts.spotify.com/api/token?grant_type=authorization_code?code=',callback_code,'?redirect_uri=http://localhost:5000/callback -H '

print(response)