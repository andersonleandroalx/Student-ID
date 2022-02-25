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
tabela = pd.read_excel(r"C:\Imports\lote229.xlsx")


# ajustar os campos que serão listados
for i, aluno in enumerate(tabela["cod"]):
    lote = tabela.loc[i, "lote"]
    data = tabela.loc[i, "data_c"]
    nome = tabela.loc[i, "nome"]
    ra1 = tabela.loc[i, "ra"]
    tipo = tabela.loc[i, "tipo"]
    categoria = tabela.loc[i, "categoria"]
    print(lote, data, nome, ra1, tipo, categoria)

    #ra_int = ra1.item() # converte numpy em int
    lote_int = lote.item()  # converte numpy em int
    #print(type(ra_int)) # checa conversão
    login_user = "alxitaliano"
    nome = nome.strip()
    tipo = tipo.strip()
    categoria = categoria.strip()

# escolher qual insert será usado
    cursor = banco2.cursor()
    comando = ("insert into ids2 (lote,data_c, nome, ra, tipo, categoria, user_cadastro) values ('"+str(lote_int)+"', '"+str(data)+"','"+nome+"', '"+str(ra1)+"', '"+tipo+"','"+categoria+"','"+login_user+"')")
    cursor.execute(comando)
