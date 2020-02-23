from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, AdminIndexView, expose
from flask_login import current_user, login_required
from app import db, app

from app.models import User, Gender, Consolation
from flask import abort


class DashboardView(AdminIndexView):
    @expose('/')
    @login_required
    def index(self):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(404)

        return self.render('admin/dashboard.html')


class UserView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    column_exclude_list = ['password_hash']
    column_searchable_list = ['username', 'email']
    column_filters = ['email']


class ConsolationView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    column_labels = dict(text='Текст поддержки', gender='Пол')
    column_sortable_list = ['text', ('gender', 'gender.gender_ru')]
    column_filters = ['text', 'gender']


admin = Admin(app, template_mode='bootstrap3', name='Админка', index_view=DashboardView(name='Статистика'))
admin.add_view(UserView(User, db.session, name='Пользователи'))
admin.add_view(ConsolationView(Consolation, db.session, name='Слова поддержки'))
