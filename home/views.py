from .spotify_utils import get_spotify_client
from .models import Album, Artist, Review
from .forms import ReviewForm
from django.http import HttpResponseForbidden
from django.db.models import Avg, Count
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
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
    # Fetch all reviews for the album
    reviews = album_info_spotify.reviews.all()

    # Handle review form submission
    if request.method == "POST":
        if 'review_id' in request.POST:
            review_id = request.POST.get('review_id')
            review = get_object_or_404(Review, id=review_id)

            if 'edit' in request.POST:
                if review.author == request.user:
                    review_form = ReviewForm(data=request.POST, instance=review)
                    if review_form.is_valid():
                        review_form.save()
                else:
                    return HttpResponseForbidden("You are not allowed to edit this review.")
            elif 'delete' in request.POST:
                if review.author == request.user:
                    review.delete()
                else:
                    return HttpResponseForbidden("You are not allowed to delete this review.")
        else:
            review_form = ReviewForm(data=request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.author = request.user
                review.album = album_info_spotify
                review.save()
    else:
        review_form = ReviewForm()

    context = {
        "album": album_info_spotify,
        "tracks": tracks,
        "review_form": review_form,
        "reviews": reviews
    }

    return render(request, 'home/album_detail.html', context)

def edit_review(request, album_id, review_id):
    album = get_object_or_404(Album, album_id=album_id)
    review = get_object_or_404(Review, id=review_id)

    if request.user == review.author:
        form = ReviewForm(request.POST or None, instance=review)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'Review updated successfully.')
                return redirect('album_detail', album_id=album_id)
        context = {
            'album': album,
            'form': form,
        }
        return render(request, 'home/edit_review.html', context)
    else:
        messages.error(request, 'You are not allowed to edit this review.')
        return redirect('album_detail', album_id=album_id)

def delete_review(request, album_id, review_id):
    album = get_object_or_404(Album, album_id=album_id)
    review = get_object_or_404(Review, id=review_id)

    if request.user == review.author:
        review.delete()
        messages.success(request, 'Review deleted successfully.')
    else:
        messages.error(request, 'You are not allowed to delete this review.')

    return redirect('album_detail', album_id=album_id)

def home(request):
    # Query albums with an average rating less than or equal to 5, annotated with average rating and count of reviews
    albums = Album.objects.annotate(
        average_rating=Avg('reviews__rating'),
        num_reviews=Count('reviews')
        ).filter(average_rating__lte=5)
    
    albums = albums.order_by('-average_rating','-num_reviews')[:3]
    latest_reviews = Review.objects.all().order_by("-created_at")[:3]

    context = {
        "albums": albums,
        "latest_reviews": latest_reviews   
        }

    return render(request, 'home/homepage.html', context)