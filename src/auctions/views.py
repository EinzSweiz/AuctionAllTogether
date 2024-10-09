from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Item, Status, ItemImage
from mixins.mixins import LoginRequiredMixin
from .forms import ItemCreateForm, ItemUpdateForm
from django.contrib import messages
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
    

class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    template_name = 'auctions/item_create.html'
    form_class = ItemCreateForm
    success_url = reverse_lazy('customers:profile')

    def form_valid(self, form):
        item = form.save(commit=False)
        item.owner = self.request.user
        item.save()

        # Handle image uploads
        image = self.request.FILES.getlist('image')
        ItemImage.objects.create(item=item, image=image)

        messages.success(self.request, 'Item created successfully!')
        return super().form_valid(form)


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    template_name = 'auctions/item_update.html'
    form_class = ItemUpdateForm
    success_url = reverse_lazy('customers:profile')

    def form_valid(self, form):
        item = form.save()
        messages.success(self.request, 'Item updated successfully!')

        image = self.request.FILES.get('image')
        if image:
            ItemImage.objects.filter(item=item).delete()   
        ItemImage.objects.create(item=item, image=image)
        if self.request.htmx:
            return render(self.request, 'auctions/partial_item_update_message.html', {'item': item})

        return super().form_valid(form)
