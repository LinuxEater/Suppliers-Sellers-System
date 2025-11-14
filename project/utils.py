from django.core.mail import send_mail
from django.conf import settings

def send_low_stock_notification(product):
    """
    Sends an email notification for low stock.
    """
    subject = f'Alerta de Estoque Baixo: {product.name}'
    message = (
        f'O produto "{product.name}" (Código: {product.product_code}) está com estoque baixo.\n'
        f'Estoque atual: {product.stock}\n'
        f'Por favor, reponha o estoque.'
    )
    recipient_list = [settings.ADMIN_EMAIL]
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
