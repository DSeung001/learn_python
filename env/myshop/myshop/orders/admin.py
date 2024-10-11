from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid', 'created',
        'updated']
    #  어드민에서 필터링 가능
    list_filter = ['paid', 'created', 'updated']
    # 다른 모델의 데이터를 한꺼번에 표시하고 수정할 수 있게 해주는 기능
    inlines = [OrderItemInline]
