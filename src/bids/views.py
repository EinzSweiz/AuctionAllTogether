from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from auctions.models import Item
from django.views.generic import ListView, CreateView
from .models import AuctionHistory, Bid
from .forms import BidCreateForm

class BidsHistory(ListView):
    model = AuctionHistory
    context_object_name = 'bids'
    paginate_by = 10
    template_name = 'bids/bids_history.html'

    def get_queryset(self):
        item_id = self.kwargs['item_id']
        return Bid.objects.filter(item_id=item_id)
    

class AddBid(CreateView):
    model = Bid
    form_class = BidCreateForm
    template_name = 'bids/add_bid.html'
    context_object_name = 'item'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        item = get_object_or_404(Item, id=self.kwargs.get('item_id'))
        kwargs['item'] = item
        return kwargs

    def form_valid(self, form):
        item = form.item
        existing_bid = Bid.objects.filter(item=form.item, bidder=self.request.user).first()
        if existing_bid:
            existing_bid.amount = form.cleaned_data['amount']
            existing_bid.save()
            return super().form_valid(form)

        form.instance.item = item
        form.instance.bidder = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('auctions:item_detail', kwargs={'pk': self.kwargs.get('item_id')})
