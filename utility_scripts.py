import random
from app import db
from app.models import User, Consolation


def create_test_users(user_list):
    for name in user_list:
        mail = "@".join(name.split(' ')) + '.ru'
        # phone = '+7 (910) '+str(random.randint(1111111, 9999999))
        new_user = User(username=name, email=mail)
        if name == 'admin':
            new_user.is_admin = True
        new_user.set_password('password')
        db.session.add(new_user)
    db.session.commit()
    print_db_table(User)


def print_db_table(model):
    for item in model.query.all():
        print(item)


def clear_db_table(model):
    """ удалить все зхаписи в таблице с указанной моделью данных"""
    for record in db.session.query(model).all():
        db.session.delete(record)
    db.session.commit()
    print_db_table(model)


def create_consolations(consolations):
    for item in consolations:
        new_consolation = Consolation()
        new_consolation.text = item['text']
        new_consolation.is_female = item['is_female']
        db.session.add(new_consolation)
    db.session.commit()
    print_db_table(Consolation)


if __name__ == '__main__':
    users = ['admin', ]

    consolations = [{'text': 'Иди, обнму', 'is_female': True},
                    {'text': 'Ты моё солнышко!', 'is_female': True},
                    {'text': 'Оууу, бедный зайка.', 'is_female': True},
                    {'text': 'Скоро скоро, всё пройдёт, моя радость!', 'is_female': True},
                    ]

    # create_consolations(consolations)
    # create_test_users(users)
    print_db_table(User)
