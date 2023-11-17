from django.urls import path
from .views import user_login, dashbord_user, user_register, RegistrationView, update_user, UpdateUser, admin_page_view
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', dashbord_user, name="user_profile"),
    path('password-change/', PasswordChangeView.as_view(), name="password_change"),
    path('password-change-done/', PasswordChangeDoneView.as_view(), name="password_change_done"),
    path('password-reset/', PasswordResetView.as_view(), name="password_reset"),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('signup/', user_register, name="register"),
    path('profile/update/', UpdateUser.as_view(), name="update_user"),
    path('admin_page/', admin_page_view, name="admin_page")
]
