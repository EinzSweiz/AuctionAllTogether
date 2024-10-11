from django.db import models
from django.shortcuts import get_object_or_404
from auctions.models import Item
from django.contrib.auth.models import User
from django.urls import reverse

class Bid(models.Model):
    item =  models.ForeignKey(Item, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('item', 'bidder')

    def get_absolute_url(self):
        return reverse('bids:add_bid', kwargs={'item_id': self.item.id})
    
    @classmethod
    def get_last_bid(cls, item):
        return cls.objects.filter(item=item).order_by('-created_at').first()


   
class AuctionHistory(models.Model):
    item = models.ForeignKey(Item, related_name='auction_history', on_delete=models.CASCADE)
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.bid.amount} on {self.item.title} at {self.timestamp} by {self.user.username}'