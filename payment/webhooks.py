import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from orders.models import Order


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    # Verificando a Assinatura do Stripe no Header da Requisição
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        # Contruíndo o evento do webhook
        event = stripe.Webhook.construct_event(payload, signature_header, settings.STRIPE_WEBHOOK_SECRET)
    except ValueError as error:
        # Caso o payload seja inválido
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as SignatureError:
        # Caso a assinatura secreta seja inválida
        return HttpResponse(status=400)

    # Checar se a sessão de checkout foi completada com sucesso
    if event.type == 'checkout.session.completed':
        # Recuperar Dados da Sessão
        session = event.data.object
        if session.mode == 'payment' and session.payment_status == 'paid':
            try:
                order = Order.objects.get(id=session.client_reference_id)
            except Order.DoesNotExist:
                return HttpResponse(status=404)
            order.paid = True
            order.save()
    
    return HttpResponse(status=200)
