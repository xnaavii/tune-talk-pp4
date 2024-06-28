from django.shortcuts import render
from django.db.models import Avg, Count
from home.models import Album


def charts(request):

    # Annotate albums with average rating and review count
    albums = Album.objects.annotate(
        average_rating=Avg("reviews__rating"), review_count=Count("reviews")
    )

    # Filter albums to have an average rating >= 1
    albums_with_rating = albums.filter(average_rating__gte=1)

    # Determine the top album based on highest average rating and most reviews
    if albums_with_rating.exists():
        top_album = albums_with_rating.order_by(
            "-average_rating", "-review_count"
        ).first()
    else:
        top_album = None

    # Fetch the next top 5 albums based on average rating, excluding the top album
    top_albums = (
        albums_with_rating.exclude(pk=top_album.pk).order_by("-average_rating")[:5]
        if top_album
        else []
    )

    # Fetch the top 5 albums based on the number of reviews
    most_reviewed_albums = albums.order_by("-review_count")[:5]

    context = {
        "top_albums": top_albums,
        "most_reviewed_albums": most_reviewed_albums,
        "top_album": top_album,
    }

    return render(request, "charts/charts.html", context)
