from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import *
from django.contrib import auth
from django.urls import reverse
from shopcartapp.models import ShopCart
# Create your views here.


def base():
    return {'menu_items': [
        {'name': 'Главная', 'link': 'index'},
        {'name': 'Каталог', 'link': 'catalog:index', 'namespace': 'catalog'},
        {'name': 'Контакты', 'link': 'contacts'},
    ]}


def user_product_count(user):
    return {'products_count': ShopCart.objects.filter(user=user).count()}


def login(request):
    login_form = ShopUserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('index'))

    context = base()
    context['login_form'] = login_form
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
            auth.login(request, user)
            return HttpResponseRedirect(reverse('index'))
    else:
        register_form = ShopUserRegisterForm()
    context = base()
    context['register_form'] = register_form
    return render(request, 'authapp/register.html', context)


def edit(request):
    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:view'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)

    context = base()
    if request.user and request.user.is_active:
        context.update(user_product_count(request.user))
    context['edit_form'] = edit_form
    context['is_edit'] = 'True'
    return render(request, 'authapp/profile.html', context=context)


def view(request):
    context = base()
    if request.user and request.user.is_active:
        context.update(user_product_count(request.user))
    context['is_edit'] = 'False'
    return render(request, 'authapp/profile.html', context=context)
