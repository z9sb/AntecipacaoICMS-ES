import requests


def ConsultarDua(num_DUA, tipo_amb, CNPJ, certificado, chave):
    if tipo_amb == 1:
        url = "https://app.sefaz.es.gov.br/WsDua/DuaService.asmx"
    elif tipo_amb == 2:
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
            <duae:duaConsulta>
                <duae:duaDadosMsg>
                    <consDua versao="1.01"
xmlns="http://www.sefaz.es.gov.br/duae">
                        <tpAmb>{tipo_amb}</tpAmb>
                        <nDua>{num_DUA}</nDua>
                        <cnpj>{CNPJ}</cnpj>
                    </consDua>
                </duae:duaDadosMsg>
            </duae:duaConsulta>
        </soap:Body>
    </soap:Envelope>"""

    headers = {
        'Content-Type': 'text/xml; charset=utf-8'
    }
    cert = (certificado, chave) if certificado and chave else None
    response = requests.post(url, headers=headers, data=payload, cert=cert)

    print(response.text)
