from django.shortcuts import render

def threads_view(request):
    return render(request, "threads.html")