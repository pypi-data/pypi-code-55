import abc
import datetime
import logging
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

import requests
from django.utils import timezone
from payments import PaymentError, PaymentStatus

logger = logging.getLogger("payments_portmone")


class StatusCodeError(PaymentError):
    """Raised when API returns non-200 status code."""


class GatewayError(PaymentError):
    """Raised when API http request failed."""


@dataclass
class PortmonePayment:
    """Represent information about Portmone payment."""

    status: str
    description: str
    pay_date: datetime.datetime
    pay_order_date: datetime.date
    payee_export_date: datetime.date
    shopBillId: str
    shopOrderNumber: str
    billAmount: Decimal
    attribute1: str
    attribute2: str
    attribute3: str
    attribute4: str
    attribute5: str = ""
    commission: Decimal = Decimal("0")
    payee_export_flag: str = ""
    chargeback: str = ""
    authCode: str = ""
    cardMask: str = ""
    token: str = ""
    gateType: str = ""
    errorCode: str = ""
    errorMessage: str = ""

    @property
    def payment_status(self) -> PaymentStatus:
        """Returns a PaymentStatus that matches Portmone status."""
        data = {
            "CREATED": PaymentStatus.WAITING,
            "PREAUTH": PaymentStatus.PREAUTH,
            "PAYED": PaymentStatus.CONFIRMED,
            "REJECTED": PaymentStatus.REJECTED,
        }
        return data.get(self.status, PaymentStatus.ERROR)

    @property
    def is_paid(self) -> bool:
        """Return True if payment paid or False."""
        return self.status in ("PAYED", "PREAUTH")  # noqa: WPS510


class BasePortmoneService(abc.ABC):
    """Base class that provides exchange methods with the Portmone API."""

    @abc.abstractmethod
    def get_payment_by_shop_bill_id(self, bill_id: str, **kwargs) -> Optional[PortmonePayment]:
        """Return Portmone payment information by shopBillId.

        Raises:
            NotImplementedError: Subclasses should implement this.
        """
        raise NotImplementedError

    @classmethod
    def _make_request(cls, url: str, payload: dict) -> dict:
        """Make request to API gateway.

        Raises:
            GatewayError: If no the API response.
            StatusCodeError: If the API response code is't 200.
        """
        try:
            response = requests.post(url, json=payload)
        except Exception as error:
            raise GatewayError from error

        if response.status_code != 200:
            raise StatusCodeError(code=response.status_code, message=response.content)

        return response.json()


class PortmoneService(BasePortmoneService):
    """Сlass provides exchange methods with the Portmone API https://docs.portmone.com.ua/docs/en/PaymentGatewayEng/."""

    def __init__(self, payee_id: str, login: str, password: str, endpoint: str):
        self.payee_id = payee_id
        self.login = login
        self.password = password
        self.endpoint = endpoint

    def get_payment_by_shop_bill_id(self, bill_id: str, bill_date: datetime.date = None) -> Optional[PortmonePayment]:
        """Return Portmone payment information by shopBillId.

        Raises:
            PaymentError: Portmone Payment build error
        """
        if bill_date is None:
            bill_date = timezone.now()
        bill_date = bill_date.strftime("%d.%m.%Y")
        payload = {
            "method": "result",
            "params": {
                "data": {
                    "login": self.login,
                    "password": self.password,
                    "payeeId": self.payee_id,
                    "shopbillId": bill_id,
                    "startDate": bill_date,
                    "endDate": bill_date,
                }
            },
            "id": "1",
        }
        result = self._make_request(self.endpoint, payload)
        if result:
            try:
                payment: dict = result[0]
            except IndexError:
                logger.error(f"Portmone payment {bill_id} is not found")
                return None
            try:
                return PortmonePayment(**payment)
            except Exception as error:
                raise PaymentError from error
        return None
