from django.shortcuts import render
from django.db.models import Q
from .models import Product

def product_list(request):
    q = request.GET.get('q')
    price_min = request.GET.get('min')
    price_max = request.GET.get('max')
    order = request.GET.get('order')  # 'price', '-price', 'name', '-name'

    products = Product.objects.all()

    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))
    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)
    if order in ['price', '-price', 'name', '-name']:
        products = products.order_by(order)

    return render(request, 'store/product_list.html', {
        'products': products,
        'q': q or '',
        'min': price_min or '',
        'max': price_max or '',
        'order': order or '',
    })
