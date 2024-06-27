from django.shortcuts import render
from django.db.models import Q
from home.models import Review
# Create your views here.
def reviews(request):

    all_reviews = Review.objects.all().order_by('-created_at')

    # Handling search functionality
    search_term = request.GET.get('search')
    if search_term:
        all_reviews = all_reviews.filter(
            Q(title__icontains=search_term)|
            Q(body__icontains=search_term)|
            Q(author__username__icontains=search_term)|
            Q(album__artist__artist_name__icontains=search_term)
        )

    context = {"all_reviews": all_reviews}
    return render(request, 'reviews/reviews.html', context)