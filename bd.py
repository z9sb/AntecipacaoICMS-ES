import sqlite3
from os import path, getlogin
import pandas as pd
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
                            DataOperacao DATE,
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

def cadastrar_nota(EmpresaID, Chave, DataEmissao, ValorTotal, DataOperacao, Usuario):
    cursor.execute("SELECT ID FROM NotasFiscais WHERE Chave = ?", (Chave,))
    chave_id = cursor.fetchone()
    
    if chave_id:
        return chave_id[0]
    else:
        cursor.execute(
            "INSERT INTO NotasFiscais (EmpresaID, Chave, DataEmissao, ValorTotal, DataOperacao, Usuario) VALUES(?, ?, ?, ?, ?, ?)", (
            EmpresaID, Chave, DataEmissao, ValorTotal, DataOperacao, Usuario))
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

def localization_item(NomeProduto):  
    cursor.execute(
        "SELECT NomeProduto, NCM, CEST, AliICMS, ValorPro, ValorIPI, ValorFrete, ValorOutras, ValorDesconto, ValorBC, ValorICMSDes,NotaFiscalID  ValorImposto FROM Itens WHERE NomeProduto LIKE ?",
                   ('%' + NomeProduto + '%',))
    item_name = cursor.fetchall()
    
    if item_name:
        for item in item_name:
            with open(f'{localization_chave_id(item[-1])}.txt','a') as f:
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