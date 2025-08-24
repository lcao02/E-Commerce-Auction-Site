from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Category, Listing, Bid, Comment, Watchlist
from .forms import ListingForm

from .models import User


def index(request):
    listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
    })
    


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    

from django.contrib import messages

@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            # Set current_price to starting_bid by default
            listing.current_price = listing.starting_bid
            listing.save()
            messages.success(request, "Listing created successfully!")
            return redirect("index")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ListingForm()

    return render(request, "auctions/create.html", {
        "form": form
    })


def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    is_watching = Watchlist.objects.filter(user=request.user, listing=listing).exists() if request.user.is_authenticated else False
    highest_bid = listing.bids.order_by('-amount').first()
    is_owner = request.user == listing.owner if request.user.is_authenticated else False
    comments = Comment.objects.filter(listing=listing)

    error = None

    if request.method == "POST" and "place_bid" in request.POST:
        try:
            new_bid = float(request.POST.get("bid"))
            minimum_bid = listing.starting_bid if not highest_bid else highest_bid.amount

            if new_bid < minimum_bid:
                error = f"Your bid must be at least ${minimum_bid}."
            else:
                Bid.objects.create(bidder=request.user, listing=listing, amount=new_bid)
                return redirect("listing", listing_id=listing.id)

        except ValueError:
            error = "Please enter a valid bid amount."

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "is_watching": is_watching,
        "comments": comments,
        "highest_bid": highest_bid,
        "is_owner": is_owner
    })

def active_listings(request):
    listings = Listing.objects.filter(is_active=True)  # or .filter(closed=False)
    return render(request, "auctions/active_listings.html", {
        "listings": listings
    })

@login_required
def bid(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    bid_amount = float(request.POST["bid"])
    current_price = listing.current_price

    if bid_amount > current_price:
        bid = Bid(bidder=request.user, listing=listing, amount=bid_amount)
        bid.save()
        listing.current_price = bid_amount
        listing.save()
        message = "Bid placed successfully!"
    else:
        message = "Bid must be higher than current price."

    return redirect("listing", listing_id=listing.id)

@login_required
def my_bids(request):
    bids = Bid.objects.filter(bidder=request.user).order_by('-timestamp')  # or just '-id'
    return render(request, "auctions/my_bids.html", {
        "bids": bids
    })


@login_required
def comment(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    content = request.POST.get("content", "").strip()  # Fix here

    if content:  # only save non-empty comments
        Comment.objects.create(
            author=request.user,
            listing=listing,
            content=content,
        )

    return redirect("listing", listing_id=listing.id)


@login_required
def toggle_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    watch_entry = Watchlist.objects.filter(user=request.user, listing=listing).first()

    if watch_entry:
        watch_entry.delete()
    else:
        Watchlist.objects.create(user=request.user, listing=listing)

    return redirect("listing", listing_id=listing.id)


@login_required
def close_listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.user != listing.owner:
        return HttpResponse("Unauthorized", status=403)
    
    highest_bid = listing.bids.order_by('-amount').first()
    if highest_bid:
        listing.winner = highest_bid.bidder

    listing.is_active = False
    listing.save()
    return redirect("listing", listing_id=listing.id)




@login_required
def watchlist(request):
    listings = Listing.objects.filter(watchlist__user=request.user)
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })



def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def category_listings(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    listings = Listing.objects.filter(category=category,is_active=True)
    return render(request, "auctions/category_listings.html", {
        "category": category,
        "listings": listings
    })

