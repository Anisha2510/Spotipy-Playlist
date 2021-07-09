import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT_ID = "ae2f32a52b3f4767a1c1ffd42bf5f81a"
SPOTIPY_CLIENT_SECRET = "c4ef8c1d9cfe483e87271285876337bb"
SPOTIPY_REDIRECT_URI = "http://example.com"
scope = "playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope,
                                               show_dialog=True,
                                               cache_path="token.txt"
                                               )
                     )

URL = "https://www.billboard.com/charts/hot-100/"

date = input("Which year do you want to travel to? (YYYY-MM-DD)")
date_list = date.split("-")
year = date_list[0]

response = requests.get(URL+date)
website_html = response.text
soup = BeautifulSoup(website_html, "html.parser")

songs = soup.find_all(name="span", class_="chart-element__information__song")
song_names = [song.getText() for song in songs]
# print(song_names)

user_id = sp.current_user()["id"]
# print(user_id)
song_uris = []
USER = "anishaanil1025"

# with open(file="token.txt") as file:
#     data = file.readlines()
# print(data[0])
# token = data["access_token"]


for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=USER,
                                   name=f"{date} Billboard 100",
                                   public=False,
                                   collaborative=False
                                   )
# print(playlist)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
