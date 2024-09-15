from django.utils import timezone

from django.db import models


# Create your models here.
class Post(models.Model):
    # db 에서는 varchar
    title = models.CharField(max_length=250)
    # slug = 워드프레스의 slug와 같음, db 에서는 varchar
    slug = models.SlugField(max_length=250)
    # db 에서는 TextField
    body = models.TextField()
    # db 에선 datetime
    publish = models.DateTimeField(default=timezone.now)
    # auto_now_add 추가 될 때만
    created = models.DateTimeField(auto_now_add=True)
    # auto_now 추가 및, 수정
    updated = models.DateTimeField(auto_now=True)

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
