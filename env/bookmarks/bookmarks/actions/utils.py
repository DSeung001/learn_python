import datetime
from django.utils import timezone
from django.contrib.admin import action
from django.contrib.contenttypes.models import ContentType
from .models import Action

def create_action(user, verb, target=None):
    # 마지막 순간에 비슷한 활동이 있는 지 체크
    now = timezone.now()
    last_minute = now - datetime.timedelta(minutes=1)
    # created__gte = grater than or equal 을 의미
    similar_actions = Action.objects.filter(user_id=user.id,
                                            verb=verb,
                                            created__gte=last_minute)

    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(
            target_ct=target_ct,
            target_id=target.id
        )

    if not similar_actions:
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False
