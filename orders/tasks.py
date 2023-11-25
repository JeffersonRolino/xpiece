from django.core.mail import send_mail

from .models import Order


def order_created(order_id):
    """
    Esta é a Tarefa para enviar um e-mail quando
    a ordem de compra for criada com sucesso...
    """
    order = Order.objects.get(id=order_id)
    subject = f'Xpiece - order number {order_id}'
    message = f'Hello {order.first_name},\n' \
              f'You have successfully placed an order.\n' \
              f'Your order ID is {order.id}.'
    mail_sent = send_mail(subject, message, 'admin@xpiece.com', [order.email])

    return mail_sent