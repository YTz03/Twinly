from django.shortcuts import render

def matching_view(request):
    return render(request, "matching/matching.html")


def match_list(request):
    # Placeholder: list of matches; replace with your matching logic
    matches = []
    return render(request, 'matching/match_list.html', {'matches': matches})