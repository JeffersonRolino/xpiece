from decimal import Decimal

import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render, reverse

from orders.models import Order

from .tasks import send_email_after_payment

# Instanciando stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def payment_process(request):
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        success_url = request.build_absolute_uri(reverse('payment:completed', kwargs={'id':order.id, 'token':order.token}))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled', kwargs={'id':order.id}))
        # Criando dados de checkout para o Stripe
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }
        # Adicionando os items da ordem na sessão de checkout do Stripe
        for item in order.items.all():
            session_data['line_items'].append({
                'price_data': {
                    # O pagamento do Stripe é em centavos, por isso a multiplicação por 100
                    'unit_amount': int(item.price * Decimal('100')),
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product.name,
                    },
                },
                'quantity': int(1),
            })

        # Criando a sessão de checkout para o Stripe usando os dados
        session = stripe.checkout.Session.create(**session_data)
        # Redirecionando para formulário de pagamento do Stripe
        return redirect(session.url, code=303)

    else:
        return render(request, 'payment/process.html', locals())

@login_required
def payment_completed(request, id, token):
    order = get_object_or_404(Order, id=id)
    order.generate_url(request)
    url = request.build_absolute_uri(reverse('payment:completed', kwargs={'id':order.id, 'token':order.token}))
    send_email_after_payment(order, url)
    context = {'order': order}
    return render(request, 'payment/completed.html', context)


def payment_canceled(request, id):
    order = get_object_or_404(Order, id=id)
    context = {'order': order}
    return render(request, 'payment/canceled.html', context)
