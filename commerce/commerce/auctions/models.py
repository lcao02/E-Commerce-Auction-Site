from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="winning_listings")
    #watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")
    """
    def toggle_watchlist(self, user):
        if user in self.watchlist.all():
             self.watchlist.remove(user)
             return False  # Removed
        else:
            self.watchlist.add(user)
            return True  # Added

    def is_watched_by(self, user):
        return user in self.watchlist.all()

    def __str__(self):
        return f"{self.title} - {self.current_price}"
"""

    
class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(default="(No comment)")
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.author} on {self.listing.title}: {self.content[:30]}"
    

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "listing")  # Prevent duplicates

    def __str__(self):
        return f"{self.user.username} - {self.listing.title}"

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"${self.amount} by {self.bidder.username} on {self.listing.title}"