import simplejwt as simplejwt
from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import ObtainTokenPairWithColorView, CustomUserCreate, MainView, LogoutAndBlacklistRefreshTokenForUserView, \
    ActivationView, LoginView, ManageProfileView  # ,TestView
from .views import ResetPassword,ChangePassword
urlpatterns = [
    path('user/create/', CustomUserCreate.as_view(), name="create_user"),
    path('token/obtain/', ObtainTokenPairWithColorView.as_view(), name='token_create'),
    #path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),  # override sjwt stock token
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('main/', MainView.as_view(), name='main'),
    path('manage_profile/', ManageProfileView.as_view(), name='manage_profile'),
    path('blacklist/', LogoutAndBlacklistRefreshTokenForUserView.as_view(), name='blacklist'),
    path('activate/<uidb64>/<token>',ActivationView.as_view(), name='activate'),
    path('/', LoginView.as_view(), name="login"),
    path('resetpassword/', ResetPassword.as_view(), name='resetpassword'),
    path('changepassword/', ChangePassword.as_view(), name='changepassword'),

    #path('test/',TestView.as_view(), name='test'),
]