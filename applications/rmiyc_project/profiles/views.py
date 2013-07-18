# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from ifind.models import game_models
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

def profile_page(request, username):
    context = RequestContext(request, {})
    u = User.objects.get(username=username)
    if u:
        user_profile = u.get_profile()
    if request.user == u:
        level = user_profile.level
        xp = user_profile.xp
        view_permission = True
        return render_to_response('profiles/profile_page.html', {'user_profile': u,
                                                                 'profile': user_profile,
                                                                 'level':level,
                                                                 'view_perm': view_permission,
                                                                 'xp':xp}, context)
    else:
        view_permission = False
        return render_to_response('profiles/profile_page.html', {'user_profile': u,
                                                                 'view_perm': view_permission,
                                                                 'profile': user_profile},
                                                                  context)
