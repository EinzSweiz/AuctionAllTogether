from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.urls import reverse

class Status(models.TextChoices):
    ON_SALE = 'on sale', 'On Sale'
    FINISHED = 'finished', 'Finished'
class Item(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at =  models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.ON_SALE)

    def clean(self):
        if self.starting_price <= 0:
            raise ValidationError('Starting price must be greater than zero.')
        if self.end_date <= timezone.now():
            raise ValidationError('End date must be in the future.')

    def is_auction_active(self):
        return self.status == Status.ON_SALE and self.end_date > timezone.now()
    
    def __str__(self):
        return self.title
    
    def end_auction(self):
        self.status = Status.FINISHED
        self.save()
    

    @property
    def actual_price(self):
        return f'{self.starting_price}'
    
    def get_absolute_url(self):
        return reverse('auctions:item_detail', kwargs={'pk': self.pk})
    
        

class ItemImage(models.Model):
    item = models.ForeignKey(Item, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='items_image/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_prefix(self):
        return f'projects/{self.id}/'
