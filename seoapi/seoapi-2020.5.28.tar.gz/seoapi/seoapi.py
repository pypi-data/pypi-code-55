# -*- coding: utf-8 -*-
import hashlib
import json
import logging
import uuid

import requests

from .exceptions import *


class Api:
    def __init__(self, token, base_url):
        self.base_url = base_url
        self.token = token

    def _process_response(self, response, params, data):
        logging.debug(f"{response.status_code} {response.reason}")

        if response.status_code == 400:
            error = response.json().get("error")

            if error == "session wasn't added":
                raise SessionDuplicateError(response)
            elif error == "session does not exist":
                raise SessionNotExistError(response)

            raise RequestError(response)

        elif response.status_code == 401:
            raise AuthError(response)
        elif 402 <= response.status_code < 500:
            raise ApiError(response)
        elif response.status_code == 500:
            raise ServerError(response)
        elif response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"{response.status_code} {response.reason}")

    def _request(self, method, resource, params=None, **data):
        end_point = f"{self.base_url}{resource}"
        headers = {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json",
        }
        request_params = {
            "headers": headers,
            "data": json.dumps(data),
            "params": params,
        }
        response = requests.request(method, end_point, **request_params)

        return self._process_response(response, params, data)


class SeoApi:
    YANDEX = "yandex"
    GOOGLE = "google"
    WORDSTAT = "wordstat"

    def __init__(self, source, token, base_url, logging_level=logging.INFO):
        self.source = source
        self._api = Api(token, base_url)
        logging.basicConfig(level=logging_level)

    def load_tasks(self, config):
        """
        http://docs.seoapi.ru/#3

        :param config: dict :
        Описание параметров для Yandex & Google
            source:	string : Источник парсинга, yandex|google
            session_id:	string : Уникальный идентификатор сессии, любое текстовое значение (можно uuid4)
            priority: integer : Приоритет для сессии. Может принимать значение от 1 до 10. В настоящий момент опция не работает
            numdoc:	integer : Кол-во результатов на одной странице выдачи
            total_pages: integer : Кол-во страниц выдачи
            queries: list : Либо список слов, либо список списков (id запроса, запрос), либо словарь
            domain:	string : yandex.ru	домен источника. Например, yandex.ru
            is_mobile: integer : мобильная выдача, принимает 1 или 0
            region:	integer : Без региона	внутренний id региона
            params: dict : словарь с параметрами url для поисковой системы, например: {“noreask”: “1”}
            queries:
                query: string : Поисковый запрос
                query_id: string : id запроса из вашей системы (если необходим)
                total_pages: integer : Кол-во страниц выдачи
                numdoc:	integer : глубина выдачи (кол-во результатов на 1 страницу)
                region:	integer : id региона (из нашей системы)

            {
                "session_id": "some-session-id",
                "source": "google",
                "total_pages": 1,
                "numdoc": 100,
                "region": 29112,
                "is_mobile": 0,
                "domain": "google.ru",
                "queries": [
                    {"query_id": 1, "query": "запрос 1", region: 1011969},
                    {"query_id": 2, "query": "запрос 2", region: 29112}
                ]
            }
        :return: dict :
        {
          "status": "OK",
          "session_id": "9bbe1184-3d9c-40f5-9654-3dbd7e4bde13",
          "query_ids": []
        }

        ===========================================

        :param config: dict :
        Описание параметров для wordstat
            source:	string : wordstat
            session_id:	string : Уникальный идентификатор сессии, любое текстовое значение (можно uuid4)
            queries: list : Либо список слов, либо список списков (id запроса, запрос), либо словарь
            device: str : 'desktop', 'mobile', 'phone', 'tablet', все(пустая строка)
            region:	integer : Без региона	внутренний id региона
            page: integer : номер страницы вордстат для парсинга
            params: dict : {"lr": 213}
            queries:
                query: string : Поисковый запрос
                query_id: string : id запроса из вашей системы (если необходим)
                device: string :
                page: integer :
                region: integer :

            {
              "session_id": "111111111-1111-1111-1111-111111111111",
              "region": 213,
              "page": 2,
              "queries": [
                  {"query_id": 2, "query": "...", "device": "desktop", "region": 1, "page": 1},
                  {"query_id": 3, "query": "...", "device": "desktop", "region": 1, "page": 1},
              ],
              "source": "wordstat",
              "params": {"lr": 213}
            }

        """
        if config["source"] != self.source:
            raise Exception(
                f"В инициализированном классе source={self.source}, "
                f"а в конфиге источник {config['source']}."
            )
        resource = f"{self.source}/load_tasks/"
        result = self._api._request("post", resource, **config)
        return result

    def get_session_status(self, session_id):
        """
        http://docs.seoapi.ru/#o

        Возможные статусы сессии:
            - queued - сессия поставлена в очередь, но съем по ней еще не начался.
            - pending - происходит сбор сессии.
            - finished - сессия завершена (возможно забрать результаты).

        :param source: str : yandex|google
        :param session_id: str : Идентификатор сессии, который вы послали при загрузки задач
        :return:
        {
            "done": 101000,
            "finished_at": "2017-06-06T13:55:36",
            "progress": "100.0",
            "started_at": "2017-06-06T10:53:03",
            "status": "finished",
            "total": 101000
        }
        """
        resource = f"{self.source}/session/{session_id}/"
        result = self._api._request("GET", resource)
        return result

    def is_finish_session(self, session_id):
        status = self.get_session_status(session_id)["status"]
        if status == "finished":
            return True
        return False

    def get_results(self, session_id, **params):
        """
        http://docs.seoapi.ru/#o-y

        :param session_id: str : Идентификатор сессии, который вы послали при загрузки задач
        :param params: dict : GET параметры
        :return:
        {
          "total": 2,
          "results": [
            {
              "query": "grim dawn",
              "created_at": "2017-08-04T09:55:22.701000",
              "count_results": 1060000,
              "organic": [
                {
                  "title": "<b>Grim Dawn</b> on Steam",
                  "url": "http://store.steampowered.com/app/219990/Grim_Dawn/",
                  "snippet": "Community Hub. <b>Grim Dawn</b>.",
                  "position": 1,
                  "page": 1,
                  "domain": "store.steampowered.com",
                  "cached_url": "..."
                },
              ]
            },
            ...
          ],
        }

        ========================
        Для Wordstat

        :return:
        {
          "total": 20000,
          "results": [
            {
              "query_id": 6582,
              "query": "what should i do",
              "parsed_at": 1506606697.409974,
              "ws_type": "base",
              "count": 13066,
              "region": 213,
              "device": "",
              "update_date": "18.09.2017",
              "source": "wordstat",
              "including_phrases": [{ "number" : "13066", "phrase" : "what should i do" }, ...],
              "related_phrases": [{ "number" : "13066", "phrase" : "what should i do" }, ...],
            },
            {
              "query_id": 6564,
               "parsed_at": 1506606697.409974
              "query": "What is the point of this",
              "count": 167,
              "region": 213
              "device": "",
              "update_date": "18.09.2017",
              "source": "wordstat",
              "including_phrases": [{ "number" : "167", "phrase" : "What is the point of this"}, ...],
              "related_phrases": [{ "number" : "167", "phrase" : "What is the point of this" }, ...],
            },
            ...
          ]
        }

        """
        resource = f"{self.source}/results/{session_id}/"
        result = self._api._request("GET", resource, params=params)
        return result

    def get_results_by_limit(self, session_id, limit_in_request=100):
        """
        Запрашивает данные пачками, размер указывается в limit_in_request

        :param source: str : yandex|google
        :param session_id: str : Идентификатор сессии, который вы послали при загрузки задач
        :param limit_in_request: кол-во скачиваемых фраз в одном запросе
        :return:
        [
            {
              "query": "grim dawn",
              "created_at": "2017-08-04T09:55:22.701000",
              "count_results": 1060000,
              "organic": [
                {
                  "title": "<b>Grim Dawn</b> on Steam",
                  "url": "http://store.steampowered.com/app/219990/Grim_Dawn/",
                  "snippet": "Community Hub. <b>Grim Dawn</b>.",
                  "position": 1,
                  "page": 1,
                  "domain": "store.steampowered.com",
                  "cached_url": "..."
                },
              ]
            },
            ...
        ]
        """
        offset = 0
        total = 1
        results = []
        while offset < total:
            r = self.get_results(session_id, limit=limit_in_request, offset=offset)
            total = r["total"]
            results += r["results"]
            offset += limit_in_request
        return results

    def get_report(self, **params):
        """
        Статистика запросов к API

        :param source: str : yandex|google
        :param report_type: str : today|month|all|daily : Тип отчета
        :param params: year=2018&month=2 : Параметры доступны для отчета типа daily
        :return:
        {
            "query_count": 5327882,
            "session_count": 1247
        }
        """
        resource = f"{self.source}/user/report/daily/"
        result = self._api._request("GET", resource, params=params)
        return result

    def get_regions(self, **params):
        """
        http://docs.seoapi.ru/#e-o

        :param source: str : yandex|google
        :param params: dict : q - Поиск по региону, можно задавать часть имени региона
        :return:
        [
          {
            "region_id": 1011969,
            "name_ru": "Москва,Москва,Россия",
            "name": "Moscow,Moscow,Russia"
          },
        ]
        """
        resource = f"{self.source}/regions/"
        result = self._api._request("GET", resource, params=params)
        return result


