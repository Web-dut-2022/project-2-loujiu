from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from . import models
from .models import User, Listing, Bid


def index(request):
    items = Listing.objects.all()
    listings = [i for i in items if i.isActive == 0]
    return render(request, "auctions/index.html", {
        'categories': models.Categories,
        'listings': listings,
        'n1': "active",
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


def categories(request, c):
    items = models.Listing.objects.filter(category=c)
    category = models.Categories.__dict__['_value2member_map_'][c].label
    listings = [i for i in items if i.isActive == 0]
    return render(request, "auctions/index.html", {
        'categories': models.Categories,
        'title': category,
        'listings': listings,
        'n2': "active"
    })


def watchlist(request):
    items = models.Watchlist.objects.filter(user=request.user)
    listings = [i.listing for i in items]
    return render(request, "auctions/index.html", {
        'categories': models.Categories,
        'listings': listings,
        'n3': "active"
    })


def create(request):
    if request.method == "POST":
        new_l = models.Listing()
        new_l.name = request.POST.get("name")
        new_l.seller = request.user
        new_l.buyer = request.user
        new_l.price = request.POST.get("price")
        new_l.itemText = request.POST.get("inf")
        new_l.category = request.POST.get("category")
        new_l.pic = request.FILES.get("picture")
        new_l.save()
        listing_id = str(new_l.ID)
        return redirect("listing/" + listing_id)
    else:
        return render(request, "create.html", {
            'categories': models.Categories,
            'n4': "active"
        })


def show(request, l_id):
    item = Listing.objects.get(ID=l_id)

    # 判断是否收藏
    try:
        ifwl = models.Watchlist.objects.get(listing=l_id, user=request.user)
        btn = "btn btn-success btn-sm"
    except models.Watchlist.DoesNotExist:
        ifwl = False
        btn = "btn btn-default btn-sm"

    # 查询是否有投标和投标最大值
    try:
        bids = Bid.objects.filter(listing=l_id).first()
        b_max = bids.bid
        msg = "Latest bid: $" + str(b_max)
    except (models.Bid.DoesNotExist, AttributeError):
        b_max = 0
        msg = ""

    if request.method == "GET":
        # 根据用户状态决定可用功能
        if item.isActive == 1:
            i = btn1 = btn2 = "disabled"
            messages.success(request, "You have won this auction!")
        else:
            if item.seller == request.user:
                btn2 = "disabled"
                i = btn1 = ""
            else:
                btn1 = "disabled"
                i = btn2 = ""
        num = Bid.objects.filter(listing=l_id).count()
        commends = models.Commend.objects.filter(listing=l_id)
        return render(request, "listing.html", {
            'categories': models.Categories,
            'listing': item,
            'num': num,
            'msg': msg,
            'btn': btn,
            'i': i,
            'btn1': btn1,
            'btn2': btn2,
            'commends': commends
        })
    else:
        # 收藏
        if request.POST.get("h") == "wl":
            if ifwl:
                ifwl.delete()
            else:
                wl = models.Watchlist()
                wl.user = request.user
                wl.listing = item
                wl.save()
        # 关闭拍卖
        elif request.POST.get("h") == "close":
            item.isActive = 1
        # 评论
        elif request.POST.get("h") == "com":
            com = models.Commend()
            com.user = request.user
            com.listing = item
            com.text = request.POST.get("com")
            com.save()
        # 投标，返回成功或失败的提示
        else:
            b = int(request.POST.get("bid"))
            ans = bid(request, b, item, b_max)
            if ans:
                messages.success(request, "Successfully bid!")
            else:
                messages.warning(request, "Your bid should be higher than current bid!")
        return redirect("/listing/"+l_id)


@login_required
def bid(request, b, item, b_max):
    # 判断投标是否成功
    price = item.price
    if b > b_max and b >= price:
        new_b = models.Bid()
        new_b.bid = b
        new_b.listing = item
        new_b.bidder = request.user
        new_b.save()
        return True
    else:
        return False


def user_l(request, u_id):
    items = models.Listing.objects.filter(seller=u_id)
    return render(request, "auctions/index.html", {
        'categories': models.Categories,
        'listings': items,
        'n3': "active"
    })