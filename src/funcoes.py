from string import punctuation
from pandas import read_excel
import bd as bd
from datetime import datetime
from os import getlogin, path
from IntegracaoSefazAPI.EmitirDua import emitiDuaSefaz
from dateutil.relativedelta import relativedelta
from IntegracaoSefazAPI.ObterPDF import ObterPDF

# Retorna a aliquota interestadual para o estado do ES

script_dir = path.dirname(path.abspath(__file__))
cert = path.abspath(
    path.join(script_dir, r'..\certificado\cert.pem'))
key = path.abspath(
    path.join(script_dir, r'..\certificado\key.pem'))


def aliquota(uf: str) -> float:
    dicionario = {
        'AC': 12.00, 'AL': 12.00, 'AM': 12.00, 'AP': 12.00,
        'BA': 12.00, 'CE': 12.00, 'DF': 12.00,
        'GO': 12.00, 'MA': 12.00, 'MT': 12.00, 'MS': 12.00,
        'MG': 7.00, 'PA': 12.00, 'PB': 12.00,
        'PR': 12.00, 'PE': 7.00, 'PI': 12.00, 'RN': 12.00,
        'RS': 7.00,  'RJ': 7.00, 'RO': 12.00,
        'RR': 12.00, 'SC': 7.00, 'SP': 7.00, 'SE': 12.00,
        'TO': 12.00, 'IM': 4.00, 'ES': 17.00
    }
    return dicionario[uf]

# Extrai a coluna informada no arquivo codigos


def file_search_xlsx(colum):
    extraction = read_excel('data\\codigos.xlsx')[colum]
    comparation = (
        [str(i).translate(str.maketrans
                          ('', '', punctuation
                           )) for i in extraction if str(i) != 'nan'])
    return comparation

# Compara o NCM e CEST informados, com o que estão no arquivo


def comparation_ncm(ncm, cest, name_prod):
    if [ncm for i in file_search_xlsx('NCM/SH') if int(i) == int(
            ncm[:len(str(i))])]:
        if cest == 0.0 or cest == '0000000':
            print(name_prod)
            cest_invalido = input(
                'O produto não tem CEST definido, calcular somente pelo ncm?\n'
                'Para não calcular pressione <N>').lower()
            if cest_invalido == 'n':
                return False
            else:
                return True
        else:
            return cest in file_search_xlsx('CEST')

    elif cest == file_search_xlsx('CEST')[-1]:
        return True

# Calcula o valor do imposto e o retorna


def calculo_antecipação_icms(
    cests, alis, ncms, name_prods, v_produtos, v_ipis, v_fretes, v_descs,
    v_outros, cnpj, nome, chave_nf, data_hora, Valor_total, NumeroNF, SerieNF,
    NomeFornecedor
):
    DataOperacao = datetime.now()

    v_impoto = 0
    for cest, ali, ncm, name_prod, v_produto, v_ipi, v_frete, v_desc, v_outro in zip(
            cests, alis, ncms, name_prods, v_produtos, v_ipis, v_fretes, v_descs, v_outros):

        if comparation_ncm(ncm, cest, name_prod):
            print(name_prod)
            base_de_calculo_ipi = (
                float(v_produto) + float(v_ipi) +
                float(v_frete) + float(v_outro) - float(v_desc)
            ) * 0.17
            base_desconto_icms = (
                float(v_produto) - float(v_desc)) * (float(ali)/100)
            v_impoto += base_de_calculo_ipi - base_desconto_icms

            bd.cadastrar_itens(
                bd.cadastrar_nota(bd.cadastrar_empresas(
                    cnpj, nome), chave_nf, NumeroNF, SerieNF, NomeFornecedor,
                    data_hora, Valor_total, 0, DataOperacao, 'Null', getlogin()),
                name_prod, ncm, cest, ali, v_produto, float(v_ipi), v_frete,
                v_outro, v_desc, base_de_calculo_ipi, base_desconto_icms,
                (base_de_calculo_ipi-base_desconto_icms)
            )
    bd.atualizar_imposto_notas(round(v_impoto, 2), chave_nf)
    competencia = f"{DataOperacao.year}-{DataOperacao.month:02d}"
    conferencia = input('Empresa do Simples Nacional? S Sim ou N Não ').lower()
    if conferencia == 's':
        nova_data_e_hora = data_hora + relativedelta(months=2)
        data_formatada = nova_data_e_hora.strftime('%Y-%m-10')
    elif conferencia == 'n':
        data_formatada = DataOperacao.strftime('%Y-%m-%d')

    N_DUA = emitiDuaSefaz(
        cnpj, competencia, data_formatada, data_formatada, round(v_impoto, 2),
        '3220', '56154', f'NF N {NumeroNF} {NomeFornecedor}', 2, cert, key
    )
    bd.atualizar_N_DUA(N_DUA, chave_nf)
    pdf = ObterPDF(N_DUA, 2, cnpj, cert, key)

    return v_impoto
