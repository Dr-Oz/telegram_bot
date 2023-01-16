from tg_bot.services.db.sqllite import Database

db = Database()

def test():

    #db.create_table_users() # создаем таблицу пользователей

    #users = db.select_all_users()  # выгружаем в переменную всех наших пользователей
    #print(f'До добавления пользователей: {users}')

    # db.add_user(1, 'One', 'email')
    # db.add_user(2, 'Vasya', 'vv@email.com')
    # db.add_user(3, 'Tree', 1)
    # db.add_user(4, 'Four', 1)
    # db.add_user(5, 'Five', 'email')

    #users = db.select_all_users()   # выгружаем в переменную всех наших пользователей
    #print(f'После добавления пользователей: {users}')
    user = db.select_user(Name='One', id=1)
    print(f'Получил пользователя {user}')

test()