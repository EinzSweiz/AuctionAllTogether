from django.urls import path
from . import views


app_name = 'auctions'

urlpatterns  = [
    path('', views.ItemList.as_view(), name='auction_list'),
    path('<int:pk>/', views.ItemDetail.as_view(), name='item_detail'),
    path('item-create/', views.ItemCreateView.as_view(), name='item_create'),
    path('item-update/<int:id>/', views.ItemUpdateView.as_view(), name='item_update'),
    path('item-delete/<int:id>/', views.ItemDeleteView.as_view(), name='item_delete'),


]