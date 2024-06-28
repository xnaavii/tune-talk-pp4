from django.shortcuts import render
from .models import About


# Create your views here.
def about_page(request):
    about = About.objects.all()
    context = {"about": about}

    return render(request, "about/about.html", context)
