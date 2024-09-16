from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    # post 뷰
    path('',views.post_list,name='post_list'),
    # https://docs.djangoproject.com/en/4.1/topics/http/urls/ => 이제 사실 5버전을 쓰긴함
    path('<int:id>/',views.post_detail,name='post_detail'),
]