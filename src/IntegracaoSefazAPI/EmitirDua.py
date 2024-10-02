import requests
import xml.etree.ElementTree as ET

def emitiDuaSefaz(cnpj: int, dataCompetencia: str,
                  dataVencimento: str, dataPagamento: str,
                  valorReceita: float, codServ: int,
                  codigoMunicipio: int, complemteno: str = None,
                  TipoAmb: int = 1, certificado: str = None,
                  chave: str = None):

    if TipoAmb == 1:
        url = "https://app.sefaz.es.gov.br/WsDua/DuaService.asmx"
    elif TipoAmb == 2:
        url = 'https://homologacao.sefaz.es.gov.br/WsDua/DuaService.asmx'

    payload = f"""<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope
        xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
        xmlns:duae="http://www.sefaz.es.gov.br/duae">
        <soap:Header>
            <duae:DuaServiceHeader>
                <duae:versao>1.01</duae:versao>
            </duae:DuaServiceHeader>
        </soap:Header>
        <soap:Body>
            <duae:duaEmissao>
                <duae:duaDadosMsg>
                    <emisDua
                        versao="1.01"
                        xmlns="http://www.sefaz.es.gov.br/duae">
                        <tpAmb>{TipoAmb}</tpAmb>
                        <cnpjEmi>27080571000130</cnpjEmi>
                        <cnpjOrg>27080571000130</cnpjOrg>
                        <cArea>5</cArea>
                        <cServ>{codServ}</cServ>
                        <cnpjPes>{cnpj}</cnpjPes>
                        <dRef>{dataCompetencia}</dRef>
                        <dVen>{dataVencimento}</dVen>
                        <dPag>{dataPagamento}</dPag>
                        <cMun>{codigoMunicipio}</cMun>
                        <xInf>{complemteno}</xInf>
                        <vRec>{valorReceita}</vRec>
                        <xIde>NFe XYZ</xIde>
                        <fPix>true</fPix>
                    </emisDua>
                </duae:duaDadosMsg>
            </duae:duaEmissao>
        </soap:Body>
    </soap:Envelope>"""

    headers = {
        'Content-Type': 'application/soap+xml'
    }

    cert = (certificado, chave) if certificado and chave else None

    # Enviando a requisição
    response = requests.post(url, headers=headers, data=payload, cert=cert)

    # Exibindo a resposta bruta
    print(response.text)

    # Analisando a resposta XML
    if response.status_code == 200:
        try:
            root = ET.fromstring(response.text)
            # Definindo o namespace
            namespace = {'soap': 'http://www.w3.org/2003/05/soap-envelope',
                         'duae': 'http://www.sefaz.es.gov.br/duae'}

            # Extraindo o número do DUA
            n_dua = root.find('.//duae:nDua', namespaces=namespace)

            if n_dua is not None:
                return f"{n_dua.text}"
            else:
                print("Número do DUA não encontrado.")
        except ET.ParseError as e:
            print(f"Erro ao analisar o XML: {e}")
    else:
        print(f"Erro na requisição: {response.status_code} - {response.text}")

