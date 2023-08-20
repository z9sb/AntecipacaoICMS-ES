from bs4 import BeautifulSoup as bs
from funcoes import aliquota

class xmlns:
    def __init__(self, file: str):
        self._file = bs(open(file, encoding='UTF-8'), 'xml')

class NF(xmlns):
    def __init__(self, file):
        super().__init__(file)
    
    #Busca o primeiro item informado no xml
    def xml_find(self, item):
        xml_file = self._file.find(item)
        return xml_file if xml_file else None
    
    #Busca o todos itens informados no xml
    def xml_find_all(self, item):
        xml_file = self._file.find_all(item)
        return [i.text for i in xml_file] if xml_file else None
    
    #Busca todos os subitens informados e retorna uma lista zerada caso não o tenha
    def xml_find_all_subitem_int(self, item, subitem, add = 0):
        lista = []
        xml_file = self._file.find_all(item)
        for i in xml_file:
            if i.find(subitem):
                lista.append(i.find(subitem).text)
            else:
                lista.append(add)
        return lista if lista != [] else [0 for i in  self.ncm()]
    
    #Retorna o itens das NF's sendo suportados os modelos (NF: 55, NFCE: 65)
    def model(self) -> str: 
        return self.xml_find('mod').text
    
    def serie(self) -> str: 
        return self.xml_find('serie').text
    
    def number_nf(self) -> str: 
        return self.xml_find('nNF').text
    
    def date_emition(self) -> str: 
        return self.xml_find('dhEmi').text
    
    def cnpj_emit(self) -> int: 
        return self.xml_find('emit').find('CNPJ').text

    def uf_emit(self) -> str: 
        return self.xml_find('emit').find('UF').text
        
    def cnpj_dest(self) -> int: 
        return self.xml_find('dest').find('CNPJ').text
    
    def name_for(self) -> str:
        return self.xml_find('emit').find('xNome').text
    
    def estado_for(self) -> str:
        return self.xml_find('emit').find('UF').text
    
    def name_cli(self) -> str:
        return self.xml_find('dest').find('xNome').text
    
    def estado_cli(self) -> str:
        return self.xml_find('dest').find('UF').text
    
    def acess_key(self) -> int: 
        return self.xml_find('chNFe').text
    
    def ncm(self) -> int: 
        return self.xml_find_all('NCM')
    
    def ali_icms(self) -> int: 
        return self.xml_find_all_subitem_int('ICMS', 'pICMS', aliquota(self.uf_emit()))
    
    def csosn(self) -> int: 
        return self.xml_find_all('CSOSN')

    def name_prod(self) -> str:
        return self.xml_find_all('xProd')
    
    def cest(self) -> int:
        return self.xml_find_all_subitem_int('prod','CEST')
    
    def v_ipi(self) -> int:
        return self.xml_find_all_subitem_int('IPI', 'vIPI')
    
    def v_prod(self) -> float:
        return self.xml_find_all('vProd')
    
    def v_frete(self) -> float:
        return self.xml_find_all_subitem_int('prod','vFrete')
    
    def v_desc(self) -> float:
        return self.xml_find_all_subitem_int('prod','vDesc')
    
    def v_outros(self) -> float:
        return self.xml_find_all_subitem_int('prod','vOutro')
    
    def Valor_total(self) -> float:
        return self.xml_find('ICMSTot').find('vNF').text