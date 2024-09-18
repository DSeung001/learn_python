from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Profile(models.Model):
    # 코드를 범용적으로 사용하려면 User 모델을 바로 사용하는 것 보단 get_user_model 메서드를 통해 사용하는 게 좋음
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d',blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'