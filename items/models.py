from django.db import models



class Product(models.Model):
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/')
    slug = models.SlugField(max_length=100, unique=True ,blank=True) 

    def save(self, *args, **kwargs):
        self.slug = self.name.replace(" ", "-")
        super().save(*args, **kwargs)
   
    def __str__(self):
        return f"{self.name} - {self.price}"


    


