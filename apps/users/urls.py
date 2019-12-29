from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('check-auth/', views.check_auth),
    path('group-permission-save/', views.group_permission_save),
    path('user-group-save/', views.user_group_save),
]