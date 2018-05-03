from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *



def index(request):
    return render(request, "pythonexam/index.html")

def register(request):
    check = User.objects.register(
        request.POST["name"],
        request.POST["username"],
        request.POST["dob"],
        request.POST["email"],
        request.POST["password"],
        request.POST["confirm"],
        
    )

    if not check["valid"]:
        for error in check["errors"]:
            messages.add_message(request, messages.ERROR, error)
            return redirect("/")
    else:
        request.session["user_id"] = check["user"].id
        messages.add_message(request, messages.SUCCESS, "Thank you for registering, {}".format(request.POST["username"]))
        return redirect("/")

def login(request):
    check = User.objects.login(
        request.POST["username"],
        request.POST["password"]
    )

    if not check["valid"]:
        for error in check["errors"]:
            messages.add_message(request, messages.ERROR, error)
        return redirect("/")
    else:
        if "user_id" not in request.session:
            request.session["user_id"] = check["username"].id
        messages.add_message(request, messages.SUCCESS, "Welcome back, {}".format(check["username"]))
        return redirect("/dashboard")



def dashboard(request):
    if "user_id" not in request.session:
        messages.add_message(request, messages.ERROR, "You need to log in first")
        return redirect("/")
        print request.session['user_id']
    user = User.objects.filter(id=request.session['user_id']).first()
    users = User.objects.all()
    friends_from = User.friend.through.objects.filter(from_user_id=request.session['user_id'])
    friends_to = User.friend.through.objects.filter(to_user_id=request.session['user_id'])
    not_friends_from = User.friend.through.objects.exclude(from_user_id=request.session['user_id'])
    friends = []
    not_friends = []
    for friend_row in friends_from:
        friends.append(User.objects.get(id=friend_row.to_user_id))
    for friend_row in friends_to:
        friends.append(User.objects.get(id=friend_row.from_user_id))

    print "flag"
    for user in users:
        if not user in friends and user.id != request.session["user_id"]:
            not_friends.append(user)
    print not_friends
    data = {
        'user':user.name,
        'users':users,
        'friends':friends,
        'friends_from':friends_from,
        'friends_to':friends_to,
        # 'friends':friend_objs,
        'not_friends':not_friends,
    }


    return render(request, "pythonexam/dashboard.html", data)


def logout(request):
    request.session.clear()
    messages.add_message(request, messages.SUCCESS, "K thanks. Bai")
    return redirect("/")

def add_friend(request, id):

	user = User.objects.get(id=request.session['user_id'])
	friend = User.objects.get(id=id)

	user.friends.add(friend)

	return redirect('/dashboard')

def del_friend(request, id):
    deletion_1 = User.friend.through.objects.filter(from_user_id=request.session['user_id']).filter(to_user_id=id)
    deletion_2 = User.friend.through.objects.filter(to_user_id=request.session['user_id']).filter(from_user_id=id)
    print deletion_1
    print deletion_2
    if len(deletion_1):
        deletion_1.first().delete()
    elif len(deletion_2):
        deletion_2.first().delete()

	return redirect('/dashboard')

def view_user(request, id):
    
	user =  User.objects.get(id = id)
	context = {
		'user': user,		
	}
	return render(request, 'pythonexam/user.html', context)