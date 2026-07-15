from django.urls import path

from . import views

urlpatterns = [

    path(
        "authorize/<int:invoice_id>/",
        views.authorize_invoice,
        name="authorize_invoice"
    ),

]