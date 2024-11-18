from src.xml_parser.xml_parser import ParseXML
from src.utils.load_xlsx import FileSearchXlsx
from src.xml_parser.ali_interestaduais import AliInterestaduais
from colorama import Fore, init
from locale import setlocale, LC_ALL, currency


class Antecipacao:
    def __init__(self, path_xml):
        """
        Parameters
        ----------
        path_xml : str
            Caminho do arquivo xml da nota fiscal

        Attributes
        ----------
        xml : ParseXML
            Inst ncia da classe ParseXML
        _produtos : list
            Lista de produtos da nota fiscal
        file_search : FileSearchXlsx
            Inst ncia da classe FileSearchXlsx
        v_total_imposto : float
            Valor total do imposto
        """
        self.xml = ParseXML(path_xml)
        self._produtos = self.xml.get_prod()
        self.file_search = FileSearchXlsx()
        self.v_total_imposto = 0
        init(autoreset=True)
        setlocale(LC_ALL, 'pt_BR.UTF-8')

    def product_verification(self):
        """
        Verifica se o produto tem aliquota interestadual e efetua o cálculo
        do imposto.

        Returns
        -------
        float
            Valor total do imposto.
        """
        for self.product in self._produtos:
            self.get_attributes_comparation()
            if self.verification():
                print(f'{Fore.GREEN}{self.product.prod.xProd}{Fore.RESET}')
                self.get_attributes_calculo()
                self.v_total_imposto += self.calculate_tax()
            else:
                print(f'{Fore.RED}{self.product.prod.xProd}{Fore.RESET}')
        print(f"""{Fore.BLUE}Total imposto: {
              currency(self.v_total_imposto, grouping=True)}{Fore.RESET}""")
        return round(self.v_total_imposto, 2)

    def get_attributes_comparation(self):
        self.ncm = self.product.prod.NCM
        self.cest = self.product.prod.CEST

    def get_attributes_calculo(self):
        self.icms = self.get_icms()
        self.ali_icms = float(self.icms.pICMS)
        self.v_icms = float(self.icms.vICMS)
        self.v_produto = float(self.product.prod.vProd)
        self.uf_origem = self.xml.get_emit().enderEmit.UF.value
        self.uf_destino = self.xml.get_dest().enderDest.UF.value
        self.v_outro = float(
            self.product.prod.vOutro) if self.product.prod.vOutro else 0.00
        self.v_desc = float(
            self.product.prod.vDesc) if self.product.prod.vDesc else 0.00
        self.v_frete = float(
            self.product.prod.vFrete) if self.product.prod.vFrete else 0.00
        self.v_ipi = float(
            self.product.imposto.IPI.IPITrib.vIPI) if hasattr(
                self.product.imposto.IPI.IPITrib, 'vIPI') and self.product.imposto.IPI.IPITrib.vIPI is not None else 0.00

    def get_icms(self) -> float:
        icms = self.product.imposto.ICMS
        for icms_type in icms.__dict__.values():
            if icms_type:
                return icms_type

        return None

    def comparation_ncm(self):
        ncm_list = self.file_search.get_column('NCM/SH')
        return any(str(self.ncm).startswith(str(i).replace('.', '')) for i in ncm_list)

    def comparation_cest(self):
        cest_list = self.file_search.get_column('CEST')
        return any(str(self.cest).startswith(str(i).replace('.', '')) for i in cest_list)

    def verification(self):
        if self.comparation_cest():
            return True

        elif self.comparation_ncm():
            cest_invalido = input(
                'O produto n o tem CEST definido, calcular somente pelo ncm?\n'
                'Para n o calcular pressione <N>').lower()
            if cest_invalido == 'n':
                return False
            else:
                return True

    def calculate_tax(self):
        base_de_calculo = (
            self.v_produto + self.v_ipi + self.v_frete + self.v_outro - self.v_desc
        )
        v_total_imposto = base_de_calculo * 0.17

        if self.ali_icms == 4.00:
            base_desc_icms = (self.v_produto - self.v_desc + self.v_outras)
            v_desc_icms = base_desc_icms * (self.ali_icms / 100)

        else:
            ali_interestaduais = AliInterestaduais(
                self.uf_origem, self.uf_destino)
            aliquota = ali_interestaduais.aliquotas_interestaduais()
            base_desc_icms = (self.v_produto - self.v_desc + self.v_outro)
            v_desc_icms = base_desc_icms * (aliquota / 100)

        v_impoto = v_total_imposto - v_desc_icms

        return v_impoto


if __name__ == '__main__':
    # xml = Antecipacao(r'C:\Users\raysl_3a68bgu\Downloads\35240958939141000154550000001233641240430425.xml')
    # xml = Antecipacao(r"C:\Users\raysl_3a68bgu\Downloads\41241004200198000108550010009133721501237830.xml")
    xml = Antecipacao(
        r"C:\Users\raysl_3a68bgu\Downloads\41241004290323000118550040002797491023615386.xml")
    xml.product_verification()
