import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def get_spotify_client():
    """
    Set up spotify client credentials manager
    """
    client_id = os.environ.get("SPOTIPY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")
    auth_manager = SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret
        )

    return spotipy.Spotify(auth_manager=auth_manager)
