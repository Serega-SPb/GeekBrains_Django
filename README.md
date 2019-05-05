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


