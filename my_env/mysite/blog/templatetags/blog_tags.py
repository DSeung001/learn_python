from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

from ..models import Post

register = template.Library()

# 장고는 함수 이름을 태그명으로 사용
# 다른 명을 사용하고 싶으면 파라미터로 전달
@register.simple_tag
def total_posts():
    return Post.objects.count()

# inclusion tag는 지정된 템플릿을 렌더링 하기 위한 콘텍스트로서 사용될 값을 반환하는데 사용
# 즉 템플릿과 사용되는 태그 코드
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))