import asyncio
import json
import os

from rabbit.client import AioRabbitClient
from rabbit.exchange import Exchange
from rabbit.publish import Publish
from rabbit.queue import Queue

PAYOAD = {
    "documento": 752617293,
    "descricao": "-",
    "enquadramentos": {
        "analise": [8, 9, 10, 11, 12, 13, 14, 15],
        "conferencia": [10, 11, 12],
        "aprovacao": [],
    },
    "paginas": [
        [
            'JUSTIÇA ELEITORAL\nTRIBUNAL REGIONAL ELEITORAL / DF\nAVISO\n\nEm cumprimento ao que dispõe o art. 33º e seus 88 1º e 2º da Lei nº 9.504/97, assim como o\nart. 8º da Resolução TSE nº 23.549/2017, comunicamos, para ciência dos interessados, que a\nempresa IBOPE INTELIGENCIA PESQUISA E CONSULTORIA LTDA encaminhou à Justiça\nEleitoral os dados referentes à pesquisa eleitoral das eleições Eleições Gerais 2018,\nprotocolizada sob o nº DF-08518/2018, contratada por IBOPE INTELIGENCIA PESQUISA E\nCONSULTORIA LTDA e registrada no sistema de registro de pesquisas eleitorais em\n01/10/2018.\nDados e informações registradas (conteúdos de responsabilidade de quem registra a pesquisa,\nnão aferidos pela Justiça Eleitoral no ato de registro):\n* Empresa contratada Eleição + Cargos + Abrangência (UF/Município) «Valor da pesquisa\n* Estatístico Responsável + Registro do estatístico no CONRE + Nº de entrevistados + Plano amostral\n* Datas de início e término + Metodologia de\n* Sistema interno de controle e verificação, conferência e fiscalização da coleta de dados e do trabalho\n* Questionário completo aplicado ou a ser aplicado em formato PDF\n* Dados relativos aos municípios e bairros abrangidos pela pesquisa / área em que foi realizada a\n\nAviso gerado às 23:07:10 de 01/10/2018.\nResolução TSE nº 23.549/2017:\n"Art. 7º Efetivado ou alterado o registro, será emitido recibo eletrônico que conterá:\n| - resumo das informações; e\nIl - número de identificação da pesquisa."\nA autenticidade deste aviso poderá ser confirmada na página do Tribunal Superior Eleitoral na\nInternet, no endereço http://www .tse.jus.br, por meio do código 4E24.6D1D.2888.C5FO.\n\nDocumento assinado digitalmente conforme MP nº 2.200-2/2001 de 24/08/2001. O documento pode ser acessado pelo endereço\nhttp:/Anww ..stf.jus.br/portal/autenticacao/autenticarDocumento.asp sob o código\n'
        ]
    ],
    "usuario": "rodrigo.barreiros",
}


class Producer:
    def __init__(self, loop=None, client=None, qtd=1):
        self.loop = loop or asyncio.get_event_loop()
        self.client = client or AioRabbitClient()
        self.qtd = qtd
        self.loop.run_until_complete(self.client.connect())

    def configure_publish(self):
        publish = Publish(
            self.client,
            exchange=Exchange(
                # name=os.getenv("SUBSCRIBE_EXCHANGE", "default.in.exchange"),
                name=os.getenv("SUBSCRIBE_EXCHANGE", "texto.extraido"),
                exchange_type=os.getenv("SUBSCRIBE_EXCHANGE_TYPE", "topic"),
                topic=os.getenv("SUBSCRIBE_TOPIC", "#"),
            ),
            queue=Queue(name=os.getenv("SUBSCRIBE_QUEUE", "default.subscribe.queue")),
        )
        self.loop.run_until_complete(publish.configure())
        return publish

    def send_event(self):
        publish = self.configure_publish()
        for i in range(0, self.qtd):
            self.loop.run_until_complete(
                publish.send_event(
                    bytes(json.dumps(PAYOAD), "utf-8")
                    # properties={'headers': {'x-delay': 5000}}
                )
            )
