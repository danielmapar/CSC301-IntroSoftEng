from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from ChatApp.models import UserProfile, Match
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from ChatApp.models import UserProfile, Match
from django.db.models import Q
from ChatApp.forms import MatchForm, ProfilePicForm

import logging
log = logging.getLogger(__name__)


def index(request):
    return render(request, 'chatapp/login.html', {'anchor': '', 'status': ''})


def signup(request):
    status = ''
    if request.method == 'POST':
        try:
            validate_email(request.POST['email'])
            if User.objects.get(username=request.POST['username']):
                status = {'error': 'Username already used!'}
                return render(request, 'chatapp/login.html', {'anchor': '#', 'signin_status': status,
                                                              'signin_attr': request.POST})
        except ValidationError:
            status = {'error': 'Invalid email!'}
            return render(request, 'chatapp/login.html', {'anchor': '#', 'signin_status': status,
                                                          'signin_attr': request.POST})
        except EmptyFields:
            status = {'error': 'Empty fields!'}
            return render(request, 'chatapp/login.html', {'anchor': '#', 'signin_status': status,
                                                          'signin_attr': request.POST})
        except User.DoesNotExist:
            if request.POST['firstname'] == '' or request.POST['lastname'] == '' or\
               request.POST['password'] == '' or request.POST['password2'] == '' or request.POST['username'] == '':
                status = {'error': 'Empty fields!'}
                return render(request, 'chatapp/login.html', {'anchor': '#', 'signin_status': status,
                                                              'signin_attr': request.POST})
            
            elif request.POST['password'] != "" and request.POST['password'] != request.POST['password2']:
                status = {'error': 'Password confirmation failed!'}
                return render(request, 'chatapp/login.html', {'anchor': '#', 'signin_status': status,
                                                              'signin_attr': request.POST})

            else:
                user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
                user.first_name = request.POST['firstname']
                user.last_name = request.POST['lastname']
                user.is_active = True
                user.save()
                user_profile = UserProfile()
                user_profile.user = user
                user_profile.save()
                new_user = authenticate(username=request.POST['username'],
                                        password=request.POST['password'])
                login(request, new_user)
                return redirect(edit_profile)
    else:
        return render(request, 'chatapp/login.html', {'anchor': '', 'signin_status': status})


def login_user(request):
    status = ''
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            # the password verified for the user
            if user.is_active:
                login(request, user)
                return redirect(profile)
            else:
                status = {'error': 'The password is valid, but the account has been disabled!'}
        else:
            status = {'error': 'The username and password were incorrect.'}
    return render(request, 'chatapp/login.html', {'anchor': '', 'login_status': status})


def logout_user(request):
    logout(request)
    return redirect(login_user)


def profile(request, username=None):
    if request.user and request.user.is_authenticated() and not username:
        profile = UserProfile.objects.get(user=request.user)
        return render(request, 'chatapp/FriendProfile.html', {'user': request.user, 'profile' : profile})
    elif username:
        try:
            user = User.objects.get(username=username)
            profile = UserProfile.objects.get(user=user)
            return render(request, 'chatapp/FriendProfile.html', {'user': user, 'profile' : profile})
        except User.DoesNotExist:
            return redirect(login_user)
    else:
        return redirect(login_user)


def chat(request):
    if request.user and request.user.is_authenticated():
        if request.method == 'GET':
                user = User.objects.get(username=request.user.username)
                user.user_profile = UserProfile.objects.get(user=user)
                return render(request, 'chatapp/chat.html', {'user': user})


def edit_profile(request):
    if request.user and request.user.is_authenticated():
        if request.method == 'GET':
                user = User.objects.get(username=request.user.username)
                user.user_profile = UserProfile.objects.get(user=user)
                return render(request, 'chatapp/Account.html', {'user': user})

        elif request.method == 'POST':
            user = User.objects.get(username=request.user.username)
            user_profile = UserProfile.objects.get(user=user)

            # Edit Profile
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user_profile.age = request.POST['age']
            user_profile.gender = request.POST['gender']
            user_profile.program = request.POST['program']
            user_profile.degree = request.POST['degree']
            user_profile.year_of_study = request.POST['year_of_study']
            user_profile.description = request.POST['description'].strip()

            if 'video_games' in request.POST:
                user_profile.video_games = True
            else:
                user_profile.video_games = False

            if 'books' in request.POST:
                user_profile.books = True
            else:
                user_profile.books = False

            if 'music' in request.POST:
                user_profile.music = True
            else:
                user_profile.music = False

            if 'sports' in request.POST:
                user_profile.sports = True
            else:
                user_profile.sports = False

            user_profile.save()

            user.user_profile = user_profile
            user.save()
            success = {'success': 'Saved!'}
            return render(request, 'chatapp/Account.html', {'user': user,
                                                            'edit_profile': success})
    else:
        return redirect(login_user)


