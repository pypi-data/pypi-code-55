from elasticsearch import Elasticsearch, TransportError, RequestsHttpConnection

from conf import conf
from taskmanager.log import logger

class MyConnection(RequestsHttpConnection):
    def __init__(self, *args, **kwargs):
        super(MyConnection, self).__init__(*args, **kwargs)
        if conf.index.proxy:
            self.session.proxies = {'http': conf.index.proxy}

class Es:

    def __init__(self, hosts):
        self._es_list = self._createEsList(hosts)

    def TEST__getAll(self, index, es_id=0):
        _es = self._es_list[es_id]
        return self._req(
            _es,
            'POST',
            f'{index}/_search',
            body={
                'query': {'match_all': {}},
                'size': 1000,
            })

    def deleteIndex(self, _index):
        try:
            for _es in self._es_list:
                self._req(_es, 'DELETE', _index)
        except TransportError as e:
            if e.status_code != 404:
                raise

    def _createEsList(self, hosts):
        es_list = list()
        for host in hosts:
            _es = Elasticsearch(
                host,
                connection_class=MyConnection,
                sniff_on_start=True,
                sniff_on_connection_fail=True,
                sniffer_timeout=60)
            es_list.append(_es)
        return es_list

    def perform_request(self, method, path, **kwargs):
        for _es in self._es_list:
            res = self._req(_es, method, path, **kwargs)
            if res.get('errors'):
                return res
        return res

    def createIndex(self, _index, CREATE_BODY):
        try:
            for _es in self._es_list:
                logger.debug('put: %s', CREATE_BODY)
                self._req(_es,'PUT', _index, body=CREATE_BODY, params={'request_timeout': 60})
        except TransportError as e:
            if e.status_code != 400:
                raise
        for i in range(len(self._es_list)):
            _es = self._es_list[i]
            res = _es.indices.get_alias(index=_index)
            logger.info('check index succ. index=%s, alias=%s, es_id=%d', _index, res, i)

    def _req(self, es, method, path, **kwargs):
        return es.transport.perform_request(method, f'/{path}', **kwargs)

    def index(self, index, _id, body):
        for _es in self._es_list:
            _es.index(index=index, id=_id, body=body)

    def getDoc(self, index, _id, es_id=0):
        _es = self._es_list[es_id]
        return _es.get(index=index, id=_id)

    def refresh(self, *args):
        for i in range(len(self._es_list)):
            _es = self._es_list[i]
            for arg in args:
                _es.indices.refresh(index=arg)
                logger.debug('refresh index finish. index=%s, es_id=%d', arg, i)

    def getDocNumbers(self, idx_name):
        doc_nums = []
        for _es in self._es_list:
            num = _es.indices.stats(index=idx_name)['_all']['primaries']['docs']['count']
            doc_nums.append(num)
        return doc_nums

    def changeIndex(self, alias_name, index_name):
        for _es in self._es_list:
            # if alias exists, remove it first to avoid multiple same aliases
            actions = []
            if _es.indices.exists_alias(alias_name):
                previous_index_name = list(_es.indices.get(alias_name).keys())[0]
                actions.append({"remove": {"index": previous_index_name, "alias": alias_name}})
            actions.append({"add": {"index": index_name, "alias": alias_name}})
            _es.indices.update_aliases(body={'actions':actions})

    def getAllIndex(self, es_id = 0):
        _es = self._es_list[es_id]
        return _es.indices.get_alias()

    def existsIndexAllHosts(self, index):
        for _es in self._es_list:
            if not _es.indices.exists(index=index):
                return False
        return True

    def existsIndexNoHosts(self, index):
        for _es in self._es_list:
            if _es.indices.exists(index=index):
                return False
        return True

    def existsAlias(self, index, alias):
        for _es in self._es_list:
            if _es.indices.exists_alias(index=index, name=alias):
                return True
        return False

    # FIXME 不要在全量任务中进行索引更新
    def updateDoc(self, index, doc_id, body):
        for _es in self._es_list:
            _es.update(index, id=doc_id, body=body)
