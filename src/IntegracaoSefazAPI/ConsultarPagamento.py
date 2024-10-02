import requests
import os


def ConsultarPagamento(dt_inicio, dt_final, CNPJ, cert_path, key_path):
    url = "https://app.sefaz.es.gov.br/WsDua/DuaService.asmx"

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
        <duae:duaPagos>
            <duae:duaPagoDadosMsg>
                <consDuaPago
 versao="1.01"
 xmlns="http://www.sefaz.es.gov.br/duae">
                    <tpAmb>1</tpAmb>
                    <indComp>0</indComp>
                    <cnpj>{CNPJ}</cnpj>
                    <dInicio>{dt_inicio}</dInicio>
                    <dFinal>{dt_final}</dFinal>
                </consDuaPago>
            </duae:duaPagoDadosMsg>
        </duae:duaPagos>
    </soap:Body>
</soap:Envelope>"""

    headers = {
        'Content-Type': 'text/xml; charset=utf-8'
    }

    cert = (cert_path, key_path)

    response = requests.post(
        url, headers=headers, data=payload, cert=cert, verify=True
    )

    print(response.text)


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cert = os.path.abspath(
        os.path.join(script_dir, r'..\..\certificado\cert.pem'))
    key = os.path.abspath(
        os.path.join(script_dir, r'..\..\certificado\key.pem'))
    ConsultarPagamento(
        '2024-08-15', '2024-08-20', '39389523000107',
        cert, key)
