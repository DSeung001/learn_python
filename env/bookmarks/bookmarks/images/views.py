from urllib.request import Request
from venv import create

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import ImageCreateForm
from django.shortcuts import get_object_or_404
from .models import Image
from actions.utils import create_action

import redis
from django.conf import settings

# 레디스 연결
r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


# Create your views here.
@login_required
def image_create(request):
    if request.method == 'POST':
        # 폼이 수신됨
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # 폼 데이터가 유효하다면, 이미지를 저장해서 인스턴스만 가져옴
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            # 항목에 현재 사용자들 할당
            new_image.user = request.user
            new_image.save()
            create_action(request.user, 'bookmarked image', new_image)
            messages.success(request, 'Image successfully created')
            return redirect(new_image.get_absolute_url())
    else:
        # GET을 통해 북마클릿에서 제공한 데이터로 폼을 빌드
        form = ImageCreateForm(data=request.GET)
    return render(request,
                  'image/create.html',
                  {
                      'section': 'images',
                      'form': form
                  })


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    # 이미지 조회수 1증가
    total_views = r.incr(f'image:{image.id}:views')
    # 이미지 순위가 1씩 증가, image:ranking 키를 가진 정렬된 셋에 이미지 조회수 를 저장함
    r.zincrby('image_ranking', 1 , image.id)
    return render(request, 'image/detail.html',
                  {'section': 'images', 'image': image, 'total_views': total_views})


@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'liked image', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Image.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 3)
    page = request.GET.get('page')
    images_only = request.GET.get('images_only')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if images_only:
            # ajax 요청이 페이지를 벗어난 경우
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)
    if images_only:
        return render(request, 'image/list_images.html', {'section': 'images', 'images': images})
    return render(request, 'image/list.html', {'section': 'images', 'images': images})


@login_required
def image_ranking(request):
    # 이미지 순위 딕션너리 가져오기, 순위 내림차로 10개만
    image_ranking = r.zrange('image_ranking', 0, -1,desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    # 가장 많이 조회된 이미지 가져오기
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x:image_ranking_ids.index(x.id))
    return render(request,
                  'image/ranking.html',
                  {
                      'section': 'images',
                      'most_viewed': most_viewed,
                  })