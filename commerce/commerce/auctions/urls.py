from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("create/", views.create_listing, name="create"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("categories/", views.categories, name="categories"),
    path("category_listings/<str:category_name>", views.category_listings, name="category_listings"),
    path("my_bids/", views.my_bids, name="my_bids"),

    #POST actions

    path("listing/<int:listing_id>/bid", views.bid, name= "bid"), 
    path("listing/<int:listing_id>/comment", views.comment, name= "comment"),
    path("watchlist/add/<int:listing_id>/toggle_watchlist", views.toggle_watchlist, name="toggle_watchlist"),
    path("watchlist/remove/<int:listing_id>/close/", views.close_listing, name="close_listing"), 
]
