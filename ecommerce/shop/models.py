from django.db import models

# Create your models here.
class Category(models.Model):
    title=models.CharField(max_length=20)
    image=models.ImageField()
    desc=models.TextField()

    def __str__(self):
        return self.title

class Products(models.Model):
    name=models.CharField(max_length=20)
    image=models.ImageField(upload_to='products',blank=True,null=True)
    desc=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.IntegerField()
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

