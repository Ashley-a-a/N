from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone

from billing.models import Invoice
from billing.services import emit_invoice

from .services import create_order, capture_order
from SRI.services import send_to_sri

def checkout(request, invoice_id):

    invoice = get_object_or_404(
        Invoice,
        pk=invoice_id
    )

    if invoice.estado != Invoice.BORRADOR:

        messages.error(
            request,
            "La factura ya fue procesada."
        )

        return redirect(
            "billing:invoice_detail",
            pk=invoice.id
        )

    paypal = create_order(invoice)

    invoice.paypal_order_id = paypal["id"]

    invoice.paypal_status = paypal["status"]

    invoice.save()

    return redirect(
        "paypal:complete_payment",
        invoice.id
    )
    
def complete_payment(request, invoice_id):

    invoice = get_object_or_404(
        Invoice,
        pk=invoice_id
    )

    paypal = capture_order(
        invoice.paypal_order_id
    )

    invoice.paypal_status = paypal["status"]
    invoice.payment_method = "paypal"

    invoice.paid_at = timezone.now()

    invoice.save(
        update_fields=[
            "paypal_order_id",
            "paypal_status",
            "payment_method",
            "paid_at",
        ]
    )
    
    if paypal["status"] == "COMPLETED":

        emit_invoice(
            invoice,
            request.user,
            tipo_pago=Invoice.CONTADO
        )

        sri = send_to_sri(invoice)

        invoice.sri_status = sri.status

        invoice.sri_authorization = sri.authorization_number

        invoice.save()

        messages.success(

            request,

            "Pago realizado correctamente mediante PayPal."

        )

    else:

        messages.error(

            request,

            "No fue posible completar el pago."

        )

    return redirect(
        "billing:invoice_detail",
        pk=invoice.id
    )
    