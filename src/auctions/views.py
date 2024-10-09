from django.http import Http404
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Item, Status, ItemImage
from mixins.mixins import LoginRequiredMixin
from .forms import ItemCreateForm, ItemUpdateForm
from django.contrib import messages
from django_htmx.http import HttpResponseClientRefresh
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

class ItemDetail(LoginRequiredMixin, DetailView):
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

        messages.success(self.request, 'Item created successfully!')

        image = self.request.FILES.get('image')
        if image:
            ItemImage.objects.create(item=item, image=image)

        if self.request.htmx:
            return render(self.request, 'auctions/partial_item_update_message.html', {'item': item})

        return super().form_valid(form)

class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    template_name = 'auctions/partial_item_update.html'
    form_class = ItemUpdateForm
    success_url = reverse_lazy('customers:profile')
    pk_url_kwarg = 'id'

    def dispatch(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Item.DoesNotExist:
            raise Http404('Item not found.')

        if self.object.owner != self.request.user:
            raise Http404('You are not the owner of this item.')
        
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        item = form.save()
        messages.success(self.request, 'Item updated successfully!')

        image = self.request.FILES.get('image')
        if image:
            # Handle image update
            ItemImage.objects.filter(item=item).delete()
            ItemImage.objects.create(item=item, image=image)

        # Trigger a client-side refresh if the request is made via HTMX
        if self.request.htmx:
            return HttpResponseClientRefresh()

        return super().form_valid(form)
    

class ItemDeleteView(DeleteView):
    model = Item
    success_url = reverse_lazy('customers:profile')
    pk_url_kwarg = 'id'

    def dispatch(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except:
            raise Http404('Item is not exists')
        if self.object.owner != self.request.user:
            raise Http404('You can not delete this item')


        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "Item deleted successfully!")
        return super().delete(request, *args, **kwargs)