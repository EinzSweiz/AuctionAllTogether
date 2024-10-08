from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from .models import Item, Status

class ItemList(ListView):
    model = Item
    template_name = 'auctions/item_list.html'
    context_object_name = 'items'
    paginate_by = 5

    def get_queryset(self):
        return Item.objects.filter(status=Status.ON_SALE).order_by('created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Auction Items'
        return context

class ItemDetail(DetailView):
    model = Item
    template_name = 'auctions/detail_list.html'
    context_object_name = 'item'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context


