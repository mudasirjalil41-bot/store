from django.db import models
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(max_length = 222)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length = 222)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    category = models.ForeignKey(Category,on_delete = models.CASCADE)
    stock = models.IntegerField()

    def __str__(self):
        return self.name

class Order(models.Model):


    status_choice = [
        ("pending","pending"),
        ("delivered", "delivered"),
        ("cancelled","cancelled"),

    ]
    customer_name = models.CharField(db_index = True, max_length = 100)
    total_amount = models.DecimalField(max_digits = 10, decimal_places = 2,blank=True, null=True)
    status = models.CharField(max_length =20, choices = status_choice, default = 'Pending')
    created_at = models.DateTimeField(auto_now_add = True)
    stock_restored = models.BooleanField(default=False)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Kis product ka order hai
    quantity = models.IntegerField(null = True,blank = True)

    def clean(self):
       super().clean()

       if self.product and self.quantity:
           if self.quantity > self.product.stock:
               raise ValidationError(f"oh this  product only has {self.product.stock} items left in stock. you cannot order {self.quantity} item")


       if self.product and self.quantity:
           if self.quantity <= 0:
               raise ValidationError({"quantity": "quantity must be at least 1"})
           expected_total = self.product.price * self.quantity

           if self.amount_paid is not None:
               if self.amount_paid != expected_total:
                   raise ValidationError(
                       {'amount_paid': f"Total Amount Mismatch! Your total comes to exactly Rs.{expected_total}. "
                                       f"Please enter the correct amount (neither more nor less)."})

           else:
               self.amount_paid = expected_total
           self.total_amount = expected_total

    def save(self,*args,**kwargs):
        self.full_clean()
        super().save(*args,**kwargs)



    def __str__(self):
        return f"Order {self.id} by {self.customer_name}"




