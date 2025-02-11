from django.db import models

# Create your models here.

class Category(models.Model):
 name = models.CharField(max_length=50)

 def __str__(self):
  return self.name
 class Meta:
  verbose_name_plural = 'categories'
  


class product(models.Model):
 name = models.CharField(max_length=30)
 price =models.DecimalField(default=0,decimal_places=3, max_digits=6)
 image = models.ImageField(upload_to='static/upload')
 category = models.ForeignKey(Category,on_delete=models.CASCADE, default=1)
 description = models.CharField(default='', max_length=200, null=True, blank=True)


 def __str__ (self):
  return self.name
