from django.urls import path

from .views import delete_category, delete_product, edit_product, home


urlpatterns = [
    path('', home, name='home'),
    path('category/<int:pk>/delete/', delete_category, name='delete_category'),
    path('product/<int:pk>/delete/', delete_product, name='delete_product'),
    path('product/<int:pk>/edit/', edit_product, name='edit_product'),
]