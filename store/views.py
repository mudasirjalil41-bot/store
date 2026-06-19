
from django.shortcuts import render
import logging
from django.http import JsonResponse
from django.core.paginator import Paginator ,EmptyPage, PageNotAnInteger
from .models import Product

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



