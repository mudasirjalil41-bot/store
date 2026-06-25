from django.urls import path
from .import views

urlpatterns = [
    path("store_list/", views.product_list, name = "product_list"),
    path("advanced_filter/", views.advanced_filter_product, name="advance_filter"),
    path("dashboard_stats/", views.store_dashboard_stats, name="dashboard_stats"),
    path("purchase_detail/", views.customer_purchase_insight, name="purchase_detail"),
    path("process_checkout/", views.process_order_checkout, name="process_checkout"),
    path("low_stock/", views.low_stock_alert_report, name="low_stock"), # New checkout route added!
    path("flash_sale/", views.apply_flash_sale, name="flash_sale"), # New checkout route added!
    # New checkout route added!
]

