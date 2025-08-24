from django.contrib import admin
from auctions.models import Category, Listing, Bid, Comment, Watchlist  

admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Bid)   
admin.site.register(Comment)
admin.site.register(Watchlist)