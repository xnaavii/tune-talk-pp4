from django.shortcuts import render
from django.db.models import Q
from home.models import Review


def reviews(request):
    """
    Render the reviews page with a list of all reviews,
    optionally filtered by a search term.

    This view fetches all reviews from the database and orders them
    by creation date in descending order.
    If a search term is provided through the GET request,
    it filters the reviews to include only those
    where the search term is found in the title, body,
    author's username, or album's artist name.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse:
        The rendered 'reviews/reviews.html' template with the context
        containing the list of all reviews.

    Context:
        all_reviews: QuerySet of Review objects,
        either all reviews or those filtered by the search term.
    """
    all_reviews = Review.objects.all().order_by("-created_at")

    # Handling search functionality for reviews
    search_term = request.GET.get("search")
    if search_term:
        all_reviews = all_reviews.filter(
            Q(title__icontains=search_term)
            | Q(body__icontains=search_term)
            | Q(author__username__icontains=search_term)
            | Q(album__artist__artist_name__icontains=search_term)
        )

    context = {"all_reviews": all_reviews}
    return render(request, "reviews/reviews.html", context)
