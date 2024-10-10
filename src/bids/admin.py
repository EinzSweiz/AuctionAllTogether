from django.contrib import admin
from .models import Bid, AuctionHistory

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ['bidder', 'amount', 'item']