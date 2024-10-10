from django.urls import path
from . import views

app_name = 'bids'

urlpatterns = [
    path('history/<int:item_id>/',  views.BidsHistory.as_view(), name='bids_history'),
    path('<int:item_id>/add-bid/', views.AddBid.as_view(), name='add_bid'),
]