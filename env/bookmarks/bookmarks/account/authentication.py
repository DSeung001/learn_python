from account.models import Profile
from django.contrib.auth.models import User

class EamilAuthBackend:
    """
        이메일을 이용한 인증
    """
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

# 새로운 사용자가 생성될 떄 마다 DB에 Profile 객체를 생성
# backend = 소설 인증 백엔드(AUTHENTICATION_BACKENDS에 추가한 것)
# user : 신규 또는 기존 사용자의 User 인스턴스
def create_profile(backend, user, *args, **kwargs):
    """
        Create user profile for social authentication.
    """
    Profile.objects.get_or_create(user=user)