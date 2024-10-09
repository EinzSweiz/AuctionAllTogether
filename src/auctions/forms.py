from django import forms
from .models import Item, ItemImage



class ItemImageCreate(forms.ModelForm):
    class Meta:
        model = ItemImage
        fields = ['image']


class ItemCreateForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Item
        fields = ['title', 'description', 'starting_price', 'end_date', 'image'] 

class ItemUpdateForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Item
        fields = ['title', 'description', 'image'] 
