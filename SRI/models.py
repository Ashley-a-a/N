from django.db import models

from billing.models import Invoice


class SriInvoice(models.Model):

    ESTADOS = [
        ("PENDIENTE", "Pendiente"),
        ("RECIBIDA", "Recibida"),
        ("AUTORIZADA", "Autorizada"),
        ("RECHAZADA", "Rechazada"),
    ]

    invoice = models.OneToOneField(
        Invoice,
        on_delete=models.CASCADE,
        related_name="sri"
    )

    access_key = models.CharField(
        max_length=49,
        unique=True
    )

    authorization_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="PENDIENTE"
    )

    xml = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    authorized_at = models.DateTimeField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"SRI Factura {self.invoice.id}"