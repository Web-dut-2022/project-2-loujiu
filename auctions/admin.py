from django.contrib import admin

# Register your models here.
from auctions import models

admin.site.register(models.Listing)
admin.site.register(models.Bid)
admin.site.register(models.Commend)
admin.site.register(models.Watchlist)
