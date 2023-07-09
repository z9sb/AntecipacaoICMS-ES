from bs4 import BeautifulSoup as bs

class xmlns:
    def __init__(self, file: str):
        self._file = bs(open(file), 'xml')
    
    def __len__(self):
        return len(self._file)

    
class NF(xmlns):
    def __init__(self, file):
        super().__init__(file)
        
    def xml_find(self, item):
        xml_file = self._file.find(item)
        assert xml_file is not None 
        return xml_file if xml_file else None
    
    def xml_find_all(self, item):
        xml_file = self._file.find_all(item)
        assert xml_file is not None 
        return [i.text for i in xml_file] if xml_file else None
    
    def xml_find_all_subitem_int(self, item, subitem):
        lista = []
        xml_file = self._file.find_all(item)
        for i in xml_file:
            if i.find(subitem):
                lista.append(i.find(subitem).text)
            else:
                lista.append(0.00)
        assert xml_file is not None
        return lista
    
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
    
    def cnpj_dest(self) -> int: 
        return self.xml_find('dest').find('CNPJ').text
    
    def acess_key(self) -> int: 
        return self.xml_find('chNFe')
    
    def ncm(self) -> int: 
        return self.xml_find_all('NCM')
    
    def ali_icms(self) -> int: 
        return self.xml_find_all('pICMS')
    
    def csosn(self) -> int: 
        return self.xml_find_all('CSOSN')

    def name_prod(self) -> str:
        return self.xml_find_all('xProd')
    
    def cest(self) -> int:
        return self.xml_find_all('CEST')
    
    def v_ipi(self) -> int:
        return self.xml_find_all_subitem_int('IPI', 'vIPI')
    
    def v_prod(self) -> float:
        return self.xml_find_all('vProd')
    
    
