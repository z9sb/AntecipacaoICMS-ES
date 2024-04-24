from pathlib import Path
from easygui import fileopenbox  # type: ignore
from funcoes import calculo_antecipação_icms
from modules.xml_file import NFe
from datetime import datetime
import time

root = Path(fileopenbox(default=r'C:\donwload\*.xml'))

if __name__ == '__main__':
    xml = NFe(root)
    cests = xml.cest()
    alis = xml.ali_icms()
    ncms = xml.ncm()
    name_prods = xml.name_prod()
    v_ipis = xml.v_ipi()
    v_produtos = xml.v_prod()
    v_fretes = xml.v_frete()
    v_descs = xml.v_desc()
    v_outros = xml.v_outros()
    cnpj_des = xml.cnpj_dest()
    n_nf = xml.number_nf()
    serie_nf = xml.serie()
    chave_nf = xml.acess_key()
    name_for = xml.name_for()
    nome_cli = xml.name_cli()
    estado_cli = xml.estado_cli()
    estado_for = xml.estado_for()
    data_e_hora_em_texto = xml.date_emition()
    data_e_hora = datetime.strptime(
        data_e_hora_em_texto, '%Y-%m-%dT%H:%M:%S%z')
    Valor_total = xml.Valor_total()

    if estado_cli == estado_for:
        pass

    else:
        ini = time.time()
        resultado = round(calculo_antecipação_icms(
            cests, alis, ncms, name_prods, v_produtos, v_ipis, v_fretes,
            v_descs, v_outros, cnpj_des, nome_cli, chave_nf, data_e_hora,
            Valor_total, n_nf, serie_nf, name_for
        ), 2)
        print(time.time()-ini)
        print(resultado)
