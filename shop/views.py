from django.shortcuts import get_object_or_404, render

from cart.forms import CartAddProductForm

from .models import Category, Format, Product, Screenshot


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(published=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'product/list.html', {'category': category,
                                                 'categories': categories,
                                                 'products': products})


def product_detail(request, id, slug):
    categories = Category.objects.all()
    product = get_object_or_404(Product, id=id, slug=slug)
    formats = Format.objects.filter(product__id=str(id))
    screenshots = Screenshot.objects.filter(product__id=str(id))
    cart_add_product = CartAddProductForm()

    return render(request, 'product/detail.html', {'product': product,
                                                   'formats': formats,
                                                   'categories': categories,
                                                   'screenshots': screenshots,
                                                   'cart_add_product': cart_add_product})


def about(request):
    categories = Category.objects.all()
    return render(request, 'about.html', {'categories': categories})


def contact(request):
    categories = Category.objects.all()
    return render(request, 'contact.html', {'categories': categories})
