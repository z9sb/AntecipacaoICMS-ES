import requests
import xml.etree.ElementTree as ET
import base64


class DuaEletronico:
    def __init__(self, cnpj, tipo_amb=1, certificado=None, chavestr=None):
        self.cnpj = cnpj
        self.tipo_amb = tipo_amb
        self.certificado = certificado
        self.chavestr = chavestr
        if self.tipo_amb == 1:
            self.url = "https://app.sefaz.es.gov.br/WsDua/DuaService.asmx"
        elif self.tipo_amb == 2:
            self.url = 'https://homologacao.sefaz.es.gov.br/WsDua/DuaService.asmx'

    def emitiDuaSefaz(self, dataCompetencia: str,
                      dataVencimento: str, dataPagamento: str,
                      valorReceita: float, codServ: int,
                      codigoMunicipio: int, complemteno: str = None,
                      ):

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
                            <tpAmb>{self.tipo_amb}</tpAmb>
                            <cnpjEmi>27080571000130</cnpjEmi>
                            <cnpjOrg>27080571000130</cnpjOrg>
                            <cArea>5</cArea>
                            <cServ>{codServ}</cServ>
                            <cnpjPes>{self.cnpj}</cnpjPes>
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

        cert = (self.certificado,
                self.chave) if self.certificado and self.chave else None

        # Enviando a requisição
        response = requests.post(
            self.url, headers=headers, data=payload, cert=cert)

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
            print(f"""Erro na requisição: {
                  response.status_code} - {response.text}""")

    def ConsultarPagamento(self, dt_inicio, dt_final):
        url = "https://app.sefaz.es.gov.br/WsDua/DuaService.asmx"

        payload = f"""
            <?xml version="1.0" encoding="utf-8"?>
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
                                <cnpj>{self.cnpj}</cnpj>
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

        cert = (self.certificado, self.chavestr)

        response = requests.post(
            url, headers=headers, data=payload, cert=cert, verify=True
        )

        print(response.text)

    def ObterPDF(self, num_DUA):
        payload = f"""
            <?xml version="1.0" encoding="utf-8"?>
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
                                <tpAmb>{self.tipo_amb}</tpAmb>
                                <nDua>{num_DUA}</nDua>
                                <cnpj>{self.cnpj}</cnpj>
                            </obterPdfDua>
                        </duae:duaDadosMsg>
                    </duae:duaObterPdf>
                </soap:Body>
            </soap:Envelope>
        """

        headers = {
            'Content-Type': 'text/xml; charset=utf-8'
        }

        cert = (self.certificado,
                self.chavestr) if self.certificado and self.chavestr else None
        response = requests.post(
            self.url, headers=headers, data=payload, cert=cert)

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
            print(f"""Erro na requisição: {
                  response.status_code} - {response.text}""")

    def ConsultarDua(self, num_DUA):
        payload = f"""
            <?xml version="1.0" encoding="utf-8"?>
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
                                    <tpAmb>{self.tipo_amb}</tpAmb>
                                    <nDua>{num_DUA}</nDua>
                                    <cnpj>{self.cnpj}</cnpj>
                                </consDua>
                            </duae:duaDadosMsg>
                        </duae:duaConsulta>
                    </soap:Body>
                </soap:Envelope>
            """

        headers = {
            'Content-Type': 'text/xml; charset=utf-8'
        }
        cert = (self.certificado,
                self.chavestr) if self.certificado and self.chavestr else None
        response = requests.post(
            self.url, headers=headers, data=payload, cert=cert)

        print(response.text)