def edit_account(request):

    if request.user and request.user.is_authenticated() and request.method == 'POST':
        # Edit Account
        if request.POST['username'] != "" and request.POST['email'] != "":


            if request.POST['password'] != "" and request.POST['password'] != request.POST['password2']:
                error = {'error': 'Passoword confirmation failed!'}
                request.user.user_profile = UserProfile.objects.get(user=request.user)
                return render(request, 'chatapp/Account.html', {'user': request.user,
                                                                'edit_account': error,
                                                                'anchor': 'true'})


            user = User.objects.get(username=request.user.username)
            user.username = request.POST['username']
            user.email = request.POST['email']
            if request.POST['password'] != "":
                user.set_password(request.POST['password'])
            user.save()
            logout_user(request)
            return redirect(login_user)
        else:
            error = {'error': 'Empty Fields!'}
            request.user.user_profile = UserProfile.objects.get(user=request.user)
            return render(request, 'chatapp/Account.html', {'user': request.user,
                                                            'edit_account': error,
                                                            'anchor': 'true'})
    else:
        return redirect(login_user)


def upload_pic(request):
    log.debug("PPStep 1")
    if request.user and request.user.is_authenticated() and request.method == 'POST':
        log.debug("PPStep 2")
        form = ProfilePicForm(request.POST, request.FILES)
        log.debug("PPStep 3")
        if form.is_valid():
            log.debug("PPStep 4")
            user = User.objects.get(username=request.user.username)
            with open('resources/chatapp/profilepics/' + str(user.id), 'wb+') as destination:
                log.debug("PPStep 5")
                for chunk in request.FILES['pic'].chunks():
                    destination.write(chunk)
            log.debug("PPStep 6")
            return redirect(profile)
        else:
            error = {'error': 'Empty Fields!'}
            return render(request, 'chatapp/Account.html', {'user': request.user,
                                                            'edit_account': error,
                                                            'anchor': 'true'})
    else:
        return redirect(login_user)

def create_match(request):
    if request.method == 'POST':
        form = MatchForm(request.POST)
        form.is_valid()
        usr = UserProfile.objects.get(id=form.cleaned_data['user'])
        myProfile = UserProfile.objects.get(user=request.user)
        match = Match.objects.filter(user1=usr).filter(user2=myProfile)
        oops = Match.objects.filter(user1=myProfile).filter(user2=usr)
        log.debug("Match requested from " + str(myProfile.id) + " to " + str(usr.id))
        if match.exists():
            match = match.get()
            match.accepted = True
            match.save()
        elif oops.exists():
            return redirect(edit_profile)
        else:
            match = myProfile.create_match(usr)
            match.save()

        Match.objects.update()
        return redirect(matches);
    else:
        form = MatchForm()
        return render(request, 'chatapp/viewprofile.html', {'form': form})

def reject_match(request):
    if request.method == 'POST':
        form = MatchForm(request.POST)
        form.is_valid()
        usr = UserProfile.objects.get(id=form.cleaned_data['user'])
        myProfile = UserProfile.objects.get(user=request.user)
        match = Match.objects.filter(user1=usr.id).filter(user2=myProfile.id)

        if match.exists():
            match = match.get()
            match.accepted = False
            match.points = -1
            match.save()
        else:
            match = usr.create_match(myProfile)
            match.points = -1
            match.save()

        return redirect(matches);
    else:
        form = MatchForm()
        return render(request, 'chatapp/viewprofile.html', {'form': form})

