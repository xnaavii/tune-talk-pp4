from .spotify_utils import get_spotify_client
from django.shortcuts import render

def get_album_metadata(search):
    sp = get_spotify_client()

    results = sp.search(q=search, type="album")

    albums = []

    for album in results['albums']['items']:
        album_info = {
            'id': album['id'],
            'name': album['name'],
            'artist': album['artists'][0]['name'],
            'release_date': album['release_date'],
            'artwork': album['images'][0]['url'] if album['images'] else None
        }
        albums.append(album_info)
        
    return albums

def get_album_info(album_data):
    
    album_info = {
        'name': album_data['name'],
        'artist': album_data['artists'][0]['name'],
        'release_date': album_data['release_date'],
        'artwork': album_data['images'][0]['url'] if album_data['images'] else None,
        'tracks': album_data['tracks']['items'] if 'tracks' in album_data else []
    }
    return album_info

def album_list(request):

    if request.method == "GET":
        search = request.GET.get("search")
        if search:
            albums = get_album_metadata(search)
        else:
            albums = []
    
        context = {
            "albums": albums, 
            "search": search
        }

        return render(request, "home/album_list.html", context)

def album_detail(request, album_id):

    sp = get_spotify_client()
    album_data = sp.album(album_id)
    album_info = get_album_info(album_data)

    context = {
        'album': album_info
    }

    return render(request, 'home/album_detail.html', context)


def home(request):
    return render(request, 'home/homepage.html')