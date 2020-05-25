from datetime import date
from typing import Dict, Generator, List, Union

from belvo.enums import AccessMode
from belvo.http import APISession
from belvo.utils import read_file_to_b64


class Resource:
    endpoint: str

    def __init__(self, session: APISession) -> None:
        self._session = session

    @property
    def session(self) -> APISession:
        return self._session

    def list(self, **kwargs) -> Generator:
        endpoint = self.endpoint
        return self.session.list(endpoint, params=kwargs)

    def get(self, id: str, **kwargs) -> Dict:
        return self.session.get(self.endpoint, id, params=kwargs)

    def delete(self, id: str) -> bool:
        return self.session.delete(self.endpoint, id)

    def resume(
        self, session: str, token: str, *, link: str = None, raise_exception: bool = False, **kwargs
    ) -> Union[List[Dict], Dict]:

        data = {"session": session, "token": token}

        if link is not None:
            data.update(link=link)

        return self.session.patch(
            self.endpoint, data=data, raise_exception=raise_exception, **kwargs
        )


class Links(Resource):
    endpoint = "/api/links/"

    def create(
        self,
        institution: str,
        username: str,
        password: str,
        *,
        token: str = None,
        encryption_key: str = None,
        save_data: bool = True,
        raise_exception: bool = False,
        access_mode: AccessMode = None,
        username_type: str = None,
        certificate: str = None,
        private_key: str = None,
    ) -> Union[List[Dict], Dict]:

        if access_mode is None:
            access_mode = AccessMode.SINGLE

        data = {
            "institution": institution,
            "username": username,
            "password": password,
            "save_data": save_data,
            "access_mode": access_mode.value,
        }

        if token:
            data.update(token=token)

        if encryption_key:
            data.update(encryption_key=encryption_key)

        if username_type:
            data.update(username_type=username_type)

        if certificate:
            data.update(certificate=read_file_to_b64(certificate))

        if private_key:
            data.update(private_key=read_file_to_b64(private_key))

        return self.session.post(self.endpoint, data=data, raise_exception=raise_exception)

    def update(
        self,
        link: str,
        *,
        password: str = None,
        password2: str = None,
        token: str = None,
        encryption_key: str = None,
        save_data: bool = True,
        raise_exception: bool = False,
        username_type: str = None,
        certificate: str = None,
        private_key: str = None,
    ) -> Union[List[Dict], Dict]:

        data = {"password": password, "save_data": save_data}

        if password:
            data.update(password=password)

        if password2:
            data.update(password2=password2)

        if token:
            data.update(token=token)

        if encryption_key:
            data.update(encryption_key=encryption_key)

        if username_type:
            data.update(username_type=username_type)

        if certificate:
            data.update(certificate=read_file_to_b64(certificate))

        if private_key:
            data.update(private_key=read_file_to_b64(private_key))

        return self.session.put(self.endpoint, id=link, data=data, raise_exception=raise_exception)


class Accounts(Resource):
    endpoint = "/api/accounts/"

    def create(
        self,
        link: str,
        *,
        token: str = None,
        encryption_key: str = None,
        save_data: bool = True,
        raise_exception: bool = False,
        **kwargs: str,
    ) -> Union[List[Dict], Dict]:

        data = {"link": link, "save_data": save_data}

        if token:
            data.update(token=token)
        if encryption_key:
            data.update(encryption_key=encryption_key)

        return self.session.post(
            self.endpoint, data=data, raise_exception=raise_exception, **kwargs
        )


class Transactions(Resource):
    endpoint = "/api/transactions/"

    def create(
        self,
        link: str,
        date_from: str,
        *,
        date_to: str = None,
        account: str = None,
        token: str = None,
        encryption_key: str = None,
        save_data: bool = True,
        raise_exception: bool = False,
        **kwargs: str,
    ) -> Union[List[Dict], Dict]:

        if date_to is None:
            date_to = date.today().isoformat()

        data = {"link": link, "date_from": date_from, "date_to": date_to, "save_data": save_data}

        if account:
            data.update(account=account)
        if token:
            data.update(token=token)
        if encryption_key:
            data.update(encryption_key=encryption_key)

        return self.session.post(
            self.endpoint, data=data, raise_exception=raise_exception, **kwargs
        )


class Balances(Resource):
    endpoint = "/api/balances/"

    def create(
        self,
        link: str,
        date_from: str,
        *,
        date_to: str = None,
        account: str = None,
        token: str = None,
        encryption_key: str = None,
        save_data: bool = True,
        raise_exception: bool = False,
        **kwargs: str,
    ) -> Union[List[Dict], Dict]:

        if date_to is None:
            date_to = date.today().isoformat()

        data = {"link": link, "date_from": date_from, "date_to": date_to, "save_data": save_data}

        if account:
            data.update(account=account)
        if token:
            data.update(token=token)
        if encryption_key:
            data.update(encryption_key=encryption_key)

        return self.session.post(
            self.endpoint, data=data, raise_exception=raise_exception, **kwargs
        )


