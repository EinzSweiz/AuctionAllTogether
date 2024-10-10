from django.http import Http404, HttpResponseForbidden
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from .models import Item, Status, ItemImage
from mixins.mixins import LoginRequiredMixin
from .forms import ItemCreateForm, ItemUpdateForm
from django.contrib import messages
from django_htmx.http import HttpResponseClientRefresh
from .tasks import send_item_created_email, send_item_updated_email, send_delete_confirmation_email
from helpers.token_helpers import generate_delete_token, validate_delete_token
from django.contrib.sites.shortcuts import get_current_site
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

        send_item_created_email.delay(item.id)
        messages.success(self.request, 'Item created successfully!')

        image = self.request.FILES.get('image')
        if image:
            try:
                ItemImage.objects.create(item=item, image=image)
            except Exception as e:
                messages.error(self.request, 'Error uploading image: {}'.format(e))

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
        
        site_domain = get_current_site(self.request).domain
        owner_email = self.request.user.email
        
        send_item_updated_email.delay(item.id, site_domain, owner_email)

        messages.success(self.request, 'Item updated successfully!')

        image = self.request.FILES.get('image')
        if image:
            ItemImage.objects.filter(item=item).delete()
            ItemImage.objects.create(item=item, image=image)

        if self.request.htmx:
            return HttpResponseClientRefresh()

        return super().form_valid(form)

class ItemDeleteView(LoginRequiredMixin, View):
    model = Item  # Assuming you have imported Item at the top of the file
    success_url = reverse_lazy('customers:profile')

    def get_object(self, item_id):
        """Retrieve the item object by ID."""
        try:
            return Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            raise Http404('Item does not exist')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object(kwargs['id'])
        if self.object.owner != self.request.user:
            raise Http404('You cannot delete this item')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        item_id = self.object.id
        
        # Generate token and send email
        token = generate_delete_token(item_id)
        confirm_url = f'{self.request.build_absolute_uri("/auctions/item-delete/confirm-delete/")}{item_id}/{token}/' 
        send_delete_confirmation_email.delay(item_id, confirm_url)
        messages.info(request, "A confirmation email has been sent to you. Please check your email to confirm the deletion.")
        
        return redirect('customers:profile')
class ItemDeleteConfirmView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        item_id = kwargs['item_id']
        token = kwargs['token']
        
        try:
            item = Item.objects.get(id=item_id)

            # Validate the token
            if not validate_delete_token(item.id, token):
                return HttpResponseForbidden("Invalid or expired token. Item cannot be deleted.")

            # Proceed to show confirmation template
            return render(request, 'auctions/item_delete.html', {'item': item, 'token': token})
        except Item.DoesNotExist:
            return Http404('Item does not exist')
    
    def post(self, request, *args, **kwargs):
        item_id = kwargs['item_id']
        token = kwargs['token']
        
        try:
            item = Item.objects.get(id=item_id)

            # Validate the token
            if not validate_delete_token(item.id, token):
                return HttpResponseForbidden("Invalid or expired token. Item cannot be deleted.")

            # Delete the item
            item.delete()
            messages.success(request, "Item deleted successfully!")
            return redirect('customers:profile')  # Redirect to the profile page after deletion
        except Item.DoesNotExist:
            return Http404('Item does not exist')
