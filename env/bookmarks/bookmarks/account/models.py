from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class Profile(models.Model):
    # 코드를 범용적으로 사용하려면 User 모델을 바로 사용하는 것 보단 get_user_model 메서드를 통해 사용하는 게 좋음
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d',blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'

class Contact(models.Model):
    user_from = models.ForeignKey('auth.User',
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)

    # 팔로우되는 사용자에 대한 foreignKey
    user_to = models.ForeignKey('auth.User',
                                related_name='rel_to_set',
                                on_delete=models.CASCADE)

    # 관계가 만들어진 시간을 저장
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
        ]
        ordering = ['-created']

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'


user_model = get_user_model()
# add_to_class로 모델에 필드를 추가하는건 권장하는 방법은 아님
# 그러나 이 경우 메서드를 사용하면 커스텀 모델을 만들지 않고 장고도 기본으로 제공하는 User 모델의 동작이 가능함
# 보통은 profile에 추가하거나, 새로 만드는 걸 권하고 커스텀 모델을 사용하게 나음
# symmetrical=False 속성으로 서로 동기화 되지 않음 => 자동 맞팔되지 않음
user_model.add_to_class('following', models.ManyToManyField(
    'self', related_name='followers', symmetrical=False
))