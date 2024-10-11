from django import forms

PRODUCT_QUNTITIY_CHOICES = [(i,str(i)) for i in range(1,21)]

class CartAddProductForm(forms.Form):
    # 수량 고를 수 있게
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUNTITIY_CHOICES,
        coerce=int,
    )
    # 수량 오버라이드 여부
    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput,
    )