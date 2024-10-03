from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.
class Action(models.Model):
    user = models.ForeignKey('auth.User',
                             related_name='actions',
                             on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    # ContentType 모델을 가리키는 ForeignKey 필드 => 실제 모델을 가리킴
    target_ct = models.ForeignKey(ContentType, blank=True, null=True,
                                  related_name='target_obj', on_delete=models.CASCADE)
    # 장고 기본 키 생성과 일치하는 필드
    target_id = models.PositiveIntegerField(null=True, blank=True)
    # 이 전 두 필드의 조합 기반으로 관계된 객체를 가리키는 필드
    target = GenericForeignKey('target_ct', 'target_id')

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['target_ct','target_id']),
        ]
        ordering = ['-created']
