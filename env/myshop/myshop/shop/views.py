from linecache import cache

from cart.forms import CartAddProductForm
from django.shortcuts import render, get_object_or_404
from unicodedata import category
from django.contrib.sessions.models import Session
from .models import Category, Product


# Create your views here.
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    sessions = Session.objects.all()
    session_data_list = []
    for session in sessions:
        session_data = session.get_decoded()  # 세션 데이터를 디코딩
        session_data_list.append({
            'session_key': session.session_key,  # 세션 키
            'session_data': session_data  # 디코딩된 세션 데이터
        })

    return render(request,
                  'shop/product/list.html',
                  {
                      'category': category,
                      'categories': categories,
                      'products': products,
                      'session_data_list': session_data_list,
                  })


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', {'product': product, 'cart_product_form': cart_product_form})
