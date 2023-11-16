from django.shortcuts import render

from cart.cart import Cart

from .forms import CreateOrderForm
from .models import OrderItem


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = CreateOrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'])
            cart.clear()
        return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = CreateOrderForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})