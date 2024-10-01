import requests


def emitiDuaSefaz(url: str, cnpj: int, dataCompetencia: str,
                  dataVencimento: str, dataPagamento: str,
                  valorReceita: float,  codServ: int,
                  codigoMunicipio: int, complemteno: str = None,
                  tipoEmissao: int = 1, ):
    url = "https://app.sefaz.es.gov.br/WsDua/DuaService.asmx"

    payload = f"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<soap:Envelope\n    xmlns:soap=\"http://www.w3.org/2003/05/soap-envelope\"\n    xmlns:duae=\"http://www.sefaz.es.gov.br/duae\">\n    <soap:Header>\n        <duae:DuaServiceHeader>\n            <duae:versao>1.01</duae:versao>\n        </duae:DuaServiceHeader>\n    </soap:Header>\n    <soap:Body>\n        <duae:duaEmissao>\n            <duae:duaDadosMsg>\n                <emisDua\n                    versao=\"1.01\"\n                    xmlns=\"http://www.sefaz.es.gov.br/duae\">\n                    <tpAmb>{tipoEmissao}</tpAmb>\n                    <cnpjEmi>27080571000130</cnpjEmi>\n                    <cnpjOrg>27080571000130</cnpjOrg>\n                    <cArea>5</cArea>\n                    <cServ>{codServ}</cServ>\n                    <cnpjPes>{cnpj}</cnpjPes>\n                    <dRef>{dataCompetencia}</dRef>\n                    <dVen>{dataVencimento}</dVen>\n                    <dPag>{dataPagamento}</dPag>\n                    <cMun>{codigoMunicipio}</cMun>\n                    <xInf>{complemteno}</xInf>\n                    <vRec>{valorReceita}</vRec>\n                    <xIde>NFe XYZ</xIde>\n                    <fPix>true</fPix>\n                </emisDua>\n            </duae:duaDadosMsg>\n        </duae:duaEmissao>\n    </soap:Body>\n</soap:Envelope>"
    headers = {
        'Content-Type': 'application/soap+xml'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
