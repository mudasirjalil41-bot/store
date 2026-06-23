
from django.shortcuts import render
import logging
from django.http import JsonResponse
from django.core.paginator import Paginator ,EmptyPage, PageNotAnInteger
from .models import Product
from django.db.models import F

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





