from django.conf.urls import url
from django.contrib.auth import views
from django.urls import path

from accounts.views import Profile, register_superuser
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', register_superuser, name='register'),
    # url(r'^otp/$', OTPLoginView.as_view(), name='otp'),
    # # url(r'^accounts/login/$', views.LoginView.as_view(authentication_form=OTPAuthenticationForm), name='login'),
    #
    url(r'logout/', views.LogoutView.as_view(), name='logout'),
    #
    path('profile/', Profile.as_view(), name='profile'),
    # url(r'^me/$', ProfileView.as_view(), name='me'),
    #
    # url(r'^password_change/$', views.PasswordChangeView.as_view(), name='password_change'),
    # url(r'^password_change/done/$', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    #
    # url(r'^password_reset/$', views.PasswordResetView.as_view(), name='password_reset'),
    # url(r'^password_reset/done/$', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # url(r'^reset/done/$', views.PasswordResetCompleteView.as_view(), name='password_reset_complete')
]
