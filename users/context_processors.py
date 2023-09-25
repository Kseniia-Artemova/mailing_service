from django.contrib.auth.models import Group


def is_manager(request):
    if request.user.is_authenticated:
        return {'is_manager': request.user.groups.filter(name='Managers').exists()}
    else:
        return {'is_manager': False}
