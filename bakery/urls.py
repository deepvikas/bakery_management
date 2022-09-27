from django.urls import path
from django.contrib.auth import views as auth_views 
from .views import AddItemsView, GetItemsView, DeleteItemView, UpdateQuantity, ShopDetialView, CreateOrderView, OrderHistoryView

urlpatterns = [
    path('add/items/', AddItemsView.as_view(), name='add-view'),
    path('all/items/', GetItemsView.as_view(), name='all-items-view'),
    path('delete/item/', DeleteItemView.as_view(), name='delete-item-view'),
    path('update/quantity/', UpdateQuantity.as_view(), name='update-quantity-view'),
    path('shop/', ShopDetialView.as_view(), name='shop-view'),
    path('shop/order/', CreateOrderView.as_view(), name='shop-order-view'),
    path('order/history/', OrderHistoryView.as_view(), name='order-history-view')
]
