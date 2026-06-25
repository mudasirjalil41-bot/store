from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, Product
from django.db.models import F
import logging

logger = logging.getLogger("store")
@receiver(post_save,sender = Order)
def reduce_product_stock(sender,instance,created, **kwargs):
    if created:
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
