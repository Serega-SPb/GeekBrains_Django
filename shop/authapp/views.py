from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

from .forms import *
from .models import *


def login(request):
    login_form = ShopUserLoginForm(data=request.POST)
    next = request.GET['next'] if 'next' in request.GET.keys() else ''
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('index'))
    context = {
        'login_form': login_form,
        'next': next
    }
    return render(request, 'authapp/login.html', context=context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            if not register_form.instance.avatar:
                register_form.instance.avatar = ''
            user = register_form.save()
            if send_verify_mail(user):
                status = 'сообщение подтверждения отправлено'
            else:
                status = 'ошибка отправки сообщения'
            print(status)
            return render(request, 'authapp/activation.html', context={'status': status})
    else:
        register_form = ShopUserRegisterForm()
    context = {'register_form': register_form}
    return render(request, 'authapp/register.html', context)


@login_required
def edit(request):
    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:view'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)

    context = {
        'edit_form': edit_form,
        'is_edit': 'True',
    }
    return render(request, 'authapp/profile.html', context=context)


@login_required
def view(request):
    context = {'is_edit': 'False'}
    return render(request, 'authapp/profile.html', context=context)


def send_verify_mail(user):
    code = user.code.code
    verify_link = reverse('auth:verify', args=[code])

    title = f'Подтверждение учетной записи {user.username}'
    message = f'Для подтверждения учетной записи {user.username} на портале \
{settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, activation_key):
    try:
        user_activation: UserActivation = UserActivation.objects.get(code=activation_key)
        if user_activation and user_activation.code_is_valid():
            user = user_activation.user
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            user_activation.delete()
            status = 'Successful'
        else:
            status = 'Failure'
            print(f'error activation by key: {activation_key}')
    except Exception as e:
        status = 'Error'
        print(f'error activation user : {e.args}')

    return render(request, 'authapp/verification.html', context={'status': status})
