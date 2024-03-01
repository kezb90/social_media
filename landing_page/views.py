from django.shortcuts import render

# Create your views here.


def landing_page(request):
    return render(request, "main.html")


def about_us(request):
    return render(request, "about_us.html")
