# E-commerce Auction Site

A web-based auction platform built with Django that allows users to create listings, place bids, comment on items, and maintain a personalized watchlist.  
The site provides an end-to-end e-commerce experience, including categories, admin management, and auction closing functionality.

---

## 🚀 Features
- **User Authentication**: Register, log in, and log out securely.
- **Create Listings**: Users can post new auction listings with title, description, starting bid, image URL, and optional category.
- **Active Listings Page**: Displays all active auctions with details like current price, description, and images.
- **Listing Detail Page**:
  - View full listing details including bids and comments.
  - Add or remove items from a personalized **watchlist**.
  - Place valid bids (must exceed the current highest bid).
  - Close auctions (for listing creators) and determine the winning bidder.
  - Display winner information on closed listings.
- **Watchlist Page**: View all saved auction items in one place for quick access.
- **Comments**: Users can add and view comments on individual listings.
- **Categories**: Browse listings by category (e.g., Fashion, Electronics, Toys).
- **Django Admin**: Full CRUD control over listings, bids, comments, and categories.

---

## 🛠️ Tech Stack
- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: SQLite (default; can be swapped with PostgreSQL/MySQL)
- **IDE**: VS Code

---

## 📦 Installation
1. **First Create a virtual environment**: python -m venv venv
                                           venv\Scripts\activate #for windows
2. **Run migrations**: python manage.py makemigration
                       python manage.py migrate
3. **Start developement server**" python manage.py runserver
