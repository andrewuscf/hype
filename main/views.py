from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from main.forms import UserForm
from django.shortcuts import render, redirect, get_object_or_404


def index(request):
    if request.user.is_authenticated():
        id = request.user.id
        user = User.objects.get(id=id)
        data = {
            'user': user,
        }
        return render(request, "home.html", data)
    else:
        return render(request, "splash.html")


@login_required
def profile(request, username):
    get_object_or_404(User, username=username)
    return render(request, 'profile.html', {'profile_user': username})


@login_required
def privacy(request, template='privacy.html'):
    return render(request, template)


@login_required
def settings(request):
    form_class = UserForm
    user = request.user
    userdata = User.objects.get(username=user)
    data = {
        'userform': form_class(instance=userdata),
    }
    if request.method == 'POST':
        print 'test'
        form = form_class(request.POST, instance=userdata)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            User.objects.filter(username=user).update(username=username, first_name=first_name, last_name=last_name)
            return redirect('/users/{}'.format(user))
        else:
            return render(request, 'settings.html', data)
    else:
        print 'hitttttt'
        return render(request, 'settings.html', data)
