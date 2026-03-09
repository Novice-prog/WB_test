from django.urls import path
from .views import RegisterView, MeView, TopUpBalanceView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("me/", MeView.as_view()),
    path("balance/top-up/", TopUpBalanceView.as_view(), name="top-up-balance"),
]