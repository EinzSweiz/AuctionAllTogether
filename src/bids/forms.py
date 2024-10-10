from django import forms
from .models import Bid
from django.core.exceptions import ValidationError


class BidCreateForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']

    
    def __init__(self, *args, **kwargs):
        self.item = kwargs.pop('item', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        amount = self.cleaned_data.get('amount')

        if amount <= 0:
            raise ValidationError('Bid amount must be greater than zero.')
       
        highest_bid = self.item.bid_set.order_by('-amount').first() 

        if highest_bid and amount < highest_bid.amount:
            raise ValidationError('Bid amount must be greater than the highest bid.')
        if amount < self.item.starting_price:
            raise ValidationError('Bid amount must be at least the starting price.')
        
        return self.cleaned_data
