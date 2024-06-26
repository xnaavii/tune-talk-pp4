from .spotify_utils import get_spotify_client
from .models import Album, Artist, Review
from .forms import ReviewForm
from django.shortcuts import render, redirect
from spotipy.client import SpotifyException

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

def get_album_info(album_id):
    sp = get_spotify_client()
    album_data = sp.album(album_id)

    try:
        album_data = sp.album(album_id)
    except SpotifyException as e:
        # Handle Spotify API exception
        print(f"Error fetching album data for {album_id}: {e}")
        return None

    if not album_data:
        print(f"Album data for {album_id} is None")
        return None

    # Save artist if not already in the database
    artist_data = album_data['artists'][0]
    artist, _ = Artist.objects.get_or_create(
        artist_id=artist_data['id'],
        defaults={'artist_name': artist_data['name']}
    )

    # Save album
    album, _ = Album.objects.get_or_create(
        album_id=album_id,
        defaults={
            'album_id': album_id,
            'title': album_data['name'],
            'artist': artist,
            'released': album_data['release_date'],
            'artwork': album_data['images'][0]['url'] if album_data['images'] else None,
        }
    ) 

    # Extract tracks from album data 
    tracks = []
    if 'tracks' in album_data:
        tracks = album_data['tracks']['items']

    return album, tracks

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

    album_info_spotify, tracks = get_album_info(album_id)

    # Handle review form submission
    if request.method == "POST":
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.album = album_info_spotify
            review.author = request.user
            review.save()
            return redirect('album_detail', album_id=album_id)  # Redirect after successful form submission
    else:
        review_form = ReviewForm()

    # Fetch all reviews for the album
    reviews = album_info_spotify.reviews.all()

    context = {
        "album": album_info_spotify,
        "tracks": tracks,
        "review_form": review_form,
        "reviews": reviews
    }

    return render(request, 'home/album_detail.html', context)


def home(request):
    return render(request, 'home/homepage.html')