from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy

from cart.cart import Cart

from .forms import CreateOrderForm
from .models import Order, OrderItem
from .tasks import order_created


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = CreateOrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'])
            cart.clear()
            # Envia email para cliente após ordem de compra criada
            order_created(order.id)
            # Adiciona ordem na sessão do cliente
            request.session['order_id'] = order.id
            # Redireciona para pagamento
            return redirect(reverse('payment:process'))
    else:
        form = CreateOrderForm()
        return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})

def order_items_download(request, id):
    order = get_object_or_404(Order, id=id)
    context = {'order': order}
    return render(request, 'orders/order/download.html', context)

def redirect_me(request, id):
    return redirect(reverse_lazy('orders:order_download', kwargs={'id':id}))