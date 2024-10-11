import os
from celery import Celery

#  celery 프로그램에 대한 기본 장고 설정 모듈을 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')
#  인스턴스화
app = Celery('myshop')
# 커스텀 구성을 로드, 네임스페이스를 설정하여 모든 설정 앞에 접두어로 CELERY_를 붙임
app.config_from_object('django.conf:settings', namespace='CELERY')
# 비동기 작업을 자동으로 검색하도록 비동기 작업을 지시
app.autodiscover_tasks()