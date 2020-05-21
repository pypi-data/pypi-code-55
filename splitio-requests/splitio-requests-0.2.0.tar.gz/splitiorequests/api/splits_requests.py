import logging
from typing import Optional, Dict, Tuple, NoReturn, Union
from urllib3.util.retry import Retry
from requests import Session, Response
from requests.exceptions import ConnectionError
import jsonpatch
from splitiorequests.api.api_requests import APIRequests
from splitiorequests.common.http_adapter import TimeoutHTTPAdapter

log = logging.getLogger('splitiorequests')


class SplitsRequests(APIRequests):
    def __init__(
            self,
            token: str,
            hostname: Optional[str] = None,
            headers: Optional[Dict[str, str]] = None
    ) -> None:
        super().__init__(token, hostname, headers)
        self.__session = self._requests_retry_session()

    def _requests_retry_session(
            self,
            retries: int = 10,
            backoff_factor: float = 0.3,
            status_forcelist: Tuple[int, ...] = (429, 500, 502, 503, 504),
            session: Optional[Session] = None
    ) -> Session:
        session = session or Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
            method_whitelist=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "PATCH", "POST"]
        )
        adapter = TimeoutHTTPAdapter(max_retries=retry)
        session.mount('https://', adapter)
        return session

    def __request_success(self, request: Response, request_success_code: int) -> bool:
        if request.status_code == request_success_code:
            return True
        else:
            log.error(f"Status code: {request.status_code}. "
                      f"Message:{request.json()}")
            return False

    def get_split(self, split_name: str, wsid: str) -> Optional[dict]:
        try:
            split = self.__session.get(f'{self._hostname}/splits/ws/{wsid}/{split_name}',
                                       headers=self._headers)
        except ConnectionError as error:
            log.exception(error)
            return None

        return split.json() if self.__request_success(split, 200) else None

    def create_split(self, traffic_type_id_or_name: str, wsid: str, payload: dict) -> bool:
        try:
            create = self.__session.post(
                f'{self._hostname}/splits/ws/{wsid}/trafficTypes/{traffic_type_id_or_name}',
                headers=self._headers, json=payload)
        except ConnectionError as error:
            log.exception(error)
            return False

        return True if self.__request_success(create, 200) else False

    def delete_split(self, split_name: str, wsid: str) -> bool:
        try:
            delete = self.__session.delete(f'{self._hostname}/splits/ws/{wsid}/{split_name}', headers=self._headers)
        except ConnectionError as error:
            log.exception(error)
            return False

        return True if self.__request_success(delete, 200) else False

    def create_split_definition_in_environment(
            self,
            split_name: str,
            wsid: str,
            environment_name: str,
            payload: dict
    ) -> bool:
        try:
            create = self.__session.post(f'{self._hostname}/splits/ws/{wsid}/{split_name}/environments/'
                                         f'{environment_name}', headers=self._headers, json=payload)
        except ConnectionError as error:
            log.exception(error)
            return False

        return True if self.__request_success(create, 200) else False

    def get_split_definition_in_environment(
            self,
            split_name: str,
            wsid: str,
            environment_name: str
    ) -> Optional[dict]:
        try:
            split_definition = self.__session.get(
                f'{self._hostname}/splits/ws/{wsid}/{split_name}/environments/{environment_name}',
                headers=self._headers
            )
        except ConnectionError as error:
            log.exception(error)
            return None

        return split_definition.json() if self.__request_success(split_definition, 200) else None

    def partial_update_split_definition_in_environment(
            self,
            split_name: str,
            wsid: str,
            environment_name: str,
            old_data: Optional[dict] = None,
            new_data: Optional[dict] = None,
            patch_string: Optional[str] = None
    ) -> Union[NoReturn, bool]:
        patch_data = None
        if old_data and new_data:
            patch_data = jsonpatch.make_patch(old_data, new_data).to_string()
        elif not patch_string:
            log.warning("Provide data for patch")
            raise TypeError

        try:
            split_definition = self.__session.patch(
                f'{self._hostname}/splits/ws/{wsid}/{split_name}/environments/'
                f'{environment_name}', headers=self._headers,
                data=patch_string or patch_data)
        except ConnectionError as error:
            log.exception(error)
            return False

        return True if self.__request_success(split_definition, 200) else False

    def remove_split_definition(self, split_name: str, wsid: str, environment_name: str) -> bool:
        try:
            remove_split = self.__session.delete(f'{self._hostname}/splits/ws/{wsid}/{split_name}/environments/'
                                                 f'{environment_name}', headers=self._headers)
        except ConnectionError as error:
            log.exception(error)
            return False

        return True if self.__request_success(remove_split, 200) else False

    def list_split_definitions(
            self,
            wsid: str,
            environment_name: str,
            offset: int = 0,
            limit: int = 50
    ):
        try:
            split_definitions = self.__session.get(
                f'{self._hostname}/splits/ws/{wsid}/environments/{environment_name}?limit={limit}&offset={offset}',
                headers=self._headers)
        except ConnectionError as error:
            log.exception(error)
            yield None
            return

        splits_definitions_payload = split_definitions.json()

        yield splits_definitions_payload if self.__request_success(split_definitions, 200) else None

        if splits_definitions_payload['totalCount'] > 50 or \
                (splits_definitions_payload['limit'] + splits_definitions_payload['offset'] - 1) < \
                splits_definitions_payload['totalCount']:
            while True:
                offset += limit
                try:
                    splits = self.__session.get(f'{self._hostname}/splits/ws/{wsid}?limit={limit}&offset={offset}',
                                                headers=self._headers)
                except ConnectionError as error:
                    log.exception(error)
                    yield None
                    return

                splits_definitions_payload = splits.json()

                yield splits_definitions_payload if self.__request_success(splits, 200) else None

                if splits_definitions_payload['limit'] + splits_definitions_payload['offset'] > \
                        splits_definitions_payload['totalCount']:
                    break

    def list_splits(
            self,
            wsid: str,
            offset: int = 0,
            limit: int = 50
    ):
        try:
            splits = self.__session.get(f'{self._hostname}/splits/ws/{wsid}?limit={limit}&offset={offset}',
                                        headers=self._headers)
        except ConnectionError as error:
            log.exception(error)
            yield None
            return

        splits_payload = splits.json()

        yield splits_payload if self.__request_success(splits, 200) else None

        if splits_payload['totalCount'] > 50 or \
                (splits_payload['limit'] + splits_payload['offset'] - 1) < splits_payload['totalCount']:
            while True:
                offset += limit
                try:
                    splits = self.__session.get(f'{self._hostname}/splits/ws/{wsid}?limit={limit}&offset={offset}',
                                                headers=self._headers)
                except ConnectionError as error:
                    log.exception(error)
                    yield None
                    return

                splits_payload = splits.json()

                yield splits_payload if self.__request_success(splits, 200) else None

                if splits_payload['limit'] + splits_payload['offset'] > splits_payload['totalCount']:
                    break

    def update_split_description(self, split_name: str, wsid: str, description: str) -> bool:
        try:
            update_description = self.__session.put(
                f'{self._hostname}/splits/ws/{wsid}/{split_name}/updateDescription',
                headers=self._headers, data=description
            )
        except ConnectionError as error:
            log.exception(error)
            return False

        return True if self.__request_success(update_description, 200) else False

    def full_update_split_definition_in_environment(
            self,
            split_name: str,
            wsid: str,
            environment_id_or_name: str,
            payload: dict
    ) -> bool:
        try:
            split_definition = self.__session.put(
                f'{self._hostname}/splits/ws/{wsid}/{split_name}/environments/{environment_id_or_name}',
                headers=self._headers,
                json=payload
            )
        except ConnectionError as error:
            log.exception(error)
            return False

        return True if self.__request_success(split_definition, 200) else False

    def kill_split_in_environment(
            self,
            split_name: str,
            wsid: str,
            environment_id_or_name: str,
            comment: Optional[str] = None
    ) -> bool:
        try:
            kill_split = self.__session.put(
                f'{self._hostname}/splits/ws/{wsid}/{split_name}/environments/{environment_id_or_name}/kill',
                headers=self._headers,
                json={"comment": f"{comment}"} if comment else None
            )
        except ConnectionError as error:
            log.exception(error)
            return False

        return True if self.__request_success(kill_split, 200) else False

    def restore_split_in_environment(
            self,
            split_name: str,
            wsid: str,
            environment_id_or_name: str,
            comment: Optional[str] = None
    ) -> bool:
        try:
            restore_split = self.__session.put(
                f'{self._hostname}/splits/ws/{wsid}/{split_name}/environments/{environment_id_or_name}/restore',
                headers=self._headers,
                json={"comment": f"{comment}"} if comment else None
            )
        except ConnectionError as error:
            log.exception(error)
            return False

        return True if self.__request_success(restore_split, 200) else False
