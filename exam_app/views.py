from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,('index.html'))

def dashboard(request):
    if 'id' not in request.session:
        return redirect('/')
    user=User.objects.get(id=request.session['id'])
    context = {
        'user_logged_in': User.objects.get(id=request.session['id']),
        'all_not_granted': user.wishes.filter(granted=False).order_by("-created_at"),
        'all_granted': Wish.objects.filter(granted=True),
    }
    return render (request,('wishes.html'), context)

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        hash_browns = bcrypt.hashpw(
        password.encode(), # pw to hash
        bcrypt.gensalt() # generated salt bae
        ).decode()  # create the hash
        user=User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=hash_browns,
        )
        request.session['id']=user.id
        return redirect('/wishes')

def logout(request):
    request.session.flush()
    return redirect('/')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['id'] = user.id
        return redirect('/wishes')
# ////////////////////////////////////////////////////////////////

def create(request):
    errors = Wish.objects.wish_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wishes/new')
    else:
        Wish.objects.create(
            wish_item=request.POST['wish_item'],
            description=request.POST['description'],
            wished_by=User.objects.get(id=request.session['id'])
        )
        return redirect('/wishes')

def view_create(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user_logged_in': User.objects.get(id=request.session['id'])
        }
        return render(request, ('create.html'), context)

def view_edit(request, wish_id):
    if 'id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user_logged_in': User.objects.get(id=request.session['id']),
            'edited_wish': Wish.objects.get(id=wish_id)
        }
        return render(request, ('edit.html'), context)

def update(request, wish_id):
    errors = Wish.objects.wish_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/edit/{wish_id}')
    else:
        edit=Wish.objects.get(id=wish_id)
        edit.wish_item=request.POST['wish_item']
        edit.description=request.POST['description']
        edit.save()
        return redirect('/wishes')

def remove(request, wish_id):
    delete=Wish.objects.get(id=wish_id)
    delete.delete()
    return redirect('/wishes')

def granted(request, wish_id):
    granted= Wish.objects.get(id=wish_id)
    granted.granted=True
    granted.save()
    return redirect('/wishes')

def like(request, wish_id):
    wish = Wish.objects.get(id=wish_id)
    user = User.objects.get(id=request.session['id'])
    user.likes.add(wish)
    return redirect('/wishes')

def unlike(request, wish_id):
    wish = Wish.objects.get(id=wish_id)
    user = User.objects.get(id=request.session['id'])
    user.likes.remove(wish)
    return redirect('/wishes')

def view_status(request):
    user=User.objects.get(id=request.session['id'])
    context={
        'this_user_status': User.objects.get(id=request.session['id']),
        'all_granted': Wish.objects.filter(granted=True),
        'this_user_granted': user.wishes.filter(granted=True),
        'this_user_not_granted':user.wishes.filter(granted=False),
    }
    return render(request, ('status.html'), context)