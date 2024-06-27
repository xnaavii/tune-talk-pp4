from django.shortcuts import render
from django.db.models import Avg, Count
from home.models import Album, Review
# Create your views here.
def charts(request):

    tests = "TESTING"

    context = {"tests": tests}

    return render(request, "charts/charts.html", context)