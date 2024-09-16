from django.contrib.auth.models import User
from django.utils import timezone

from django.db import models


# QuerySet 수정
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


# Create your models here.
class Post(models.Model):

    # 중첩 클래스로, 논리적 그룹화 + 캡슐화 강화 + 모듈성 유지를 얻음
    # 선택을 위한 하위 클래스로 열거형을 제공해줌
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    # db 에서는 varchar
    title = models.CharField(max_length=250)
    # slug = 워드프레스의 slug와 같음, db 에서는 varchar
    slug = models.SlugField(max_length=250)
    # 다대일 연결
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    # db 에서는 TextField
    body = models.TextField()
    # db 에선 datetime
    publish = models.DateTimeField(default=timezone.now)
    # auto_now_add 추가 될 때만
    created = models.DateTimeField(auto_now_add=True)
    # auto_now 추가 및, 수정
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    # 기본 관리자
    objects = models.Manager()
    # 커스텀 관리자
    published = PublishedManager()

    # 부가 정보
    class Meta:
        # 기본 정렬 방법 '-'으로 내림차
        ordering = ['-publish']
        # index
        indexes = [
            # '-'으로 인덱스 정렬을 내림차로 하는데, mysql에선 기본이 내림차고 적용이 안됨
            models.Index(fields=['-publish']),
        ]

        #  문자열로

    def __str__(self):
        return self.title


