from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Categories(models.TextChoices):
    FASHION = 'FA', 'Fashion'
    ELECTRONICS = 'EL', 'Electronics'
    SPORTS = 'SP', 'Sports'
    BOOKS = 'BO', 'Books'


class IsActive(models.IntegerChoices):
    ACTIVE = 0, 'Active'
    INACTIVE = 1, 'Inactive'


# 拍卖清单
class Listing(models.Model):
    name = models.CharField(max_length=30, verbose_name="Item name")
    seller = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name="Seller",
                               to_field='username',
                               related_name="seller",
                               null=True)
    buyer = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              verbose_name="Buyer",
                              to_field='username',
                              related_name="buyer",
                              null=True,
                              blank=True)
    ID = models.BigAutoField(primary_key=True,
                             editable=False)
    createTime = models.DateTimeField(default=timezone.now,
                                      verbose_name="Created time")
    pic = models.ImageField(null=True,
                            upload_to='img/',
                            verbose_name="Image")
    price = models.DecimalField(default=0.00,
                                max_digits=10,
                                decimal_places=2,
                                verbose_name="Price")
    itemText = models.TextField(verbose_name="Introduction")
    category = models.CharField(max_length=2,
                                choices=Categories.choices,
                                default=Categories.FASHION,
                                verbose_name="Category")
    isActive = models.IntegerField(choices=IsActive.choices,
                                   default=IsActive.ACTIVE,
                                   verbose_name="Status")

    class Meta:
        db_table: "listing"
        ordering = ['-createTime']


# 投标
class Bid(models.Model):
    ID = models.BigAutoField(primary_key=True,
                             editable=False)
    bid = models.DecimalField(default=0.00,
                              max_digits=10,
                              decimal_places=2,
                              verbose_name="Bid")
    listing = models.ForeignKey(Listing,
                                on_delete=models.CASCADE,
                                verbose_name="Listing",
                                to_field='ID')
    bidder = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name="Bidder",
                               to_field='username')

    class Meta:
        db_table: "bid"
        ordering = ['listing', '-bid']


# 对拍卖清单进行评论
class Commend(models.Model):
    ID = models.BigAutoField(primary_key=True,
                             editable=False)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name="Username",
                             to_field='username')
    text = models.TextField(verbose_name="Commend")
    listing = models.ForeignKey(Listing,
                                on_delete=models.CASCADE,
                                verbose_name="Listing",
                                to_field='ID')
    createTime = models.DateTimeField(default=timezone.now,
                                      verbose_name="Created time")

    class Meta:
        db_table: "commend"
        ordering = ['listing', '-createTime']


# watchlist
class Watchlist(models.Model):
    ID = models.BigAutoField(primary_key=True,
                             editable=False)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name="Username",
                             to_field='username')
    listing = models.ForeignKey(Listing,
                                on_delete=models.CASCADE,
                                verbose_name="Listing",
                                to_field='ID')

    class Meta:
        db_table: "listing"
        ordering = ['listing']
