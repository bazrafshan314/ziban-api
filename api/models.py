from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Category(models.Model):
    title = models.CharField(max_length=70)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=70)
    category = models.ManyToManyField(Category)
    description = models.TextField()
    image = models.ImageField(upload_to="uploads/")
    price = models.FloatField()
    inventory = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title


class Order(models.Model):
    address = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title


# class Service(models.Model):
#     title = models.CharField(max_length=50)
#     description = models.TextField()
#     icon = models.ImageField(upload_to="uploads/")
#     time = models.IntegerField()  # zaman anjam
#     status = models.IntegerField()
#     created_at = models.DateTimeField()
#     updated_at = models.DateTimeField()


# class BarberShop(models.Model):
#     title = models.CharField(max_length=50)
#     description = models.TextField()
#     icon = models.ImageField(upload_to="uploads/")
#     email = models.EmailField()
#     mobile = models.CharField(max_length=20)
#     address = models.CharField(max_length=200)
#     manager = models.ForeignKey(User, on_delete=models.CASCADE)
#     score = models.IntegerField()
#     inventory = models.FloatField()
#     type = models.IntegerField()  # gender
#     start_at = models.IntegerField()  # zaman shuru kar
#     end_at = models.IntegerField()  # zaman payan kar
#     status = models.IntegerField()
#     created_at = models.DateTimeField()
#     updated_at = models.DateTimeField()


# class Barbers(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     barber_shop = models.ForeignKey(BarberShops, on_delete=models.CASCADE)
#     start_at = models.IntegerField()  # zaman shuru kar
#     end_at = models.IntegerField()  # zaman payan kar
#     status = models.IntegerField()
#     created_at = models.DateTimeField()
#     updated_at = models.DateTimeField()


# class ServiceBarberRelates(models.Model):
#     barber = models.ForeignKey(Barbers, on_delete=models.CASCADE)
#     service = models.ForeignKey(Services, on_delete=models.CASCADE)
#     extraCost = models.FloatField()
#     level = models.IntegerField()
#     status = models.IntegerField()
#     created_at = models.DateTimeField()
#     updated_at = models.DateTimeField()


# class Reservations(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     barber = models.ForeignKey(Barbers, on_delete=models.CASCADE)
#     total_cost = models.FloatField()
#     start_at = models.IntegerField()  # zaman shuru arayesh
#     end_at = models.IntegerField()  # zaman payan araryesh
#     status = models.IntegerField()
#     created_at = models.DateTimeField()
#     updated_at = models.DateTimeField()


# class ReservationItems(models.Model):
#     service_barber_relate = models.ForeignKey(
#         ServiceBarberRelates, on_delete=models.CASCADE
#     )
#     reservation = models.ForeignKey(Reservations, on_delete=models.CASCADE)
#     status = models.IntegerField()
#     created_at = models.DateTimeField()
#     updated_at = models.DateTimeField()


# class Gifts(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     code = models.CharField(max_length=15)
#     type = models.IntegerField()
#     amount = models.FloatField()
#     status = models.IntegerField()
#     created_at = models.DateTimeField()
#     updated_at = models.DateTimeField()


# class Payments(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     card_number = models.CharField(max_length=30)
#     amount = models.FloatField()
#     status = models.IntegerField()
#     created_at = models.DateTimeField()
#     updated_at = models.DateTimeField()


# class Stores(models.Model):
#     title = models.CharField(max_length=50)
#     description = models.TextField()
#     icon = models.ImageField(upload_to="uploads/")
#     email = models.EmailField()
#     mobile = models.CharField(max_length=20)
#     address = models.CharField(max_length=200)
#     manager = models.ForeignKey(User, on_delete=models.CASCADE)
#     score = models.IntegerField()
#     inventory = models.FloatField()
#     status = models.IntegerField()
#     created_at = models.DateTimeField()
#     updated_at = models.DateTimeField()


# class Comments(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     final_product = models.ForeignKey(FinalProducts, on_delete=models.CASCADE)
#     title = models.CharField(max_length=50)
#     description = models.TextField()
#     score = models.IntegerField()
#     status = models.IntegerField()
#     created_at = models.DateTimeField()
#     updated_at = models.DateTimeField()


# class CommentLikes(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     comment = models.ForeignKey(Comments, on_delete=models.CASCADE)
#     status = models.IntegerField()
#     created_at = models.DateTimeField()
#     updated_at = models.DateTimeField()


# class Replies(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     comment = models.ForeignKey(Comments, on_delete=models.CASCADE)
#     title = models.CharField(max_length=50)
#     description = models.TextField()
#     status = models.IntegerField()
#     created_at = models.DateTimeField()
#     updated_at = models.DateTimeField()


# class ReplyLikes(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     reply = models.ForeignKey(Replies, on_delete=models.CASCADE)
#     status = models.IntegerField()
#     created_at = models.DateTimeField()
#     updated_at = models.DateTimeField()
