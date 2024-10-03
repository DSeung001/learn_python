from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse


# Create your models here.
class Image(models.Model):
    # 이미지는 한 사용자에게 종속
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='images_created',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    # unique는 인덱스 생성을 의미하기도 함
    slug = models.SlugField(max_length=200, unique=True)
    url = models.URLField(max_length=2000)
    image =  models.ImageField(upload_to='images/%Y/%m/%d')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True)
    # 다대다 관계로 좋아요를 누른 게시물 표시
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       related_name='images_liked',
                                       blank=True)
    total_likes = models.PositiveIntegerField(default=0)
    class Meta:
        # 생성일 내림차 순
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['-total_likes']),
        ]
        ordering = ['-created']

    def __str__(self):
        return self.title

    def create_unique_slug(self, new_slug=None):
        slug = slugify(new_slug) if new_slug else slugify(self.title)
        unique_slug = slug
        counter = 1
        while Image.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, counter)
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.create_unique_slug(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        if not self.slug:
            # 기본 슬러그 설정 또는 적절한 처리
            return reverse('images:detail', args=[self.id, 'default-slug'])
        return reverse('images:detail', args=[self.id, self.slug])

