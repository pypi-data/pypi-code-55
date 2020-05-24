from zeep import Client

class Correios(object):

    PAC = '04510'
    SEDEX = '04014'
    SEDEX_12 = '04782'
    SEDEX_10 = '04790'
    SEDEX_HOJE = '04804'

    def frete(self, nCdEmpresa='', sDsSenha='', nCdServico, sCepOrigem, sCepDestino, nVlPeso, nCdFormato,
              nVlComprimento, nVlAltura, nVlLargura , nVlDiametro, sCdMaoPropria='N',
              nVlValorDeclarado='0', sCdAvisoRecebimento='N'):

        base_url = "http://ws.correios.com.br/calculador/CalcPrecoPrazo.asmx?wsdl"

        fields = {
            'nCdEmpresa': nCdEmpresa,
            'sDsSenha': sDsSenha,
            'nCdServico': nCdServico,
            'sCepOrigem': sCepOrigem,
            'sCepDestino': sCepDestino,
            'nVlPeso': nVlPeso,
            'nCdFormato': nCdFormato,
            'nVlComprimento': nVlComprimento,
            'nVlAltura': nVlAltura,
            'nVlLargura': nVlLargura ,
            'nVlDiametro': nVlDiametro,
            'sCdMaoPropria': sCdMaoPropria,
            'nVlValorDeclarado': nVlValorDeclarado,
            'sCdAvisoRecebimento': sCdAvisoRecebimento,
        }

        cl = Client(base_url)
        return cl.service.CalcPrecoPrazo(**fields)