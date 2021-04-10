from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .Forms import UserAdminCreationForm, AuthenticationForm, IdeaForm
from .models import MyUser, Idea
from django.contrib.auth.decorators import login_required
from .ideabot import stackfind

@login_required
def ideas(request):
    return render(request, 'ideas.html')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'home.html', {'form': AuthenticationForm()})
    else:
        try:
            user = authenticate(request, email=request.POST['email'], password=request.POST['password'])
            if user is None:
                return render(request, 'home.html',
                            {'form': AuthenticationForm(), 'error': 'User password did not match'})
            else:
                login(request, user)
                return redirect('ideas')
        except:
            # Create a new user
            if request.POST['password1'] == request.POST['password2']:
                try:
                    user = MyUser.objects.create_user(password=request.POST['password1'], email=request.POST['email'], mob=request.POST['mob'])
                    user.save()
                    login(request, user)
                    return redirect('ideas')
                except IntegrityError:
                    return render(request, 'home.html',
                                {'error': 'This email id has already been registered. Please try to login or use different email id'})
                except ValueError:
                    return render(request, 'home.html',
                                {'error': 'Please enter valid email'})
            else:
                # tell the user the password didn't match
                return render(request, 'home.html', {'error': 'Passwords did not match'})

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('loginuser')

@login_required
def ideas(request):
    details = Idea.objects.filter(user=request.user)
    for detail in details:
        print(type(detail.description))
        detail.stack=stackfind(detail.description)
        print(detail.stack)
    return render(request, 'ideas.html', {'details':details})

@login_required
def submitidea(request):
    if request.method == 'GET':
        return render(request, 'submitidea.html', {'form': IdeaForm()})
    else:
        try:
            form = IdeaForm(request.POST)
            newidea = form.save(commit=False)
            newidea.user = request.user
            newidea.save()
            return redirect('ideas')
        except ValueError:
            return render(request, 'submitidea.html',
                          {'form': IdeaForm(), 'error': 'Wrong data put in. Try Again'})

@login_required
def viewprofile(request):
    pass
