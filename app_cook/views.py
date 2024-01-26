from django.shortcuts import render

# Create your views here.


def index(request):
    context = {
        "hello": "Hello World!",
    }
    return render(request, "app_cook/index.html", context)