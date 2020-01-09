from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from django.db import IntegrityError, transaction
from django.contrib.auth.models import update_last_login, Group, Permission
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from services.common.logging import log_err
from .models import User
from .serializers import UserSerializer, GroupSerializer, PermissionSerializer


@api_view(['POST'])
def check_auth(request):
    # Проверка аутентификации пользователя
    if request.method == 'POST':
        user = User.objects.get(account=request.user.account)
        user_ser = UserSerializer(user)
        _groups = Group.objects.all()
        _permissions = get_permissions_with_exclude()
        groups_ser = GroupSerializer(_groups, many=True)
        permissions_ser = PermissionSerializer(_permissions, many=True)
        staff_condition = None if request.user.is_staff else True
        users = User.objects.all().exclude(is_staff=staff_condition)
        users_ser = UserSerializer(users, many=True)
        return JsonResponse({
            'user': user_ser.data,
            'users': users_ser.data,
            'info': {
                'groups': groups_ser.data,
                'permissions': permissions_ser.data
            }
        }, safe=False)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        refresh = self.get_token(user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['account'] = user.account
        update_last_login(None, user)
        return data

    def create(self, validated_data):
        return

    def update(self, instance, validated_data):
        return


# Кастомизируем данные, которые отправляются клиенту при входе в систему
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(viewsets.ViewSet):
    permission_classes = [permissions.DjangoModelPermissions]
    queryset = User.objects.none()

    # Выбрать всех пользователей
    def list(self, request):
        staff_condition = None if request.user.is_staff else True
        users = User.objects.all().exclude(is_staff=staff_condition)
        users_ser = UserSerializer(users, many=True)
        return JsonResponse({
            'users': users_ser.data
        }, safe=False)

    # Создать/обновить пользователя
    @action(detail=False, methods=['post', 'put'], url_path='save')
    @transaction.atomic
    def save(self, request):
        user_req = request.data.get('user')
        try:
            with transaction.atomic():
                if request.method == 'POST':  # create
                    serializer = UserSerializer(data=user_req)
                if request.method == 'PUT':  # update
                    print(1, )
                    user = User.objects.get(id=user_req['id'])
                    serializer = UserSerializer(user, data=user_req)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return JsonResponse({
                    'user': serializer.data
                }, safe=False)
        except IntegrityError as err:
            log_err(err)
            return JsonResponse({}, status=500)


class GroupViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Group.objects.none()

    # Выбрать все группы и разрешения
    @action(detail=False, methods=['get'], url_path='groups-permissions-list')
    def groups_permissions_list(self, request):
        groups = Group.objects.all()
        permissions = get_permissions_with_exclude()
        groups_ser = GroupSerializer(groups, many=True)
        permissions_ser = PermissionSerializer(permissions, many=True)
        auth_info = {
            'groups': groups_ser.data,
            'permissions': permissions_ser.data
        }
        return JsonResponse({
            'info': auth_info
        }, safe=False)

    # Создать/обновить группу
    @action(detail=False, methods=['post', 'put'], url_path='group-save')
    @transaction.atomic
    def group_save(self, request):
        group_req = request.data.get('group')
        try:
            with transaction.atomic():
                if request.method == 'POST':  # create
                    serializer = GroupSerializer(data=group_req)
                if request.method == 'PUT':  # update
                    group = Group.objects.get(id=group_req['id'])
                    serializer = GroupSerializer(group, data=group_req)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return JsonResponse({
                    'group': serializer.data
                }, safe=False)
        except IntegrityError as err:
            log_err(err)
            return JsonResponse({}, status=500)


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def group_permission_save(request):
    # Добавить/удалить разрешение у группы
    if request.method == 'POST':
        group_id = request.data.get('group_id')
        permission_id = request.data.get('permission_id')
        is_checked = request.data.get('is_checked')
        group = Group.objects.get(id=group_id)
        permission = Permission.objects.get(id=permission_id)
        group.permissions.add(permission) if is_checked else group.permissions.remove(permission)
    return JsonResponse({}, safe=False)


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def user_group_save(request):
    # Добавить пользователя в группу, удалить из группы
    if request.method == 'POST':
        user_id = request.data.get('user_id')
        group_id = request.data.get('group_id')
        is_checked = request.data.get('is_checked')
        user = User.objects.get(id=user_id)
        group = Group.objects.get(id=group_id)
        user.groups.add(group) if is_checked else user.groups.remove(group)
        return JsonResponse({}, safe=False)


def get_permissions_with_exclude():
    return Permission.objects.all() \
            .exclude(
        content_type__model__in=['logentry', 'permission','group',
                                 'contenttype', 'session'])