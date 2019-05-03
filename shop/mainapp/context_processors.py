
def get_main_menu(request):
    return {'menu_items': [
        {'name': 'Главная', 'link': 'index'},
        {'name': 'Каталог', 'link': 'catalog:index', 'namespace': 'catalog'},
        {'name': 'Контакты', 'link': 'contacts'},
        {'name': 'Admin', 'link': 'admin_custom:index'}
    ]}
