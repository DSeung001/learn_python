from django.contrib import admin
from .models import Post, Comment


# Register your models here.

# @는 데코라이트 함수로, 함수에 앞 뒤에 기능을 더해줌, 약간 js의 콜백함수 느낌
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    # 검색 바
    search_fields = ['title', 'body']
    # 자동 슬러그 추가
    prepopulated_fields = {"slug": ("title",)}
    # Author 선택 필드
    raw_id_fields = ['author']
    # 날짜 정렬 추가
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name','email','body']