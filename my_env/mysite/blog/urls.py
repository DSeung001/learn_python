from django.urls import path
from . import views

app_name = 'blog'

# https://docs.djangoproject.com/en/4.1/topics/http/urls/ => 이제 사실 5버전을 쓰긴함
urlpatterns = [
    # post 뷰
    # path('',views.post_list,name='post_list'),
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_detail,name='post_detail'),
    path('<int:post_id>/share/',views.post_share, name='post_share'),
    path('<int:post_id>/comment/',views.post_comment,name='post_comment'),
]