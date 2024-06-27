from django.shortcuts import render
from home.models import Review
# Create your views here.
def reviews(request):

    reviews = Review.objects.all()

    context = {"reviews": reviews}
    return render(request, 'reviews/reviews.html', context)