from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from user import views

app_name = 'user'

router = DefaultRouter()
router.register('roles', views.RoleViewSet)

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('logout/', views.BlacklistTokenView.as_view(), name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('me/update/', views.ProfileView.as_view(), name='profile'),
    path('perms/', views.retrieve_all_permissions, name='all_perms'),
    path('perms/<str:model>', views.custom_user_model_permissions, name='model_perms'),
    path('', include(router.urls)),
    path('my-roles/', views.RoleUserListView.as_view(), name='my_roles')
]
