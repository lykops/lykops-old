import time, os, sys, re

from bootstrap_toolkit.widgets import BootstrapUneditableInput
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response, render, get_object_or_404 
from django.template.context import RequestContext
from django.urls.base import reverse
from lykops.settings import BASE_DIR, DEBUG

def login(request):
    from .forms import LoginForm
    # if request.user.is_authenticated():
    #    return HttpResponseRedirect(reverse('index'))
    
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            post_username = request.POST.get('username', '')
            post_password = request.POST.get('password', '')
            
            if post_username and post_password:
                auth_user = auth.authenticate(username=post_username, password=post_password)
                
                if auth_user is not None :
                    if auth_user.is_active:
                        auth.login(request, auth_user)
                        request.session['role_id'] = 0
                        '''
                        if auth_user.role == 'SU':
                            request.session['role_id'] = 2
                        elif auth_user.role == 'GA':
                            request.session['role_id'] = 1
                        else:
                            request.session['role_id'] = 0
                        '''
                        
                        return HttpResponseRedirect(request.session.get('pre_url', reverse('index')))
                    else:
                        error_message = '登陆失败：用户未激活'
                else:
                    error_message = '登陆失败：用户名或密码错误'
            else:
                error_message = '登陆失败：用户名或密码不能为空'
            
        return render(request, 'login.html', {'form': form, 'error_message':error_message})

