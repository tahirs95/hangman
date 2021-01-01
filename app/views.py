import json

from django.shortcuts import render, redirect
from django.contrib.auth.models import User

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


def game_start_2(request):
     return render(request, 'game-start-2.html')

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

def role(request):
    up = UserProfile.objects.filter(user=request.user)[0]
    role = up.role
    return render(request,'role.html',{"role":role})

def add_players(request):
    teacher = UserProfile.objects.filter(user=request.user)[0]
    if request.method == 'POST':
        players = request.POST.getlist('players')
        for player in players:
            student = UserProfile.objects.filter(user__username=player)[0]
            p = Player(student=student, teacher=teacher)
            p.save()
        return redirect('/')
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
        
        return render(request, 'players.html', {'player_names':player_names, 'teacher_players_list':teacher_players_list})

def play(request):
    student = UserProfile.objects.filter(user=request.user)[0]
    player = Player.objects.filter(student=student)
    if player:
        teacher = player[0].teacher.user.username
    else:
        teacher = None
    return render(request,'play.html',{"teacher":teacher})

def game_link(request, *args, **kwargs):
    teacher_uname = kwargs['teacher']
    teacher = UserProfile.objects.filter(user__username=teacher_uname)[0]
    g = Game.objects.filter(teacher=teacher)
    words = json.loads(g[0].words)
    return render(request,'game_link.html',{"words":words})

