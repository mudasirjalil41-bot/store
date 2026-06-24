from django.db.models import Sum,Avg,Count
from django.shortcuts import render
import logging
from django.http import JsonResponse
from django.core.paginator import Paginator ,EmptyPage, PageNotAnInteger
from .models import Product,Order
from django.db.models import F
import json

logger = logging.getLogger("store")
def product_list(request):
    logger.info("product page accessed successfully!")
    try:
       products_queryset  = Product.objects.select_related("category").all()
       search_query = request.GET.get("search",None)
       if search_query:
         products_queryset = products_queryset.filter(name__icontains = search_query)
         if not products_queryset.exists():
            logger.warning(f"product {search_query} not found by user.")
       paginator = Paginator(products_queryset,5)
       page_no = request.GET.get("page",1)
       try:
         obj_page = paginator.page(page_no)
       except PageNotAnInteger:
          obj_page = paginator.page(1)
       except EmptyPage:
               obj_page = paginator.page(paginator.num_pages)


       products_list = []
       for product in obj_page:
         products_list.append({
            "product_name": product.name,
            "price": str(product.price),
            "category": product.category.name,
            "stock": product.stock,
         }

         )
       return JsonResponse({
          "current_page": obj_page.number,
          'total_page': paginator.num_pages,
          "has_next": obj_page.has_next(),
          "has_previous": obj_page.has_previous(),
          "products": products_list,
        },safe = False)

    except Exception as e:
        logger.error(f"unexpected error occurred {str(e)}. ")
        return JsonResponse ("server problem", status = 500)

def advanced_filter_product(request):
    try:

        filter_product = Product.objects.filter(price__gt = 500).annotate(tax_amount = F("price")*0.18,
                                                                      total_amount = F("price")+ F("price")*0.18)
        filter_product_list = []
        for product in filter_product:
          filter_product_list.append({
            "product_name": product.name,
            "original_price": str(product.price),
            "tex_price": round(product.tax_amount,2),
            "total_price":round(product.total_amount,2),

        })

        return JsonResponse({
            "status": "success",
            "total_premium_product": len(filter_product_list),
            "products": filter_product_list
        },safe = False)
    except Exception as e:
        logger.error(f"error in advanced filter view: {str(e)}")
        return JsonResponse({"error":"server internal problem"},status = 500 )
def store_dashboard_stats(request):
    try:
        stats = Product.objects.aggregate(
            total_product = Count("id"),
            average_price = Avg("price"),
            total_inventory_value = Sum(F("price")*F("stock"))
        )

        return JsonResponse({
            "status": "success",
            "dashboard_metric":{
                "total_product_count": stats["total_product"] or 0,
                "average_product_price": round(stats["average_price"] or 0, 2),
                "total_store_worth": round(stats["total_inventory_value"] or 0 ,2),
            }
        },safe = False)
    except Exception as e:
        logger.error(f"error in dashboard stats view: {str(e)}")
        return JsonResponse ({"error":"server internal problem"},status = 500)

def process_order_checkout(request):
    if request.method != "POST":
        return JsonResponse({"error: method not allowed to used post"},status = 405)
    try:
        data = json.loads(request.body)
        product_id = data.get("product_id")
        quantity = data.get("quantity")
        if not quantity or not product_id:
            return JsonResponse ({"error:missing product id and quantity"},status = 400)
        quantity = int(quantity)
        try:
            product = Product.objects.get(id = product_id)
        except Product.DoesNotExist:
            return JsonResponse({"error: product not found"},status = 404)

        if quantity > product.stock:
            logger.warning(f"insufficient stock for product {product.name}")
            return JsonResponse({"error: insufficient stock available"},status = 400)
        else:
            product.stock = F("stock") - quantity
            product.save()
            return JsonResponse({
                "status": "success",
                "message": "Order processed successfully",
                "product_name": product.name,
            })

    except Exception as e:
        logger.error(f"Unexpected error in checkout: {str(e)}")
        return JsonResponse({"error": "Server internal problem"}, status=500)
def customer_purchase_insight(request):
    try:
        delivered_orders = Order.objects.filter(status = "delivered")
        orders_with_cashback = delivered_orders.annotate(
        cashback_amount = F("total_amount") * 0.10
        )
        summary_stats = delivered_orders.aggregate(
          total_order_count = Count("id"),
          total_revenue = Sum("total_amount"),
          average_order_value = Avg("total_amount")
        )
        orders_list = []
        for order in orders_with_cashback:
            orders_list.append({
                "order_id": order.id,
                "customer": order.customer_name,
                "bill_amount": str(order.total_amount),
                "earn_cashback": round(order.cashback_amount,2)
            })

        return JsonResponse({
            "status": "success",
            "store_summary":{
                "total_delivered_order": summary_stats["total_order_count"] or 0,
                "total_money_earn": round(summary_stats["total_revenue"] or 0),
                "average_bill_amount": round(summary_stats["average_order_value"] or 0 ,2)
            },
            "delivered_detail": orders_list
        },safe = False)
    except Exception as e:
        logger.error(f"Unexpected error in insights view: {str(e)}")
        return JsonResponse({"error": "Server internal problem"}, status=500)




