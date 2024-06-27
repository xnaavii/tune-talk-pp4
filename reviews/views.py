from django.shortcuts import render

# Create your views here.
def reviews(request):

    test = "Hello World!"

    context = {"test": test}
    return render(request, 'reviews/reviews.html', context)