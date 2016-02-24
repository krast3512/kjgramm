from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from kjgramm.models import Friends, Loads, Photo


@require_http_methods(["GET"])
def add_photo(request):

    return


@require_http_methods(["POST"])
def like(request):

    return


@require_http_methods(["GET"])
def comments(request):
    return


@require_http_methods(["GET"])
def people_search(request):
    return


@require_http_methods(["POST"])
def add_comment(request, text):
    return


@require_http_methods(["POST"])
def register_user(request):
    return


@require_http_methods(["GET"])
def feed(request):
    photos = []
    friends_ids = []
    new_photos = []
    for friend in Friends.objects.all():
        if friend.first_id == request.user.id:
            friends_ids.append(friend.second_id)
        elif friend.second_id == request.user.id:
            friends_ids.append(friend.first_id)
    for load in Loads.objects.all():
        if load.user_id in friends_ids:
            photos.append(load.photo_id)
    for photo_id in photos:
        new_photos.append(Photo.object.get(photo_id))
    return render(request, 'templates/feed.html', {'photos': new_photos})

