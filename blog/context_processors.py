from accounts.models import Profile

def common(request):
    profile_data = Profile.objects.get(pk=request.user.id)
    context = {
        'profile_data': profile_data,
    }
    return context
