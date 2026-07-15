from django.db import models


class PayPalTransaction(models.Model):

    order_id = models.CharField(max_length=100, unique=True)

    capture_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    status = models.CharField(max_length=30)

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    created_at = models.DateTimeField(auto_now_add=True)

    approved_at = models.DateTimeField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.order_id