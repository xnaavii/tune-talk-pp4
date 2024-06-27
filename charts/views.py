from django.shortcuts import render
from django.db.models import Avg, Count
from home.models import Album, Review
# Create your views here.
def charts(request):

    # Fetch the top 5 albums based on average rating
    top_albums = Album.objects.annotate(average_rating=Avg('reviews__rating')).filter(average_rating__lte=5)
    top_albums = top_albums.order_by('-average_rating')[:10]
    context = {"top_albums": top_albums}

    return render(request, "charts/charts.html", context)