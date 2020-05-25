import json
import logging

from django.shortcuts import redirect
from django.utils.module_loading import import_string
from django.utils.translation import get_language
from payments import PaymentStatus
from payments.core import BasicProvider
from payments.forms import PaymentForm
from payments_portmone.forms import PortmoneResponseForm
from payments_portmone.service import PortmonePayment

logger = logging.getLogger("payments_portmone")


class PortmoneProvider(BasicProvider):
    """This class defines the Portmone provider API."""

    def __init__(self, payee_id: str, login: str, password: str, **kwargs):
        self.payee_id = payee_id
        self.login = login
        self.password = password
        self.endpoint = kwargs.pop("endpoint", "https://www.portmone.com.ua/gateway/")
        service_path = kwargs.pop("service", "payments_portmone.service.PortmoneService")
        self.currency = kwargs.pop("currency", "UAH")
        self.portmone = import_string(service_path)(payee_id, login, password, self.endpoint, **kwargs)
        self.exp_time = kwargs.pop("exp_time", 120)
        self.prefix = kwargs.pop("prefix", "")

        super().__init__(**kwargs)

    def get_hidden_fields(self, payment) -> dict:
        """Converts a payment into a dict containing transaction data."""
        order_number = "{prefix}{number}".format(prefix=self.prefix, number=payment.pk)
        body_request = {
            "payee": {"payeeId": self.payee_id},
            "order": {
                "shopOrderNumber": order_number,
                "billAmount": str(payment.total),
                "billCurrency": "{currency}".format(currency=payment.currency or self.currency),
                "description": payment.description or "Payment order #{number}".format(number=order_number),
                "successUrl": "{url}".format(url=self.get_return_url(payment)),
                "failureUrl": "{url}".format(url=self.get_return_url(payment)),
                "preauthFlag": "Y" if getattr(payment, "is_preauth", True) else "N",
                "expTime": self.exp_time,
                "encoding": "UTF-8",
            },
            "payer": {"lang": get_language()},
        }

        return {"bodyRequest": json.dumps(body_request), "typeRequest": "json"}

    def get_form(self, payment, data=None):
        """Converts *payment* into a form suitable for Django templates."""
        return PaymentForm(data=self.get_hidden_fields(payment), action=self.endpoint, method=self._method)

    def process_data(self, payment, request):
        """Process callback request from a payment provider."""
        form = PortmoneResponseForm(request.POST)
        if form.is_valid():
            bill_id = form.cleaned_data["SHOPBILLID"]
            portmone_payment: PortmonePayment = self.portmone.get_payment_by_shop_bill_id(bill_id=bill_id)
            if portmone_payment:
                new_status = portmone_payment.payment_status
                payment.transaction_id = portmone_payment.shopBillId
                if new_status == PaymentStatus.PREAUTH:
                    payment.captured_amount = portmone_payment.billAmount
                payment.extra_data = {"token": portmone_payment.token}
                payment.change_status(new_status)
                if portmone_payment.is_paid:
                    return redirect(payment.get_success_url())
        else:
            payment.change_status(PaymentStatus.ERROR, message=form.cleaned_data["RESULT"])

        return redirect(payment.get_failure_url())