class Serp(SeoApi):
    YANDEX = "yandex"
    GOOGLE = "google"

    def __init__(self, source, token, base_url):
        super().__init__(source=source, token=token, base_url=base_url)

    def generate_sessions_id_and_queries_ids(
        self, search_phrases, session_size, suffix=""
    ):
        new_data = []
        offset = 0
        limit = len(search_phrases)
        while offset < limit:
            sample = search_phrases[offset : offset + session_size]
            queries = [
                {"query": q, "query_id": uuid.uuid4().hex} for q in sample
            ]
            s = "".join(sample)
            s = f"{suffix}{s}"
            s = s.encode("utf8")
            session_id = hashlib.sha256(s).hexdigest()
            new_data.append({"session_id": session_id, "queries": queries})
            offset += session_size
        return new_data

    def generate_config_sessions(
        self,
        search_phrases,
        regions,
        is_mobile,
        count_results,
        domains=["ru"],
        suffix="",
        session_size=2000,
    ):
        """
        Формирует конфиги тасков для заказа в seoapi.

        :param search_phrases: list : фразы
        :param regions: list : ид регионов в которых будут сниматься позиции
        :param is_mobile: list : тип устройств в которых будут сниматься позиции
        :param count_results: int : кол-во результатов в выдачи
        :param domains: list : домены регионального поиска
        :param suffix: str : строка подставляемая при формирование хеша ид сессии
        :param session_size: int : кол-во фраз в одной сесии
        :return: list
        """
        sessions = []
        for domain in domains:
            for is_mobile_ in is_mobile:
                for region in regions:
                    suffix = f"{suffix}{is_mobile}{region}{count_results}{self.source}"
                    # Фразы расфасовываются по мелким пачкам, к которым
                    # присваивается идентификатор.
                    sessions_params_list = self.generate_sessions_id_and_queries_ids(
                        search_phrases, session_size=session_size, suffix=suffix
                    )
                    for session_params in sessions_params_list:
                        d = {
                            "total_pages": 1,
                            "region": region,
                            "source": self.source,
                            "numdoc": count_results,
                            "is_mobile": is_mobile_,
                            "domain": f"{self.source}.{domain}",
                            "session_id": session_params["session_id"],
                            "queries": session_params["queries"],
                        }
                        sessions.append(d)
        return sessions


