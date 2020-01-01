"""
Добавление первоначальных данных для админ. панели.
Запускается после выполнения всех миграций и fixtures
"""
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from apps.users.models import User
from django.db.models import Q


# Добавить разрешения к группам
def seed_group_permissions(group_m, permission_m, user_m, q):
    def get_all_group_permission(_q):
        return (_q(codename__contains="add_") | _q(codename__contains="change_") |
                _q(codename__contains="delete_") | _q(codename__contains="view_"))
    for group in group_m.objects.all():
        if group.id == user_m.MANAGER:  # разрешения для менеджера
            for permission in permission_m.objects.filter(codename__contains="view_"):
                group.permissions.add(permission)
        if group.id == user_m.OPERATOR:  # разрешения для оператора
            for permission in permission_m.objects.filter(q(codename__contains="change_") |
                                                          q(codename__contains="view_")):
                group.permissions.add(permission)
        if group.id == user_m.CHIEF_OPERATOR:  # разрешения для главного оператора
            for permission in permission_m.objects.filter(get_all_group_permission(q)):
                group.permissions.add(permission)
        if group.id == user_m.IT_DEVELOPER:  # разрешения для IT разработчика/владельца
            for permission in permission_m.objects.filter(get_all_group_permission(q)):
                group.permissions.add(permission)
    print("Разрешения успешно добавлены!")


# init
seed_group_permissions(Group, Permission, User, Q)
