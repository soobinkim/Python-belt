from django.shortcuts import render, redirect
from .models import User, UserManager
from django.db.models import Count
from django.contrib import messages
import bcrypt
# Create your views here.
def index(request):
    # User.objects.all().delete()
    return render(request, 'blackbelt/index.html')

def process(request):
    if request.POST['button'] == 'register':
        register = request.POST
        user = User.objects.register(register)
        if user[0] == False:
            for error in user[1]:
                messages.warning(request, error)
            return redirect('/')
        context = {
            'user': user[1]
        }
        return render(request, 'blackbelt/success.html', context)
    if request.POST['button'] == 'login':
        user = User.objects.login(request.POST)
        # if isinstance(user, list):
        if user[0] == False:
            for error in user[1]:
                messages.warning(request, error)
            return redirect('/')
        else:
            request.session['id'] = user[1].id
            return redirect('/success')

            # messages.message

def success(request):
    if request.session.get('id') == None:
        return redirect('/')
    return render(request, 'blackbelt/success.html')
# post quotes on the wall
def post(request, post_id):
    user = User.objects.get(id = request.session['id'])
    if request.POST['button'] == 'message':
        Quotes.objects.create(message = request.POST['message'], user = user)
    elif request.POST['button'] == 'favorite':
        user.objects.favorited_post(request.session['id'], post_id)
    else:
        Quotes.objects.favorited_post(request.session['id'], post_id)
        return redirect('/favorited_quotes')
    return redirect('/success')

def delete(request,id):
    Quotes.objects.get(id = id).delete()
    context = {
        'user': User.objects.get(id = request.session['id']),
        'messages': messages.objects.all(),
    }
    if request.POST['button']=='delete2':
        return redirect('/favorited_quotes')
    return redirect('/success')

def logout(request):
    request.session.pop('id')
    return redirect('/')

def favorited_quotes(request):
    context = {
        'quotes': User.objects.annotate(numlike = Count('favorites')).order_by('-numlike'),
        'user': User.objects.get(id = request.session['id']),
    }
    return render(request, 'blackbelt/favorited_quotes.html', context)

# def logout(request):
