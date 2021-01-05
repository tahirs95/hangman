import json
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import  UserForm, ProfileForm
from .models import  UserProfile, Game, Player

# Create your views here.

def home(request):
    return render(request, "home.html")

def signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            password = user_form["password"].value()
            username = user_form["username"].value()
            role = profile_form["role"].value().lower()
            u = User.objects.get(username=username)
            u.set_password(password)
            u.save()
            up = UserProfile(role=role, user=u)
            up.save()
            # profile_form.save()
            return redirect('/')
        else:
            pass
            # messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'authentication/signup.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def game_2(request):
     return render(request, 'game-2.html')

def graph_2(request):
     return render(request, 'graph-2.html')

@login_required(login_url="/login")
def graph(request):
     return render(request, 'graph-link.html')

def game_start_2(request):
     return render(request, 'game-start-2.html')

@login_required(login_url="/login")
def game(request):
    if request.method == 'POST':
        words = request.POST.get('words')
        teacher = UserProfile.objects.filter(user=request.user)[0]
        game = Game.objects.filter(teacher=teacher)
        if game:
            game = game[0]
            game.words = words
            game.save()
        else:
            game = Game(teacher=teacher, words=words)
            game.save()
        return redirect('/role')
    else:
        up = UserProfile.objects.filter(user=request.user)[0]
        game = Game.objects.filter(teacher=up)
        if game:
            words = json.loads(game[0].words)
        else:
            words = {}
        return render(request, 'game.html', {"words":words})

@login_required(login_url="/login")
def role(request):
    up = UserProfile.objects.filter(user=request.user)[0]
    if request.method == 'POST':
        status = request.POST.get('status')
        up.status = status
        up.save()

    d1 = request.user.date_joined
    timezone = request.user.date_joined.tzinfo
    d2 = datetime.now(timezone)
    joining_days = abs((d2 - d1).days)

    if joining_days >= 30:
        status = True
        up.status = status
        up.save()
        print("True")
    else:
        status = False
        up.status = status
        up.save()
        print("False")

    teachers = []
    up = UserProfile.objects.filter(user=request.user)[0]
    role = up.role

    if role == "student":
        student = UserProfile.objects.filter(user=request.user)[0]
        players = Player.objects.filter(student=student)
        if players:
            for p in players:
                teachers.append(p.teacher.user.username)
    return render(request,'role.html',{"role":role, "teachers":list(set(teachers)), "status":status})

@login_required(login_url="/login")
def add_players(request):
    teacher = UserProfile.objects.filter(user=request.user)[0]
    if request.method == 'POST':
        Player.objects.filter(teacher=teacher).delete()
        players = request.POST.getlist('players')
        for player in players:
            student = UserProfile.objects.filter(user__username=player)[0]
            p = Player(student=student, teacher=teacher)
            p.save()
        return redirect('/role')
    else:
        teacher_players_list = []
        teacher_players = Player.objects.filter(teacher=teacher)
        if teacher_players:
            for p in teacher_players:
                teacher_players_list.append(p.student.user.username)
        
        players = UserProfile.objects.filter(role='student')
        player_names = []
        for p in players:
            player_names.append(p.user.username)
        
        print(teacher_players_list)
        return render(request, 'players.html', {'player_names':player_names, 'teacher_players_list':list(set(teacher_players_list))})

@login_required(login_url="/login")
def game_link(request, *args, **kwargs):
    teacher_uname = kwargs['teacher']
    teacher = UserProfile.objects.filter(user__username=teacher_uname)[0]
    g = Game.objects.filter(teacher=teacher)
    words = json.loads(g[0].words)
    return render(request,'game_link.html',{"words":words})

