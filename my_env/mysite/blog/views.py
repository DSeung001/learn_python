from re import search

from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.views.generic import ListView
from taggit.models import Tag

from .form import EmailPostForm, CommentForm, SearchForm
from .models import Post, Comment


def post_detail(request, year, month, day, post):
    # try:
    #     post = Post.objects.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404("Post does not exist")
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # 이 글의 active 댓글 목록
    comments = post.comments.filter(active=True)
    # 사용자가 댓글을 달 수 있는 댓글 인스턴스도 전달
    form = CommentForm()
    # 유사한 게시물들의 목록
    post_tags_ids = post.tags.values_list('id', flat=True)
    # tag 기능 api도 있음 : https://django-taggit.readthedocs.io/en/latest/api.html
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags')[:4]
    return render(request, 'blog/post/detail.html',
                  {
                      'post': post,
                      'comments': comments,
                      'form': form,
                      'similar_posts': similar_posts,
                  })


# Create your views here.
#  함수 기반 list 방식
def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        # 페이지 번호가 범위를 넘어간 경우
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts, 'tag': tag}
                  )


# Class 기반 list 방식
# class PostListView(ListView):
#     """
#     Alternative post list view
#     """
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 5
#     template_name = 'blog/post/list.html'


def post_share(request, post_id):
    # id로 조회
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # 유효성 검사 체크
            cd = form.cleaned_data
            #  전송
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}'s comments: {cd['comments']}"
            send_mail(subject, message, 'seungryeol156@gmail.com', [cd['name']])
            sent = True
    else:
        form = EmailPostForm()

    #  form이 유효하지 않으면 다시 템플릿 랜더링
    return render(request, 'blog/post/share.html', {
        'post': post,
        'form': form,
        'sent': sent
    })


# 데코레이터를 이용하여 post만 허용
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # 댓글이 달림
    form = CommentForm(request.POST)
    if form.is_valid():
        # Db에 저잗하지 않고 객체만 생성
        comment = form.save(commit=False)
        # 댓글에 게시물 할당
        comment.post = post
        # DB에 저장, save 메서드는 ModelForm에는 사용할 수 있지만 Form 인스턴스는 연결된 모델이 없으므로 사용못함
        comment.save()
    return render(request, 'blog/post/comment.html',
                  {
                      'post': post,
                      'form': form,
                      'comment': comment
                  })


# postgresql vector 검색을 이용
def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            # config='spanish로 언어를 바꿔서 형태소를 분석하고 불용어를 제거할 수 있음
            # 아래 처럼 가중치를 줄 수 있음 A:1,B:0.4,C:0.2,D:0.1을 의미함
            # 형태소 분석을 통한 검색
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A') + \
                            SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            results = Post.published.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(search=query)

            # 트라이그램 유사성을 이용한 검색
            # => 형변환 에러 뜨면서 안되는데 이유 못찾음, 근데 그렇게 중요하진 않으니까 패스
            # query = str(form.cleaned_data['query'])
            # results = Post.published.annotate(
            #     similarity=TrigramSimilarity('title', query)
            # ).filter(similarity__gt=0.1).order_by('-similarity')

    return render(request,
                  'blog/post/search.html',
                  {'form': form, 'query': query, 'results': results})
