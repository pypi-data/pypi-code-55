from zeep import Client

class Correios(object):

    PAC = '04510'
    SEDEX = '04014'
    SEDEX_12 = '04782'
    SEDEX_10 = '04790'
    SEDEX_HOJE = '04804'

    def frete(self, cod, origem, destino, peso, formato,
              comprimento, altura, largura, diametro, mao_propria='N',
              valor_declarado='0', aviso_recebimento='N',
              empresa='', senha=''):

        base_url = "http://ws.correios.com.br/calculador/CalcPrecoPrazo.asmx?wsdl"

        fields = {
            'nCdEmpresa': empresa,
            'sDsSenha': senha,
            'nCdServico': cod,
            'sCepOrigem': origem,
            'sCepDestino': destino,
            'nVlPeso': peso,
            'nCdFormato': formato,
            'nVlComprimento': comprimento,
            'nVlAltura': altura,
            'nVlLargura': largura,
            'nVlDiametro': diametro,
            'sCdMaoPropria': mao_propria,
            'nVlValorDeclarado': valor_declarado,
            'sCdAvisoRecebimento': aviso_recebimento,
        }

        cl = Client(base_url)
        return cl.service.CalcPrecoPrazo(**fields)