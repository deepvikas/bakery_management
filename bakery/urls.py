from django.urls import path
from django.contrib.auth import views as auth_views 
from .views import AddItemsView, GetItemsView, DeleteItemView, UpdateQuantity

urlpatterns = [
    path('add/items/', AddItemsView.as_view(), name='add-view'),
    path('all/items/', GetItemsView.as_view(), name='all-items-view'),
    path('delete/item/', DeleteItemView.as_view(), name='delete-item-view'),
    path('update/quantity/', UpdateQuantity.as_view(), name='update-quantity-view'),
    # path('delete/user/', DeleteUserView.as_view(), name='delete-users-view'),
]
