from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin

from authapp.models import ShopUser
from mainapp.models import Product, Serial

MENU_ITEMS = [
    {'name': 'Main', 'link': 'admin_custom:index', 'namespace': 'index'},
    {'name': 'Users', 'link': 'admin_custom:read_user', 'namespace': 'user'},
    {'name': 'Products', 'link': 'admin_custom:read_product', 'namespace': 'product'},
    {'name': 'Serials', 'link': 'admin_custom:read_serial', 'namespace': 'serial'},
]

LINKS = [
    {'name': 'Users', 'namespace': 'user',
        'view': 'admin_custom:read_user',
        'create': 'admin_custom:create_user',
        'update': 'admin_custom:update_user',
        'delete': 'admin_custom:delete_user'},
    {'name': 'Products',  'namespace': 'product',
        'view': 'admin_custom:read_product',
        'create': 'admin_custom:create_product',
        'update': 'admin_custom:update_product',
        'delete': 'admin_custom:delete_product'},
    {'name': 'Serials', 'namespace': 'serial',
        'view': 'admin_custom:read_serial',
        'create': 'admin_custom:create_serial',
        'update': 'admin_custom:update_serial',
        'delete': 'admin_custom:delete_serial'},
]

MODELS = {
    'user': ShopUser,
    'product': Product,
    'serial': Serial
}


def activation_objects(request):

    ns = request.GET.get('ns')
    id = request.GET.get('id')

    entity = MODELS[ns].objects.filter(id=id).first()
    if entity and hasattr(entity, 'is_active'):
        entity.is_active = not entity.is_active
        entity.save()

    link = [x['view'] for x in LINKS if x['namespace'] == ns]
    if link:
        link = link[0]
        return HttpResponseRedirect(reverse(link))


class SUBaseView(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_items'] = MENU_ITEMS
        cur_link = self.request.resolver_match.view_name
        if 'create_' in cur_link:
            context['subject'] = [x['namespace'] for x in LINKS if x['create'] == cur_link][0]
        if 'read_' in cur_link:
            self.read_context(context, cur_link)
        return context

    def read_context(self, context, cur_link):
        item = [x for x in LINKS if x['view'] == cur_link]
        if item:
            item = item[0]
        context['menu_name'] = item['name']
        context['namespace'] = item['namespace']
        context['create_link'] = item['create']
        context['update_link'] = item['update']
        context['delete_link'] = item['delete']


class BaseDeleteView(DeleteView):

    def post(self, request, *args, **kwargs):
        answer = request.POST.get('answer')
        if not answer:
            return HttpResponseNotFound()
        subject = self.model.objects.filter(id=kwargs['pk']).first()

        if answer == 'Yes':
            subject.delete()

        cur_link = self.request.resolver_match.view_name
        redirect = [x for x in LINKS if x['delete'] == cur_link][0]['view']
        return HttpResponseRedirect(reverse(redirect))


class IndexView(SUBaseView, TemplateView):
    template_name = 'adminapp/index.html'

# ----------------Users----------------


class UsersCreateView(SUBaseView, CreateView):
    model = ShopUser
    template_name = 'adminapp/create_page.html'
    fields = ['username', 'email', 'password', 'age']
    success_url = reverse_lazy('admin_custom:read_user')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        return super(UsersCreateView, self).form_valid(form)


class UsersReadView(SUBaseView, ListView):
    model = ShopUser
    template_name = 'adminapp/read_page.html'


class UsersUpdateView(SUBaseView, UpdateView):
    model = ShopUser
    template_name = 'adminapp/update_page.html'
    fields = ['username', 'email', 'avatar', 'age']
    success_url = reverse_lazy('admin_custom:read_user')


class UsersDeleteView(SUBaseView, BaseDeleteView):
    model = ShopUser
    template_name = 'adminapp/delete_page.html'

# ----------------Products----------------


class ProductsCreateView(SUBaseView, CreateView):
    model = Product
    template_name = 'adminapp/create_page.html'
    fields = ['name', 'image', 'price', 'release', 'properties']
    success_url = reverse_lazy('admin_custom:read_product')


class ProductsReadView(SUBaseView, ListView):
    model = Product
    template_name = 'adminapp/read_page.html'


class ProductsUpdateView(SUBaseView, UpdateView):
    model = Product
    template_name = 'adminapp/update_page.html'
    fields = ['name', 'image', 'price', 'release', 'properties']
    success_url = reverse_lazy('admin_custom:read_product')


class ProductsDeleteView(SUBaseView, BaseDeleteView):
    model = Product
    template_name = 'adminapp/delete_page.html'

# ----------------Serials----------------


class SerialsCreateView(SUBaseView, CreateView):
    model = Serial
    template_name = 'adminapp/create_page.html'
    fields = ['name']
    success_url = reverse_lazy('admin_custom:read_serial')


class SerialsReadView(SUBaseView, ListView):
    model = Serial
    template_name = 'adminapp/read_page.html'


class SerialsUpdateView(SUBaseView, UpdateView):
    model = Serial
    template_name = 'adminapp/update_page.html'
    fields = ['name']
    success_url = reverse_lazy('admin_custom:read_serial')


class SerialsDeleteView(SUBaseView, BaseDeleteView):
    model = Serial
    template_name = 'adminapp/delete_page.html'