class Institutions(Resource):
    endpoint = "/api/institutions/"

    def delete(self, id: str) -> bool:
        raise NotImplementedError()

    def resume(
        self,
        session: str,
        token: str,
        *,
        link: str = None,
        raise_exception: bool = False,
        **kwargs: str,
    ) -> Dict:
        raise NotImplementedError()


class Owners(Resource):
    endpoint = "/api/owners/"

    def create(
        self,
        link: str,
        *,
        token: str = None,
        encryption_key: str = None,
        save_data: bool = True,
        raise_exception: bool = False,
        **kwargs: str,
    ) -> Union[List[Dict], Dict]:

        data = {"link": link, "save_data": save_data}

        if token:
            data.update(token=token)
        if encryption_key:
            data.update(encryption_key=encryption_key)

        return self.session.post(
            self.endpoint, data=data, raise_exception=raise_exception, **kwargs
        )


class Invoices(Resource):
    endpoint = "/api/invoices/"

    def create(
        self,
        link: str,
        date_from: str,
        date_to: str,
        type_: str,
        *,
        attach_xml: bool = False,
        encryption_key: str = None,
        save_data: bool = True,
        raise_exception: bool = False,
        **kwargs: str,
    ) -> Union[List[Dict], Dict]:

        data = {
            "link": link,
            "date_from": date_from,
            "date_to": date_to,
            "type": type_,
            "attach_xml": attach_xml,
            "save_data": save_data,
        }

        if encryption_key:
            data.update(encryption_key=encryption_key)

        return self.session.post(
            self.endpoint, data=data, raise_exception=raise_exception, **kwargs
        )

    def resume(
        self,
        session: str,
        token: str,
        *,
        link: str = None,
        raise_exception: bool = False,
        **kwargs: str,
    ) -> Dict:
        raise NotImplementedError()


class TaxReturns(Resource):
    endpoint = "/api/tax-returns/"

    def create(
        self,
        link: str,
        year_from: str,
        year_to: str,
        *,
        attach_pdf: bool = False,
        encryption_key: str = None,
        save_data: bool = True,
        raise_exception: bool = False,
        **kwargs: str,
    ) -> Union[List[Dict], Dict]:

        if year_to is None:
            year_to = date.today().year

        data = {
            "link": link,
            "year_from": year_from,
            "year_to": year_to,
            "attach_pdf": attach_pdf,
            "save_data": save_data,
        }

        if encryption_key:
            data.update(encryption_key=encryption_key)

        return self.session.post(
            self.endpoint, data=data, raise_exception=raise_exception, **kwargs
        )

    def resume(
        self,
        session: str,
        token: str,
        *,
        link: str = None,
        raise_exception: bool = False,
        **kwargs: str,
    ) -> Dict:
        raise NotImplementedError()


class TaxStatus(Resource):
    endpoint = "/api/tax-status/"

    def create(
        self,
        link: str,
        *,
        attach_pdf: bool = False,
        encryption_key: str = None,
        save_data: bool = True,
        raise_exception: bool = False,
        **kwargs: str,
    ) -> Union[List[Dict], Dict]:

        data = {"link": link, "attach_pdf": attach_pdf, "save_data": save_data}

        if encryption_key:
            data.update(encryption_key=encryption_key)

        return self.session.post(
            self.endpoint, data=data, raise_exception=raise_exception, **kwargs
        )

    def resume(
        self,
        session: str,
        token: str,
        *,
        link: str = None,
        raise_exception: bool = False,
        **kwargs: str,
    ) -> Dict:
        raise NotImplementedError()


class Statements(Resource):
    endpoint = "/api/statements/"

    def create(
        self,
        link: str,
        account: str,
        year: str,
        month: str,
        *,
        attach_pdf: bool = False,
        encryption_key: str = None,
        save_data: bool = True,
        raise_exception: bool = False,
        **kwargs: str,
    ) -> Union[List[Dict], Dict]:

        data = {
            "link": link,
            "account": account,
            "year": year,
            "month": month,
            "attach_pdf": attach_pdf,
            "save_data": save_data,
        }

        if encryption_key:
            data.update(encryption_key=encryption_key)

        return self.session.post(
            self.endpoint, data=data, raise_exception=raise_exception, **kwargs
        )

    def resume(
        self,
        session: str,
        token: str,
        *,
        link: str = None,
        account: str = None,
        raise_exception: bool = False,
        **kwargs,
    ) -> Union[List[Dict], Dict]:

        data = {"session": session, "token": token}

        if link is not None:
            data.update(link=link)

        if account is not None:
            data.update(account=account)

        return self.session.patch(
            self.endpoint, data=data, raise_exception=raise_exception, **kwargs
        )


class WidgetToken(Resource):
    endpoint = "/api/token/"

    def create(self, *, raise_exception: bool = False):
        data = {
            "id": self.session._secret_key_id,
            "password": self.session._secret_key_password,
            "scopes": "read_institutions,write_links,read_links,delete_links",
        }
        return self.session.post(self.endpoint, data=data, raise_exception=raise_exception)
