from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, Product
from django.db.models import F
import logging

logger = logging.getLogger("store")
@receiver(post_save,sender = Order)
def reduce_product_stock(sender,instance,created, **kwargs):
    if created:
        if instance.status == "pending":

            try:
              logger.info(f"signal triggered:order detected from product ID{instance.product_id}")
              updated_count = Product.objects.filter(id = instance.product_id).update(
                stock = F("stock") - instance.quantity
              )
              if updated_count > 0:
                logger.info(f"successfully reduce stock from product ID {instance.product_id} by {instance.quantity}")
              else:
                logger.warning(f"product ID {instance.product_id} not found during stock reduction signal")

            except Exception as e:
              logger.error(f"error in reduce stock signal {str(e)}")

        elif instance.status == "cancelled":
           try:
              Order.objects.filter(id=instance.id).update(stock_restored=True)
              print(f"🟡 New Order direct Cancelled : dont reduce stock.")
           except Exception as e:
            logger.error(f"Error marking new cancelled order: {str(e)}")
    else:
        if instance.status == "cancelled" and not instance.stock_restored:
            try:

                updated_count = Product.objects.filter(id = instance.product_id).update(
                    stock = F("stock") + instance.quantity
                )
                if updated_count > 0:
                    Order.objects.filter(id = instance.id).update(stock_restored = True)
                    logger.info(
                f"❌ Order Cancelled: stock of Product ID {instance.product_id}  {instance.quantity} again increased.")

                    print(   f"❌ Order Cancelled: product ID {instance.product_id} stock increased by {instance.quantity} ")

            except Exception as e:
                 logger.error(f"Error in restore stock signal: {str(e)}")