from django.shortcuts import render, get_object_or_404
from accounts.models import User

def profiles_view(request):
    users = User.objects.all()
    return render(request, "profiles/profiles_list.html", {'users': users})


def profile_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'profiles/profile_detail.html', {'profile_user': user})