class Wordstat(Serp):
    def __init__(self, token, base_url):
        super().__init__(source=Serp.WORDSTAT, token=token, base_url=base_url)

    def generate_config_sessions(
        self,
        search_phrases,
        pages,
        regions,
        devices,
        searchs_params=None,
        suffix="",
        session_size=2000,
    ):
        """
        Формирует конфиги тасков для заказа в seoapi.

        :param search_phrases: list : фразы
        :param pages: list : номера страниц wordstat, в которых собрать данные
        :param regions: list
        :param devices: list
        :param searchs_params: list : параметры, наверно которые подставляются в url страницы при парсинге
        :param suffix: str : строка подставляемая при формирование хеша ид сессии
        :param session_size: int : кол-во фраз в одной сесии
        :return: list
        """
        sessions = []
        for search_params in searchs_params or [{}]:
            for device in devices:
                for page in pages:
                    for region in regions:
                        suffix = f"{suffix}{page}{region}{search_params}{device}"
                        # Фразы расфасовываются по мелким пачкам, к которым
                        # присваивается идентификатор.
                        sessions_params_list = self.generate_sessions_id_and_queries_ids(
                            search_phrases, session_size=session_size, suffix=suffix
                        )
                        for session_params in sessions_params_list:
                            d = {
                                "session_id": session_params["session_id"],
                                "region": region,
                                "page": page,
                                "device": device,
                                "queries": session_params["queries"],
                                "source": SeoApi.WORDSTAT,
                            }
                            if search_params:
                                d["params"] = search_params
                            sessions.append(d)
        return sessions
