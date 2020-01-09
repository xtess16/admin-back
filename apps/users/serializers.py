from rest_framework import serializers
from django.contrib.auth.models import Group, Permission

from utils.convert_data import get_account_by_email
from .models import User


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'content_type_id', 'codename']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']

    def create(self, validated_data):
        group = Group.objects.create(**validated_data)
        return group

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'is_staff',
            'is_active',
            'last_login',
            'password_is_generate',
            'remember_me',
            'created_at',
            'updated_at',
            'groups'
        ]
        read_only_fields = ['id', 'account', 'last_login', 'created_at', 'updated_at']

    def create(self, validated_data):
        user = User(
            account=get_account_by_email(validated_data['email']),
            **validated_data
        )
        # TODO Пароль генерируем авто-ки и далее отправляем аккаунт, пароль(и другую инфу) на почту пользователя
        user.set_password('1234')
        user.save()
        return user

    def update(self, instance, validated_data):
        print(2, validated_data)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.password_is_generate = validated_data.get('password_is_generate', instance.password_is_generate)
        instance.remember_me = validated_data.get('remember_me', instance.remember_me)
        if instance.is_superuser is not True:
            instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance
