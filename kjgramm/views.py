import os

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from kjgramm.forms import SearchForm, PhotoModelForm, CommentForm
from kjgramm.models import Loads, Photo, Liked, Commented, Post, Followed


def filter_followed(user):
    return User.objects.filter(followed__follower=user)


def exclude_followed_self(user):
    return User.objects.exclude(followed__follower=user).exclude(pk=user.pk)


def filter_followers(user):
    return User.objects.filter(follower__followed=user)


def exclude_followers_self(user):
    return User.objects.exclude(follower__followed=user).exclude(pk=user.pk)


def can_user_like(user, photo):
    return not Liked.objects.filter(user=user, photo=photo).exists() \
           and not Loads.objects.filter(user=user, photo=photo).exists()


@require_http_methods(["POST", "GET"])
def media_file(request, path, document_root):

    # File upload
    if request.method == "POST":
        form = PhotoModelForm(request.POST, request.FILES)

        if form.is_valid():
            new_photo = form.save()

            load_instance = Loads.objects.create(user=request.user, photo=new_photo)
            load_instance.save()

        return HttpResponseRedirect("/feed/")

    # Display image
    else:
        with open(os.path.join(document_root, path)) as image:
            return HttpResponse(content=image.read(), content_type="image/jpg")


@require_http_methods(["POST"])
def like(request, photo_id):
    # One person should not be able to like the same photo twice
    like_repeated = Liked.objects.filter(user=request.user, photo=Photo.objects.get(pk=photo_id)).exists()

    if not like_repeated:
        photo = Photo.objects.get(pk=photo_id)
        photo.likes_num += 1
        photo.save()

        Liked.objects.create(user_id=request.user.id, photo_id=photo_id).save()

    return HttpResponseRedirect(request.POST.get('next'))


@require_http_methods(["GET"])
def comments(request, photo_id):
    comments_on_photo = []

    for commented_instance in Commented.objects.all():
        if commented_instance.photo.id == int(photo_id):
            comments_on_photo.append((commented_instance.post, commented_instance.user))

    photo = Photo.objects.get(pk=photo_id)

    return render(request, 'comments.html', {
        'photo': photo,
        'comments_on_photo': comments_on_photo,
        'can_like': can_user_like(request.user, photo)
    })


@login_required
@require_http_methods(["GET", "POST"])
def people_search(request):
    # Post method means actual search being performed
    if request.method == "POST":
        form = SearchForm(request.POST)
        if not form.is_valid():
            return render(request, 'people.html', {'people': [], 'form': form})
        search = form.cleaned_data['search']

        non_friend_results = exclude_followed_self(request.user).filter(username__contains=search)
        friend_results = filter_followed(request.user).filter(username__contains=search)

        people_with_friends_tag = []
        people_with_friends_tag.extend([(result, False) for result in non_friend_results])
        people_with_friends_tag.extend([(result, True) for result in friend_results])

        print(people_with_friends_tag)
        return render(request, 'people.html', {
            'people': sorted(people_with_friends_tag, key=lambda x: x[0].username),
            'form': form
        })

    # Otherwise, the list of current uploader's friends is to be displayed
    friends = [(result, True) for result in filter_followed(request.user)]

    return render(request, 'people.html', {
        'people': sorted(friends, key=lambda x: x[0].username),
        'form': SearchForm()
    })


@require_http_methods(["POST"])
def add_comment(request, photo_id):
    form = CommentForm(request.POST)

    if form.is_valid():

        post = Post.objects.create(text=form.cleaned_data['text'])
        post.save()

        Commented.objects.create(photo=Photo.objects.get(pk=photo_id), post=post, user=request.user).save()

        return HttpResponseRedirect('/' + str(photo_id) + '/comments/')

    return HttpResponseRedirect('/' + str(photo_id) + '/comments/', {'form': form})


@require_http_methods(["GET", "POST"])
def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, new_user)
            return HttpResponseRedirect('/feed/')

        return render(request, 'register.html', {'form': form})
    form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
@require_http_methods(["GET"])
def feed(request):
    photos = Photo.objects.filter(loads__user__in=filter_followed(request.user)).order_by("date")[:20]
    uploaders = [User.objects.filter(loads__photo=photo).first() for photo in photos]
    photos_with_uploaders = list(zip(photos, uploaders))
    photos_with_uploaders_likes = [(photo, uploader, can_user_like(request.user, photo))
                                   for photo, uploader in photos_with_uploaders]

    return render(request, 'feed.html', {'photos': photos_with_uploaders_likes})


@login_required
@require_http_methods(["POST"])
def follow(request, new_friend_id):
    # Self-adding check
    if request.user.id == new_friend_id:
        # FIXME
        return HttpResponseRedirect("/people/")

    # Re-adding check
    if filter_followed(request.user).exists():
        # FIXME
        return HttpResponseRedirect("/people/")

    friends_instance = Followed.objects.create(follower=request.user, followed=User.objects.get(pk=new_friend_id))
    friends_instance.save()

    # FIXME
    return HttpResponseRedirect("/people/")
