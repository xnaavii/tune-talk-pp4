import os
import spotipy
from django.shortcuts import render
from spotipy.oauth2 import SpotifyClientCredentials

def get_spotify_client():
    """
    Set up spotify client credentials manager
    """
    client_id = os.environ.get("SPOTIPY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

    return spotipy.Spotify(auth_manager=auth_manager)

def album_list(request):

    sp = get_spotify_client()

    if request.method == "GET":

        search = request.GET.get("search")

        results = sp.search(q=search, type="album")

        albums = []

        for album in results['albums']['items']:
            album_info = {
                'name': album['name'],
                'artist': album['artists'][0]['name'],
                'release_date': album['release_date'],
                'artwork': album['images'][0]['url'] if album['images'] else None
            }
            albums.append(album_info)
        
        context = {
            "albums": albums, "search": search
        }


        return render(request, "home/album_list.html", context)


def home(request):
    return render(request, 'home/homepage.html')