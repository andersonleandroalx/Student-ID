import pandas as pd
import mysql.connector
import numpy as np

banco2 = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="db_1"
)

# escolher a tabela
tabela = pd.read_excel(r"C:\Imports\alunos-carteirinhas.xlsx")

# ajustar os campos que serão listados
for i, aluno in enumerate(tabela["cod"]):
    #data = tabela.loc[i, "data"]
    lote = tabela.loc[i, "lote"]
    nome = tabela.loc[i, "nome"]
    ra1 = tabela.loc[i, "ra"]
    tipo = tabela.loc[i, "tipo"]
    categoria = tabela.loc[i, "categoria"]
    print(lote, nome, ra1, tipo, categoria)

    ra_int = ra1.item() # converte numpy em int
    print(type(ra_int)) # checa conversão
    nome = nome.strip()
    tipo = tipo.strip()
    categoria = categoria.strip()

# escolher qual insert será usado
    cursor = banco2.cursor()
    comando = ("insert into teste_excel (data_1, nome, ra, tipo, categoria) values (now(),'"+nome+"', '"+str(ra_int)+"', '"+tipo+"','"+categoria+"')")
    cursor.execute(comando)