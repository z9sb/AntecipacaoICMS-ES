from nfelib.nfe.bindings.v4_0.proc_nfe_v4_00 import NfeProc


class ParseXML:
    def __init__(self, path_xml):
        self.xml = path_xml
        self._NF = NfeProc.from_path(self.xml)

    def get_ide(self):
        return self._NF.NFe.infNFe.ide

    def get_emit(self):
        return self._NF.NFe.infNFe.emit

    def get_dest(self):
        return self._NF.NFe.infNFe.dest

    def get_total(self):
        return self._NF.NFe.infNFe.total

    def get_prod(self):
        return self._NF.NFe.infNFe.det

    def get_transp(self):
        return self._NF.NFe.infNFe.transp

    def get_infAdic(self):
        return self._NF.NFe.infNFe.infAdic

    def get_infCpl(self):
        return self._NF.NFe.infNFe.infCpl

    def get_infProt(self):
        return self._NF.NFe.infNFe.infProt

if __name__ == '__main__':
    xml = ParseXML(r"C:\Users\raysl_3a68bgu\Downloads\35240958939141000154550000001233641240430425.xml")
    for i in xml.get_prod():
        print(i.prod)