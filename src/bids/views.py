from django.shortcuts import get_object_or_404, redirect
from auctions.models import Item
from django.views.generic import ListView, CreateView
from .models import AuctionHistory, Bid
from .forms import BidCreateForm
from django_htmx.http import HttpResponseClientRefresh
from .tasks import send_rebid_notification
from django.contrib import messages

class BidsHistory(ListView):
    model = AuctionHistory
    context_object_name = 'bids'
    paginate_by = 10
    template_name = 'bids/bids_history.html'

    def get_queryset(self):
        item_id = self.kwargs['item_id']
        return Bid.objects.filter(item_id=item_id).order_by('-amount')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_id = self.kwargs['item_id']
        context['item'] = Item.objects.get(id=item_id)
        return context
    

class AddBid(CreateView):
    model = Bid
    form_class = BidCreateForm
    template_name = 'bids/add_bid.html'
    context_object_name = 'bid'

    def get_item(self):
        return get_object_or_404(Item, id=self.kwargs.get('item_id'))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        item = self.get_item()
        kwargs['item'] = item
        return kwargs

    def form_valid(self, form):
        item = self.get_item() 
        existing_bid = Bid.objects.filter(item=form.item, bidder=self.request.user).first()
        if existing_bid:
            existing_bid.amount = form.cleaned_data['amount']
            existing_bid.save()
            send_rebid_notification.delay(existing_bid.id)  # Send notification via Celery
            messages.success(self.request, 'Your bid has been updated successfully.')
            return HttpResponseClientRefresh()

        form.instance.item = item
        form.instance.bidder = self.request.user
        bid = form.save()
        send_rebid_notification.delay(bid.id)
        messages.success(self.request, 'Your bid has been placed successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.get_item()
        last_bid = Bid.objects.filter(item=item).order_by('-created_at').first()
        context['last_bid'] = last_bid 
        context['item'] = item
        return context