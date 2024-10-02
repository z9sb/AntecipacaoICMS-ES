import requests
import base64
import xml.etree.ElementTree as ET

def ObterPDF(num_DUA, tipo_amb, CNPJ, certificado, chave):

    if tipo_amb == 1:
        url = "https://app.sefaz.es.gov.br/WsDua/DuaService.asmx"
    elif tipo_amb == 2:
        url = 'https://homologacao.sefaz.es.gov.br/WsDua/DuaService.asmx'
    else:
        raise ValueError("tipo_amb deve ser 1 ou 2.")
    
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
        <duae:duaObterPdf>
            <duae:duaDadosMsg>
                <obterPdfDua versao="1.01" xmlns="http://www.sefaz.es.gov.br/duae">
                    <tpAmb>{tipo_amb}</tpAmb>
                    <nDua>{num_DUA}</nDua>
                    <cnpj>{CNPJ}</cnpj>
                </obterPdfDua>
            </duae:duaDadosMsg>
        </duae:duaObterPdf>
    </soap:Body>
</soap:Envelope>"""

    headers = {
        'Content-Type': 'text/xml; charset=utf-8'
    }

    cert = (certificado, chave) if certificado and chave else None
    response = requests.post(url, headers=headers, data=payload, cert=cert)

    if response.status_code == 200:
        root = ET.fromstring(response.content)
        namespaces = {'ns': 'http://www.sefaz.es.gov.br/duae'}
        xpdf_element = root.find('.//ns:xPdf', namespaces)

        if xpdf_element is not None:
            pdf_data = base64.b64decode(xpdf_element.text)

            with open(f"DUA_{num_DUA}.pdf", "wb") as pdf_file:
                pdf_file.write(pdf_data)
            print(f"PDF salvo com sucesso como DUA_{num_DUA}.pdf")
        else:
            print("Tag <xPdf> não encontrada na resposta.")
    else:
        print(f"Erro na requisição: {response.status_code} - {response.text}")