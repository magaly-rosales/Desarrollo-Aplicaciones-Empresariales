from django.urls import path

from shop import views

urlpatterns = [
    path("cart/", views.cart_detail),
    path("cart/items/", views.cart_add),
    path("cart/items/<str:sku>/", views.cart_remove),
    path("cart/coupon/", views.cart_coupon),
    path("cart/checkout/", views.cart_checkout),
    path("cart/audit/", views.cart_audit),
]
