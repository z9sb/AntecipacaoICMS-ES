import sqlite3
from os import path
# Conectar-se ao banco de dados (ou criar um novo se não existir)

conn = sqlite3.connect('dados.db')
cursor = conn.cursor()

try:
    if not path.exists('dados.bd'):
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
                            DataEmissao DATE,
                            ValorTotal DECIMAL,
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

except:
    pass


def cadastrar_empresas(cnpj, nome):
    cursor.execute("SELECT ID FROM Empresas WHERE CNPJ = ?", (cnpj,))
    empresa_id = cursor.fetchone()
    
    if empresa_id:
        return empresa_id[0]
    else:
        cursor.execute("INSERT INTO Empresas (CNPJ, Nome) VALUES(?, ?)", (cnpj, nome))
        return cursor.lastrowid

def cadastrar_nota(EmpresaID, Chave, DataEmissao, ValorTotal):
    cursor.execute("SELECT ID FROM NotasFiscais WHERE Chave = ?", (Chave,))
    chave_id = cursor.fetchone()
    
    if chave_id:
        return chave_id[0]
    else:
        cursor.execute(
            "INSERT INTO NotasFiscais (EmpresaID, Chave, DataEmissao, ValorTotal) VALUES(?, ?, ?, ?)", (
            EmpresaID, Chave, DataEmissao, ValorTotal))
        return cursor.lastrowid

def cadastrar_itens(NotaDIscalID, NomeProduto, NCM, CEST, AliICMS, ValorPro, ValorIPI, 
            ValorFrete, ValorOutras, ValorDesconto, ValorBC, ValorICMSDes,ValorImposto):
    
    cursor.execute("SELECT ID FROM Itens WHERE NomeProduto = ?", (NomeProduto,))
    item_id = cursor.fetchone()
    
    if item_id:
        return item_id[0]
    
    else:
        cursor.execute(
            "INSERT INTO Itens (NotaFiscalID, NomeProduto, NCM, CEST, AliICMS, ValorPro, ValorIPI, ValorFrete, ValorOutras, ValorDesconto, ValorBC, ValorICMSDes, ValorImposto) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (NotaDIscalID, NomeProduto, NCM, CEST, AliICMS, ValorPro,
            ValorIPI, ValorFrete, ValorOutras, ValorDesconto, ValorBC, ValorICMSDes, ValorImposto)
        )
    
    return conn.commit()