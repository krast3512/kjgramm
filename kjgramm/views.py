from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from kjgramm.forms import SearchForm, PhotoModelForm
from kjgramm.models import Friends, Loads, Photo, Liked, Commented, Post


def filter_friends(user):
    return (User.objects.filter(first_id__second_id=user.id) | User.objects.filter(
        second_id__first_id=user.id)).exclude(pk=user.pk)


def exclude_friends_self(user):
    return User.objects.exclude(first_id__second_id=user.id).exclude(second_id__first_id=user.id).exclude(pk=user.pk)


@require_http_methods(["POST"])
def upload_file(request, path, document_root):
    if request.method == "POST":
        form = PhotoModelForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            new_photo = form.save(commit=False)

            new_photo.file = request.FILES["file"]
            new_photo.save()

        return HttpResponseRedirect("/feed/")
    form = PhotoModelForm()
    return HttpResponseRedirect("/feed/", {'form': form})


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
    return render(request, 'comments.html', {
        'photo': Photo.objects.get(photo_id),
        'comments_on_photo': comments_on_photo
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

        non_friend_results = exclude_friends_self(request.user).filter(username__contains=search)
        friend_results = filter_friends(request.user).filter(username__contains=search)

        people_with_friends_tag = []
        people_with_friends_tag.extend([(result, False) for result in non_friend_results])
        people_with_friends_tag.extend([(result, True) for result in friend_results])

        print(people_with_friends_tag)
        return render(request, 'people.html', {
            'people': sorted(people_with_friends_tag, key=lambda x: x[0].username),
            'form': form
        })

    # Otherwise, the list of current user's friends is to be displayed
    friends = [(result, True) for result in filter_friends(request.user)]

    return render(request, 'people.html', {
        'people': sorted(friends, key=lambda x: x[0].username),
        'form': SearchForm()
    })


@require_http_methods(["POST"])
def add_comment(request, photo_id):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if not form.is_valid():
            return HttpResponseRedirect()
        new_text = form.cleand_data['text']
        post = Post.objects.create(text=new_text)
        post.save()
        Commented.objects.create(photo_id=photo_id, post_id=post.id, user_id=request.user.id).save()
        return HttpResponseRedirect('/' + str(photo_id) + '/comments/')
    form = SearchForm()
    return render(request, '/' + str(photo_id) + '/comments/', {'form': form})


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

    photos = sorted(photos, key=lambda entry: Photo.objects.get(entry[0]).date)[:20]

    liked_photos = [liked_entry.photo_id for liked_entry in Liked.objects.all()
                    if liked_entry.user_id == request.user.id]
    photos = [(Photo.objects.get(photo_id), User.objects.get(user_id), photo_id not in liked_photos)
              for photo_id, user_id in photos]

    return render(request, 'feed.html', {'photos': photos})


@login_required
@require_http_methods(["POST"])
def add_to_friends(request, new_friend_id):
    # Self-adding check
    if request.user.id == new_friend_id:
        # FIXME
        return HttpResponseRedirect("/people/")

    # Re-adding check
    if filter_friends(request.user).exists():
        # FIXME
        return HttpResponseRedirect("/people/")

    friends_instance = Friends.objects.create(first_id=request.user, second_id=User.objects.get(pk=new_friend_id))
    friends_instance.save()

    # FIXME
    return HttpResponseRedirect("/people/")
