from django.db import models
from django.contrib.auth.models import User
from auctions.models import AuctionHistory, ItemImage

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    @property
    def items_images(self):
        try:
            return ItemImage.objects.filter(item__owner=self.user)
        except:
            return None

    @property
    def bids_history(self):
        return AuctionHistory.objects.filter(item__owner=self.user)
    
