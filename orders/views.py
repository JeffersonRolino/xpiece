from django.shortcuts import redirect, render
from django.urls import reverse

from cart.cart import Cart

from .forms import CreateOrderForm
from .models import OrderItem
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