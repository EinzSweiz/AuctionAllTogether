from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, UpdateView
from .models import Profile
from .forms import ProfileForm
from mixins.mixins import LoginRequiredMixin
from django.http import Http404
from django.contrib import messages
from django_htmx.http import HttpResponseClientRedirect


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'customers/profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object
        context['items_image'] = profile.items_images
        context['bids_history'] = profile.bids_history
        return context
     
    def get_object(self, queryset=None):
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            raise Http404("Profile does not exist")


class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'customers/update_profile.html'
    success_url = reverse_lazy('customers:profile')

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)
    

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, 'Your profile has been updated successfully!')
        return HttpResponseClientRedirect(self.success_url)