def matches(request):
    myProfile = UserProfile.objects.get(user=request.user)
    Match.objects.update()
    matches = Match.objects.filter(Q(user1=myProfile) | Q(user2=myProfile)).filter(accepted=True)
    rejects = Match.objects.filter(user2=myProfile).filter(points=-1)
    pending = Match.objects.filter(user1=myProfile)
    log.debug("Finding matches for "+ str(myProfile.id));
    log.debug("Pending:")
    for e in pending.all():
        log.debug("  match:")
        log.debug("\t->" + str(e.user1.id))
        log.debug("\t->" + str(e.user2.id))
        log.debug("\t->" + str(e.accepted))
    i = 0;
    matchInfo = []
    log.debug("Matches:")
    for e in matches.all():
        if (e.user1 == myProfile):
            temp = e.user2
        else:
            temp = e.user1
        tup = (temp.user,temp)
        log.debug("\t-> With " + str(tup[0].first_name)+ "(" + str(tup[1].id) + ")")
        matchInfo.append(tup)

    if request.user and request.user.is_authenticated():
        requests = Match.objects.filter(user2=myProfile).exclude(points=-1).exclude(accepted=True)
        if requests.exists():
            ret = requests[:1].get()
            log.debug("Requests:")
            for e in requests.all():
                log.debug("Match:")
                log.debug("\t->" + str(e.user1.id))
                log.debug("\t->" + str(e.user2.id))
                log.debug("\t->" + str(e.accepted))
            user = User.objects.get(id=ret.user1.user.id)
            profile = UserProfile.objects.get(id=ret.user1.id)
            return render(request, 'chatapp/viewprofile.html', {'user': user, 'profile' : profile, 'match': ret, 'matches' : matchInfo, 'value' : ret.points})
        else:
            max = -1
            profile = myProfile
            profiles = UserProfile.objects.exclude(id = myProfile.id)[:10]
            for usr in profiles :
                if (usr.id != myProfile.id) :
                    value = myProfile.match_value(usr)
                    isReject = (rejects.filter(user1=usr).exists())
                    premade = matches.filter(user1=usr).exists() or matches.filter(user2=usr).exists() or pending.filter(user2=usr).exists()
                    requested = Match.objects.filter(user1=myProfile).filter(user2=usr).exists()
                    log.debug("(" + str(max) +")checking "+ str(usr.id) + ":");
                    log.debug("\t->Value = "+ str(value));
                    log.debug("\t->isReject = "+str(isReject));
                    log.debug("\t->premade = "+ str(premade));
                    log.debug("\t->requested = "+ str(requested));
                    if (value > max and not isReject and not premade and not requested):
                        max = myProfile.match_value(usr)
                        profile = usr
                        
            user = User.objects.get(id=profile.user.id)
            matchid = user.id;
            myid = request.user.id;
            log.debug("Returning " + str(profile.id) + " for " + str(myProfile.id))
            return render(request, 'chatapp/viewprofile.html', {'user': user, 'profile' : profile, 'matches' : matchInfo, 'value' : max})
    else:
        return redirect(login_user)

def qb(request):
    if request.user and request.user.is_authenticated():
        myProfile = UserProfile.objects.get(user=request.user)
        Match.objects.update()
        matches = Match.objects.filter(Q(user1=myProfile) | Q(user2=myProfile)).filter(accepted=True)
        rejects = Match.objects.filter(user2=myProfile).filter(points=-1)
        pending = Match.objects.filter(user1=myProfile)
        log.debug("Finding matches for "+ str(myProfile.id));
        log.debug("Pending:")
        for e in pending.all():
            log.debug("  match:")
            log.debug("\t->" + str(e.user1.id))
            log.debug("\t->" + str(e.user2.id))
            log.debug("\t->" + str(e.accepted))
        i = 0;
        matchInfo = []
        log.debug("Matches:")
        for e in matches.all():
            if (e.user1 == myProfile):
                temp = e.user2
            else:
                temp = e.user1
            tup = (temp.user,temp)
            log.debug("\t-> With " + str(tup[0].first_name)+ "(" + str(tup[1].id) + ")")
            matchInfo.append(tup)
        return render(request, 'chatapp/qb.html', {'user' : request.user, 'matches' : matchInfo})
    else:
        return redirect(login_user)

class EmptyFields(Exception):
    pass
