from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from .form import EmailPostForm, CommentForm
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
    return render(request, 'blog/post/detail.html',
                  {
                      'post': post,
                      'comments': comments,
                      'form': form,
                  })


# Create your views here.
#  함수 기반 list 방식
# def post_list(request):
#     posts = Post.published.all()
#     paginator = Paginator(posts, 3)
#     page_number = request.GET.get('page', 1)
#     try:
#         posts = paginator.page(page_number)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         # 페이지 번호가 범위를 넘어간 경우
#         posts = paginator.page(paginator.num_pages)
#     return render(request,
#                   'blog/post/list.html',
#                   {'posts': posts}
#                   )

# Class 기반 list 방식
class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 5
    template_name = 'blog/post/list.html'


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
