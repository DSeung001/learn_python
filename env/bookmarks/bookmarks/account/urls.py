from django.contrib.auth.decorators import login_required
from django.urls import include

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # 이전 로그인
    # path('login/', views.user_login, name='login'),
    # test
    # path('index/', views.index, name='index'),

    # 로그인 / 로그아웃
    # 장고에서 제공하는 클래스 기반 뷰
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    #  -------------------------------------------

    # #  패스워드 url 변경
    # path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    # path('password-change/done', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    #
    # # 패스워드 재설정 url
    # path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # 위 로직은 아래와 동일

    path('',include('django.contrib.auth.urls')),
    # 대시보드
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
]
