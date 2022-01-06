import mysql.connector

banco2 = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="dbo_studentid"
)

total = 0
for i in range(267):
    total += 1
    print(total)

# escolher qual insert será usado
    cursor = banco2.cursor()
    comando = ("insert into batch (lote_batch, dataab_batch, status_batch) values ('"+str(total)+"', now(),'Aberto')")
    cursor.execute(comando)