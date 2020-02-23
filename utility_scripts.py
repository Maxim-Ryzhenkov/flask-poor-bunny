import random
from app import db
from app.models import User, Consolation, Gender


def create_admin():
    new_user = User(username='admin', email='admin@admin.ru')
    new_user.is_admin = True
    db.session.add(new_user)
    db.session.commit()
    new_user.set_password('password')
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
        new_consolation.gender = Gender.query.filter(Gender.gender == item['gender']).first()
        db.session.add(new_consolation)
    db.session.commit()
    print_db_table(Consolation)


def create_genders(genders):
    for item in genders:
        new_gender = Gender()
        new_gender.gender = item['gender']
        new_gender.gender_ru = item['gender_ru']
        db.session.add(new_gender)
    db.session.commit()
    print_db_table(Gender)


if __name__ == '__main__':
    users = ['admin', ]

    consolations = [{'text': 'Иди, обнму', 'gender': 'female'},
                    {'text': 'Ты моё солнышко!', 'gender': 'female'},
                    {'text': 'Оууу, бедный зайка.', 'gender': 'female'},
                    {'text': 'Скоро скоро, всё пройдёт, моя радость!', 'gender': 'female'},
                    ]

    genders = [{'gender': 'male', 'gender_ru': 'мужчина'},
               {'gender': 'female', 'gender_ru': 'женщина'},
               {'gender': 'unknown', 'gender_ru': 'неизвестно'}]

    # create_genders(genders)
    # create_consolations(consolations)
    create_admin()
    #clear_db_table(User)