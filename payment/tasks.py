from django.core.mail import send_mail


def send_email_after_payment(order, url):
    """
    Esta é a Tarefa para enviar um e-mail com o link
    para download dos arquivos após o pagamento ser confirmado...
    """
    order = order
    link = url

    subject = f'Xpiece - order number {order.id}'
    message = f'Hello {order.first_name},\n' \
              f'Your payment was approve, access the link below to download your files.\n' \
              f'Download: {link}.'
    mail_sent = send_mail(subject, message, 'admin@xpiece.com', [order.email])

    return mail_sent