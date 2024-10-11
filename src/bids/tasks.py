from celery import shared_task
from django.core.mail import send_mail
from .models import Bid
from auctions.models import Item

@shared_task
def send_rebid_notification(bid_id):
    try:
        bid = Bid.objects.get(id=bid_id)
        subject = 'New Bid on Your Item'
        message = f"{bid.bidder.username} has placed a new bid of ${bid.amount} on your item: {bid.item.title}."
        recipient_list = [bid.item.owner.email]
        send_mail(subject, message, 'noreply@yourdomain.com', recipient_list)
    except Bid.DoesNotExist:
        pass