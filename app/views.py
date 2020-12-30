from django.shortcuts import render, redirect
from .forms import  UserForm, ProfileForm
from .models import  UserProfile, Game, Player
from django.contrib.auth.models import User

# Create your views here.


def home(request):
    return render(request, "home.html")

def signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            
            username = user_form["username"].value()
            role = profile_form["role"].value().lower()
            u = User.objects.get(username=username)
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


def game(request):
    if request.method == 'POST':
        words = request.POST.get('words')
        teacher = UserProfile.objects.filter(user=request.user)[0]
        game = Game(teacher=teacher, words=words)
        game.save()
        return redirect('/')
    else:
        return render(request, 'game.html')

def add_players(request):
    if request.method == 'POST':
        players = request.POST.get('players').split(',')
        teacher = UserProfile.objects.filter(user=request.user)[0]
        for player in players:
            student = UserProfile.objects.filter(user__username=player)[0]
            p = Player(student=student, teacher=teacher)
            p.save()
        return redirect('/')
    else:
        players = UserProfile.objects.filter(role='student')
        player_names = []
        for p in players:
            player_names.append(p.user.username)
        print(player_names)
        return render(request, 'players.html', {'player_names':player_names})