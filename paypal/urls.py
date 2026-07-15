from django.urls import path

from . import views

app_name = "paypal"

urlpatterns = [

    path(
        "checkout/<int:invoice_id>/",
        views.checkout,
        name="checkout",
    ),

    path(
        "complete/<int:invoice_id>/",
        views.complete_payment,
        name="complete_payment",
    ),

]