from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Services(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    icon = models.ImageField(upload_to='uploads/')
    time = models.IntegerField()  # zaman anjam
    status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class BarberShops(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    icon = models.ImageField(upload_to='uploads/')
    email = models.EmailField()
    mobile = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    inventory = models.FloatField()
    type = models.IntegerField()  # gender
    start_at = models.IntegerField()  # zaman shuru kar
    end_at = models.IntegerField()  # zaman payan kar
    status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class Barbers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    barber_shop = models.ForeignKey(BarberShops, on_delete=models.CASCADE)
    start_at = models.IntegerField()  # zaman shuru kar
    end_at = models.IntegerField()  # zaman payan kar
    status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class ServiceBarberRelates(models.Model):
    barber = models.ForeignKey(Barbers, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    extraCost = models.FloatField()
    level = models.IntegerField()
    status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class Reservations(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    barber = models.ForeignKey(Barbers, on_delete=models.CASCADE)
    total_cost = models.FloatField()
    start_at = models.IntegerField()  # zaman shuru arayesh
    end_at = models.IntegerField()  # zaman payan araryesh
    status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class ReservationItems(models.Model):
    service_barber_relate = models.ForeignKey(ServiceBarberRelates, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservations, on_delete=models.CASCADE)
    status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class Gifts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=15)
    type = models.IntegerField()
    amount = models.FloatField()
    status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class Payments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=30)
    amount = models.FloatField()
    status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class Stores(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    icon = models.ImageField(upload_to='uploads/')
    email = models.EmailField()
    mobile = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    inventory = models.FloatField()
    status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class Products(models.Model):
    title = models.CharField(max_length=70)
    description = models.TextField()
    main_pic = models.ImageField(upload_to='uploads/')
    status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class FinalProducts(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    store = models.ForeignKey(Stores, on_delete=models.CASCADE)
    color = models.IntegerField()
    inventory = models.IntegerField()
    price = models.FloatField()
    discount = models.FloatField()
    score = models.IntegerField()
    status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class ProductPictures(models.Model):
    final_product = models.ForeignKey(FinalProducts, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='uploads/')


class CartItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    final_product = models.ForeignKey(FinalProducts, on_delete=models.CASCADE)
    count = models.IntegerField()
    status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    discount = models.FloatField()
    gift = models.ForeignKey(Gifts, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class OrderItems(models.Model):
    final_product = models.ForeignKey(FinalProducts, on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    amount = models.FloatField()
    discount = models.FloatField()
    count = models.IntegerField()
    status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    final_product = models.ForeignKey(FinalProducts, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    score = models.IntegerField()
    status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class CommentLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE)
    status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class Replies(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class ReplyLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey(Replies, on_delete=models.CASCADE)
    status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


