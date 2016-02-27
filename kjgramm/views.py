from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from kjgramm.models import Friends, Loads, Photo, Liked, Commented, Post
from django import forms


class TextForm(forms.Form):
    text = forms.CharField(max_length=50)


@require_http_methods(["GET"])
def add_photo(request):
    return
#VOVA DELAET


@require_http_methods(["POST"])
def like(request, photo_id):
    like_repeated = False
    for likes in Liked.objects.all():
        if likes.user_id == request.user.id and likes.photo_id == photo_id:
            like_repeated = True
            break
    if not like_repeated:
        photo_obj = Photo.objects.get(photo_id)
        photo_obj.likes_num += 1
        Liked.objects.create(user_id=request.user.id, photo_id=photo_id).save()
    return HttpResponseRedirect(request.POST.get('next'))


@require_http_methods(["GET"])
def comments(request, photo_id):
    comments_on_photo = []
    post_data = []
    for commented_instance in Commented.objects.all():
        if commented_instance.photo_id == photo_id:
            post_data.append((commented_instance.post_id, commented_instance.user_id))
    for post_id, user_id in post_data:
        comments_on_photo.append((Post.objects.get(post_id), User.objects.get(user_id)))
    return render(request, 'templates/comments.html', {'photo': Photo.objects.get(photo_id),
                                                       'comments_on_photo': comments_on_photo})


@require_http_methods(["GET"])
def people_search(request):
    form = TextForm(request.GET)
    if not form.is_valid():
        return render(request, 'templates/people.html', {'people':[], 'form': form})
    search = form.cleand_data['search']
    people_with_friends = []
    for user in User.objects.all():
        if search in user.login:
            people_with_friends.append((user, False))
    for friend in Friends.objects.all():
        for i, (man, _) in enumerate(people_with_friends):
            if friend.first_id == man.login or friend.second_id == man.login:
                people_with_friends[i] = (man, True)
    return render(request, 'templates/people.html', {'people': people_with_friends.sort(key=lambda x:x[0].login)})


@require_http_methods(["POST"])
def add_comment(request, photo_id):
    form = TextForm(request.POST)
    if not form.is_valid():
        return HttpResponseRedirect()
    new_text = form.cleand_data['text']
    post = Post.objects.create(text=new_text)
    post.save()
    Commented.objects.create(photo_id=photo_id, post_id=post.id, user_id=request.user.id).save()
    return HttpResponseRedirect('/' + str(photo_id) + '/comments/')


@require_http_methods(["GET", "POST"])
def register_user(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        login(request, new_user)
        return HttpResponseRedirect('/feed/')
    return render(request, 'templates/register.html', {'form': form})


@require_http_methods(["GET"])
def feed(request):
    photos = []
    friends_ids = []
    for friend in Friends.objects.all():
        if friend.first_id == request.user.id:
            friends_ids.append(friend.second_id)
        elif friend.second_id == request.user.id:
            friends_ids.append(friend.first_id)
    for load in Loads.objects.all():
        if load.user_id in friends_ids:
            photos.append((load.photo_id, load.user_id))

    photos = photos.sort(key=lambda entry: Photo.objects.get(entry[0]).date)[:20]

    liked_photos = [liked_entry.photo_id for liked_entry in Liked.objects.all()
                    if liked_entry.user_id == request.user.id]
    photos = [(Photo.objects.get(photo_id), User.objects.get(user_id), photo_id not in liked_photos)
              for photo_id, user_id in photos]

    return render(request, 'templates/feed.html', {'photos': photos})
