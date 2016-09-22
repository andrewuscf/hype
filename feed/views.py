from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from feed.models import Event


@login_required
def find_friends(request):
    return render(request, 'find_friends.html', {})


@login_required
def find_event(request):
    return render(request, 'find_event.html', {'events': Event.objects.all()})


@login_required
def create_event(request):
    return render(request, "event_post.html")


@login_required
def view_event(request, id=None):
    posts = Event.objects.get(id=id)
    data = {
        'posts': posts,
    }
    return render(request, 'view_event.html', data)
