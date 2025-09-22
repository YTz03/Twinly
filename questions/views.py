from django.shortcuts import render

def questions_view(request):
    return render(request, "questions.html")
