from django.apps import AppConfig


class ImagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'images'
    # images 애플리케이션이 로드될 때 임포트되도록 ready 메서드에서 이 애플리케이션의 시그널을 가져옴
    def ready(self):
        import images.signals
