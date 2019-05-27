# GeekBrains_Django
=======
# GeekBrains_Django Part 2

## Homework 1
Все сделано

Примечание:
- ключи активации юзеров вынес в отдельную модель UserActivation 
  (после активации ключ удаляется)
- из ссылки для активации юзера убрал email
- контекстный процессор сделал для меню в шапке сайта
  (информация о корзине юзера сделано через template tag)
  
## Homework 2
Fixes:
- UserActivation: default expired_to исправил
- UsersCreateView: исправил ошибку при создании юзера (из-за этого пользователь django криво записался в бд)

Сделано пункты 1-4

Примечание:
- сделал загрузку аватарки юзера из профиля google в media/users_avatars/\<username>_avatar.jpg

## Homework 3
Все сделано

## Homework 4
Все сделано

## Homework 7
- @cached_property не нашел где применить чтобы получить прирост производительности
(прописал в ShopCart.get_all_cached, Order.get_total_quantity и Order.get_total_cost)
- тег "with" уже давно используется в шапке сайта (состояние корзины) в комбинации с шаблонным тегом
- сделал метод get_products() с кешированием
- изменил шаблон страницы каталога, чтобы можно было загружать контент через ajax
- написал скрипт для отправки/приема ajax и подставки стилей к выбраной категории
