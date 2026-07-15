import random
import string
from datetime import datetime

from .models import SriInvoice


def generate_access_key():

    return "".join(
        random.choices(string.digits, k=49)
    )


def generate_xml(invoice):

    xml = f"""
<factura>

    <numero>{invoice.id}</numero>

    <cliente>{invoice.customer.full_name}</cliente>

    <total>{invoice.total}</total>

</factura>
"""

    return xml


def send_to_sri(invoice):

    access_key = generate_access_key()

    xml = generate_xml(invoice)

    sri = SriInvoice.objects.create(

        invoice=invoice,

        access_key=access_key,

        authorization_number=f"AUT-{invoice.id}",

        status="AUTORIZADA",

        xml=xml,

        authorized_at=datetime.now()

    )
    
    invoice.sri_status = "AUTORIZADA"
    invoice.save(update_fields=[])

    return sri