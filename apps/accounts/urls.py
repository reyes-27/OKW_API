from django.urls import path
from .views import (
    CustomerProfileDetailView, 
    RegisterView, 
    LoginView,
    CSRFApiView,
    )
urlpatterns = [
    path("customers/<uuid:id>/", view=CustomerProfileDetailView.as_view(), name="customer-detail"),
    path("register/", view=RegisterView.as_view(), name="register"),
    path("login/", view=LoginView.as_view(), name="login"),
    path("csrf/", view=CSRFApiView.as_view(), name="csrf" ),
]