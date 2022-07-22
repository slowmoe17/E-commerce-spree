from django.db import models
from users.models import CustomUser
from django.db.models.signals import pre_save
from django.dispatch import receiver
from items.models import Product
from django.contrib.auth import get_user_model

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order = models.BooleanField(default=False ,blank=True , null=True)
    total_price = models.FloatField(default=0 ,blank=True , null=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(blank=True, null=True)
    total_price = models.FloatField(blank=True, null=True)


    def save(self, *args, **kwargs):
        self.price = self.product.price
        self.total_price = self.quantity * self.price
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Product Name : {self.product.name} -  Quantity : {self.quantity} - TotalPrice : {self.total_price}"

@receiver(pre_save, sender=CartItem)
def update_total_price(sender, instance, **kwargs):
    # get all cart items for this cart and update total price of cart
    cart = instance.cart
    cart.total_price = 0
    cart.save()
    cart_items = CartItem.objects.filter(cart=cart)
    for item in cart_items:
        cart.total_price += item.total_price
    cart.save()
    
"""@receiver(pre_save, sender=get_user_model())
def create_cart(sender, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)"""


class Transaction(models.Model):
    order_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)



    def __str__(self):
        return f"{self.cart.user.username} - {self.amount}"

@receiver(pre_save, sender=CartItem)
def update_total_price(sender, instance, **kwargs):
    cart = instance.cart
    cart.total_price = 0
    cart.save()
    cart_items = CartItem.objects.filter(cart=cart)
    for item in cart_items:
        cart.total_price += item.total_price
    cart.save()



"""class OrderStatus(models.Model):
    order_status = (
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    )
    order = models.ForeignKey(Transaction, on_delete=models.CASCADE , default="success")
    status = models.CharField(max_length=50, choices=order_status, )

    def __str__(self):
        return f"{self.order.cart.user.username} - {self.status}"
    

#signal that create new orderstatus for each transaction when new transaction is created
@receiver(pre_save, sender=Transaction)
def create_orderstatus(sender, instance, **kwargs):
    if instance.pk is None:
        OrderStatus.objects.create(order=instance)
    else:
        OrderStatus.objects.filter(order=instance).update(status=instance.status)






    



    












    








    
        

   


     
"""

    

