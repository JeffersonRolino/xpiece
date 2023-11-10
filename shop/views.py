from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(published=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'shop/product/list.html', {'category': category,
                                                      'categories': categories,
                                                      'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    return render(request, 'shop/product/product_detail.html', {'product': product})
