import sqlite3
from os import path

caminho_db = r'data\dados.db'
# Conectar-se ao banco de dados (ou criar um novo se não existir)

if not path.exists(caminho_db):
    conn = sqlite3.connect(caminho_db)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE Empresas (
                    ID INTEGER PRIMARY KEY,
                    CNPJ TEXT,
                    Nome TEXT
                )''')

    # Criar tabela de notas fiscais
    cursor.execute('''CREATE TABLE NotasFiscais (
                        ID INTEGER PRIMARY KEY,
                        EmpresaID INTEGER,
                        Chave TEXT,
                        NumeroNF TEXT,
                        SerieNF TEXT,
                        NomeFornecedor TEXT,
                        DataEmissao DATE,
                        ValorTotal DECIMAL,
                        ValorImposto DECIMAL,
                        DataOperacao DATE,
                        N_DUA TEXT,
                        Usuario TEXT,
                        FOREIGN KEY (EmpresaID) REFERENCES Empresas(ID)
                    )''')

    # Criar tabela de itens de notas fiscais
    cursor.execute('''CREATE TABLE Itens (
                        ID INTEGER PRIMARY KEY,
                        NotaFiscalID INTEGER,
                        NomeProduto TEXT,
                        NCM TEXT,
                        CEST TEXT,
                        AliICMS DECIMAL,
                        ValorPro DECIMAL,
                        ValorIPI DECIMAL,
                        ValorFrete DECIMAL,
                        ValorOutras DECIMAL,
                        ValorDesconto DECIMAL,
                        ValorBC DECIMAL,
                        ValorICMSDes DECIMAL,
                        ValorImposto DECIMAL,
                        FOREIGN KEY (NotaFiscalID) REFERENCES NotasFiscais(ID)
                    )''')
conn = sqlite3.connect(caminho_db)
cursor = conn.cursor()


def cadastrar_empresas(cnpj, nome):
    cursor.execute("SELECT ID FROM Empresas WHERE CNPJ = ?", (cnpj,))
    empresa_id = cursor.fetchone()

    if empresa_id:
        return empresa_id[0]
    else:
        cursor.execute(
            "INSERT INTO Empresas (CNPJ, Nome) VALUES(?, ?)", (cnpj, nome))
        return cursor.lastrowid


def cadastrar_nota(EmpresaID, Chave, NumeroNF, SerieNF, NomeFornecedor,
                   DataEmissao, ValorTotal, ValorImposto, DataOperacao,
                   N_DUA, Usuario):
    try:
        cursor.execute("SELECT ID FROM NotasFiscais WHERE Chave = ?", (Chave,))
        chave_id = cursor.fetchone()

        if chave_id:
            return chave_id[0]  # Retorna o ID se a nota fiscal já existe.
        else:
            cursor.execute(
                "INSERT INTO NotasFiscais (EmpresaID, Chave, NumeroNF, SerieNF, "
                "NomeFornecedor, DataEmissao, ValorTotal, ValorImposto,"
                "DataOperacao, N_DUA, Usuario) "
                "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                    EmpresaID, Chave, NumeroNF, SerieNF, NomeFornecedor,
                    DataEmissao, ValorTotal, ValorImposto, DataOperacao,
                    N_DUA, Usuario
                ))
            conn.commit()  # Commit das alterações
            return cursor.lastrowid  # Retorna o ID da nova nota fiscal cadastrada.

    except Exception as e:
        print(f"Erro ao cadastrar nota: {e}")
        conn.rollback()
        return None


def cadastrar_itens(NotaDIscalID, NomeProduto, NCM, CEST, AliICMS, ValorPro,
                    ValorIPI, ValorFrete, ValorOutras, ValorDesconto,
                    ValorBC, ValorICMSDes, ValorImposto):

    cursor.execute(
        "SELECT ID FROM Itens WHERE NomeProduto = ?", (NomeProduto,))
    item_id = cursor.fetchone()

    if item_id:
        return item_id[0]

    else:
        cursor.execute(
            "INSERT INTO Itens (NotaFiscalID, NomeProduto, NCM, CEST, AliICMS, "
            "ValorPro, ValorIPI, ValorFrete, ValorOutras, ValorDesconto, ValorBC,"
            "ValorICMSDes, ValorImposto) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (NotaDIscalID, NomeProduto, NCM, CEST, AliICMS, ValorPro,
             ValorIPI, ValorFrete, ValorOutras, ValorDesconto, ValorBC,
             ValorICMSDes, ValorImposto)
        )

    return conn.commit()


def localization_chave(Chave):
    cursor.execute("SELECT Chave FROM NotasFiscais WHERE Chave LIKE ?",
                   ('%' + Chave + '%',))
    chave_text = cursor.fetchone()

    if chave_text:
        return print(chave_text[0])

    else:
        return print('A chave informada não se encontra cadastrada!')


def localization_chave_id(ID):
    cursor.execute("SELECT Chave FROM NotasFiscais WHERE ID = ?", (ID,))
    chave_id = cursor.fetchone()

    if chave_id:
        return chave_id[0]


def get_N_DUA(chave):
    numero = cursor.execute("SELECT N_DUA FROM NotasFiscais = ? WHERE Chave = ?", (
        chave))

    if numero:
        return numero[0]


def atualizar_N_DUA(N_DUA, chave):
    cursor.execute("UPDATE NotasFiscais SET N_DUA = ? WHERE Chave = ?", (
        N_DUA, chave))

    conn.commit()


def atualizar_imposto_notas(imposto, chave):
    cursor.execute("UPDATE NotasFiscais SET ValorImposto = ? WHERE Chave = ?", (
        imposto, chave))

    conn.commit()


def localization_item(NomeProduto):
    cursor.execute(
        "SELECT NomeProduto, NCM, CEST, AliICMS, ValorPro, ValorIPI, ValorFrete,"
        "ValorOutras, ValorDesconto, ValorBC, ValorICMSDes, ValorImposto, NotaFiscalID"
        "FROM Itens WHERE NomeProduto LIKE ?", ('%' + NomeProduto + '%',))
    item_name = cursor.fetchall()

    if item_name:
        for item in item_name:
            with open(f'{localization_chave_id(item[-1])}.txt', 'a') as f:
                f.writelines(f'{item[0]}; ')
                f.writelines(f'{item[1]}; ')
                f.writelines(f'{item[2]}; ')
                f.writelines(f'{item[3]}; ')
                f.writelines(f'{item[4]}; ')
                f.writelines(f'{item[5]}; ')
                f.writelines(f'{item[6]}; ')
                f.writelines(f'{item[7]}; ')
                f.writelines(f'{item[8]}; ')
                f.writelines(f'{item[9]}; ')
                f.writelines(f'{item[10]}; ')
                f.writelines(f'{item[11]}\n')
    else:
        print(f'O item informado "{NomeProduto}" não foi encontrado!')


if __name__ == '__main__':
    consulta = input(
        'Você deseja consultar uma NF ou algun item? 1 - para nota 2 - para item.\n')
    if consulta == '1':
        localization_chave(
            input('Digite a chave ou parte dela!\n')
        )
    elif consulta == '2':
        localization_item(
            input('Digite o item ou parte dele!\n')
        )
    else:
        print('Digite uma opção válida.')
