from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    # 게시글의 변경 빈도와 사이트에서의 관련성
    changefreq = 'weekly'
    priority = 0.9

    # 이 사이트 맵에 포함할 객체
    def items(self):
        return Post.published.all()

    # 반환된 각 객체를 받아서 객체가 마지막으로 수정된 날짜를 반환
    def lastmod(self, obj):
        return obj.updated
