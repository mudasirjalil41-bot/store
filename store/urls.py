from django.urls import path
from .import views

urlpatterns = [
    path("store_list/", views.product_list, name = "product_list"),
    path("advanced_filter/", views.advanced_filter_product, name="advance_filter"),
    path("dashboard_stats/", views.store_dashboard_stats, name="dashboard_stats"),
    path("purchase_detail/", views.customer_purchase_insight, name="purchase_detail"),
    path("process-checkout/", views.process_order_checkout, name="process_checkout"), # New checkout route added!
]

