from django import forms
from .models import Image
from django.core.files.base import ContentFile
from django.utils.text import slugify
import requests

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'url', 'description']
        widgets = {
            'url' : forms.HiddenInput,
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError("This is not a valid image")
        return url

    # save를 재정의 하는 것보단 일반적인 방법
    def save(self, force_insert=False, force_update=False, commit=True):
        # commit이 False이면 모델 인스턴스를 반환하지만 DB에는 저장하지 않음
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        # 원본 이름을 슬러그화해서 사용
        name = slugify(image.title)
        extension = image_url.rsplit('.',1)[1].lower()
        image_name = f'{name}.{extension}'
        # 주어진 URL에서 이미지를 다운로드
        response = requests.get(image_url)
        # 프로젝트의 미디어 디렉터리에 저장, 객체를 DB에 저장하지 않도록 save=False
        image.image.save(image_name,
                         ContentFile(response.content),
                         save=False)

        if commit:
            # commit이 True인 경우 진짜로 저장
            image.save()
        return image

