# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from ifind.models.game_models import HighScore, PlayerAchievement, UserProfile
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import os
from django.forms import ModelForm
from forms import *
from configuration import MEDIA_URL
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.urlresolvers import reverse




def profile_page(request, username):
    murl = MEDIA_URL
    context = RequestContext(request, {})
    u = User.objects.get(username=username)
    if u:
        user_profile = u.get_profile()
    if request.user == u:
        level = user_profile.level
        xp = user_profile.xp
        achievements = PlayerAchievement.objects.filter(user=u)
        for i in achievements:
            print MEDIA_URL + str(i.achievement.badge_icon)
            print i.achievement.badge_icon
        highscores = HighScore.objects.filter(user=u)
        view_permission = True
        return render_to_response('profiles/profile_page.html', {'user_profile': u,
                                                                 'profile': user_profile,
                                                                 'level':level,
                                                                 'murl': murl,
                                                                 'age':user_profile.age,
                                                                 'achievements': achievements,
                                                                 'view_perm': view_permission,
                                                                 'highscores': highscores,
                                                                 'xp':xp}, context)
    else:
        view_permission = False
        return render_to_response('profiles/profile_page.html', {'user_profile': u,
                                                                 'view_perm': view_permission,
                                                                 'profile': user_profile},
                                                                  context)
@login_required
def edit_profile(request, username):
    #if usr1 tries accessing usr2 profile edit page, redirect to usr1 edit page
    if username != request.user.username:
        return redirect('/profile/%s/edit_profile' % request.user.username)
    context = RequestContext(request, {})
    usr = User.objects.get(username=request.user.username)
    profile = UserProfile.objects.get(user=usr)
    profile_form = ProfileForm(instance=profile)
    user_form = UserForm(instance=usr)

    if request.method == 'GET':
        return render_to_response('profiles/edit_profile.html', {'profile_form': profile_form,
                                                                 'user_form': user_form},context)
    else:
        profile_form = ProfileForm(request.POST)
        user_form = UserForm(request.POST)
        if profile_form.is_valid() and user_form.is_valid():
            profile.age = profile_form.cleaned_data['age']
            profile.gender = profile_form.cleaned_data['gender']
            profile.school = profile_form.cleaned_data['school']
            profile.country = profile_form.cleaned_data['country']
            profile.city = profile_form.cleaned_data['city']
            profile.save()
            usr.first_name = user_form.cleaned_data['first_name']
            usr.last_name = user_form.cleaned_data['last_name']
            usr.email = user_form.cleaned_data['email']
            usr.save()
        else:
            return render_to_response('profiles/edit_profile.html', {'profile_form': profile_form,
                                                                     'user_form': user_form},context)
        return HttpResponseRedirect(reverse('profile', args=(usr.username,)))





