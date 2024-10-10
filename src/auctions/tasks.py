import random
from celery import shared_task
from django.core.mail import send_mail
from .models import Item
import logging


logger = logging.getLogger(__name__)

def get_item_details(item_id):
    try:
        return Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        logger.error(f"Item with ID {item_id} not found for email notification.")
        return None



@shared_task(name="send_item_created_email")
def send_item_created_email(item_id):
    item = get_item_details(item_id)
    subject = 'Item Created'
    message = (
        f'Congratulations! Your item "{item.title}" has been created successfully.\n'
        f'Starting price: {item.actual_price}\n'
        f'Description: {item.description}\n'
        f'You can view your item here: {item.get_absolute_url()}'
    )
    recipient_list = [item.owner.email]
    send_mail(subject, message, 'riad.sultanov.1999@example.com', recipient_list)


@shared_task(name="send_item_updated_email")
def send_item_updated_email(item_id, site_domain, owner_email):
    item = get_item_details(item_id)
    if item is None:
        logger.error(f"Item with ID {item_id} not found for email notification.")
        return None

    subject = 'Item Updated'
    message = (
        f'Congratulations! Your item "{item.title}" has been updated successfully.\n'
        f'Starting price: {item.actual_price}\n'
        f'Description: {item.description}\n'
        f'You can view your item here: http://{site_domain}{item.get_absolute_url()}'
    )
    
    recipient_list = [owner_email]
    send_mail(subject, message, 'riad.sultanov.1999@example.com', recipient_list)


@shared_task(name='send_delete_confirmation_email')
def send_delete_confirmation_email(item_id, confirm_url):
    try:
        item = get_item_details(item_id)
        subject = f"Confirm Deletion of {item.title}"
        message = f"Please click the link below to confirm the deletion of your item:\n{confirm_url}"
        from_email = 'riad.sultanov.1999@gmail.com'
        recipient_list = [item.owner.email]
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        print(f"Failed to send email for item {item_id}: {str(e)}")


# @shared_task(name="sum_list_numbers")
# def xsum(numbers):
#     # Celery recognizes this as the `sum_list_numbers` task
#     return sum(numbers)