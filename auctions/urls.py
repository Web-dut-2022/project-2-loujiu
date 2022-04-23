from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories/<str:c>", views.categories),
    path("watchlist", views.watchlist, name="watchlist"),
    path("create", views.create, name="create"),
    path("listing/<str:l_id>", views.show),
    path("user/<str:u_id>", views.user_l)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
