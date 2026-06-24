from django.urls import path
from .import views

urlpatterns = [
    path("store_list/", views.product_list, name = "product_list"),
    path("advanced filter/", views.advanced_filter_product, name="advance_filter"),
    path("dashboard_stats/", views.store_dashboard_stats, name="dashboard_stats"),

]

