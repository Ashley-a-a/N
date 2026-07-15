from django.http import JsonResponse

from billing.models import Invoice

from .services import send_to_sri


def authorize_invoice(request, invoice_id):

    invoice = Invoice.objects.get(pk=invoice_id)

    sri = send_to_sri(invoice)

    return JsonResponse({

        "estado": sri.status,

        "clave": sri.access_key,

        "autorizacion": sri.authorization_number

    })