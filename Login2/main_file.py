# import do PyQt5 o módulo Qtwidgets e uic para carregar as telas e as funções atribuidas aos botões
from PyQt5 import QtWidgets, uic
import mysql.connector
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# GLOBALS
numero_id = None
busca_id = None
busca_id2 = None
busca_id3 = None
login_user = ""
permissao = None

# DATABASE LINK
banco2 = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="db_1"
)


# FUNCTIONS
# START LOGIN
def def_login():
    global login_user
    global permissao
    login_sc.label_status.setText("")
    nome_user = login_sc.lineEdit.text()
    senha = login_sc.lineEdit_2.text()

    cursor = banco2.cursor()
    cursor.execute("Select login, senha, permissao1 from login where login='" + nome_user + "' and senha='" + senha + "'")
    result = cursor.fetchone()
    permissao = (str(result[2]))
    if result:
        login_user = nome_user
        main_sc.show()
        def_home()
        main_sc.label_8.setText(login_user)
        login_sc.close()
    else:
        login_sc.label_status.setText("Usuário ou senha incorretos!!")


# START HOME
def def_home():
    main_sc.users.close()
    main_sc.home.show()
    global busca_id
    global login_user
    global permissao
    print(type(permissao))

    main_sc.label_8.setText(login_user)
    # batches
    cursor = banco2.cursor()
    comando_sql1 = ("SELECT lote, date_format(data_abert, '%d-%m-%Y'), date_format(data_fech, '%d-%m-%Y'), lote_status FROM controle_lote1 order by lote desc LIMIT 2")
    cursor.execute(comando_sql1)
    dados_lidos1 = cursor.fetchall()

    main_sc.tableWidget.setRowCount(len(dados_lidos1))
    main_sc.tableWidget.setColumnCount(4)

    for i in range(0, len(dados_lidos1)):
        for j in range(0, 4):
            main_sc.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos1[i][j])))

    # carteirinhas
    busca_id = "Tudo"

    cursor = banco2.cursor()
    comando_sql2 = ("SELECT lote, date_format(data, '%d-%m-%Y')data, nome, ra, tipo, categoria, user_cadastro FROM carteirinhas order by id desc LIMIT 3")
    cursor.execute(comando_sql2)
    dados_lidos = cursor.fetchall()

    main_sc.tableWidget_2.setRowCount(len(dados_lidos))
    main_sc.tableWidget_2.setColumnCount(7)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 7):
            main_sc.tableWidget_2.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
# END HOME


# START USERS
def def_users():
    main_sc.home.close()
    main_sc.batch.close()
    main_sc.id_card.close()
    main_sc.reports_id.close()
    main_sc.about_app.close()
    main_sc.users.show()


def def_list_users():
    global permissao
    print(type(permissao))
    if permissao == '1':

        cursor = banco2.cursor()
        comando_sql1 = ("SELECT date_format(data, '%d-%m-%Y')data, nome, login, email FROM login order by id")
        cursor.execute(comando_sql1)
        dados_lidos1 = cursor.fetchall()

        main_sc.tableWidget_6.setRowCount(len(dados_lidos1))
        main_sc.tableWidget_6.setColumnCount(4)

        for i in range(0, len(dados_lidos1)):
            for j in range(0, 4):
                main_sc.tableWidget_6.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos1[i][j])))
    else:
        main_sc.label_20.setText("Usuário sem permissão")


def def_add_users():
    nome = main_sc.lineEdit.text()
    login1 = main_sc.lineEdit_2.text()
    senha1 = main_sc.lineEdit_3.text()
    senha2 = main_sc.lineEdit_4.text()
    email = main_sc.lineEdit_5.text()

    if nome != "" and login1 != "" and senha1 != "" and senha2 != "" and email != "":
        if senha1 == senha2:
            cursor = banco2.cursor()
            cursor.execute("Insert into login Values (null, now(), '" + nome + "','" + login1 + "','" + senha1 + "', '" + email + "')")
            main_sc.label_20.setText("Usuário cadastrado com Sucesso!!")
            main_sc.lineEdit.setText("")
            main_sc.lineEdit_2.setText("")
            main_sc.lineEdit_3.setText("")
            main_sc.lineEdit_4.setText("")
            main_sc.lineEdit_5.setText("")
            def_list_users()
        else:
            main_sc.label_20.setText("Senhas não conferem")
    else:
        main_sc.label_20.setText("Preencha todos os campos | Usuário não cadastrado!")


def def_del_users():
    linha = main_sc.tableWidget_6.currentRow()
    main_sc.tableWidget_6.removeRow(linha)

    cursor = banco2.cursor()
    cursor.execute("SELECT id FROM login")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM login WHERE id=" + str(valor_id))


def def_users_pdf():
    main_sc.label_20.setText("")

    cursor = banco2.cursor()
    comando_sql = "SELECT id, date_format(data, '%d-%m-%Y'), nome, login, email FROM login order by id asc"
    cursor.execute(comando_sql)
    dados_lidos = cursor.fetchall()
    y = 0
    #user_windows = getpass.getuser()
    #pdf = canvas.Canvas(f'C:\\Users\\{user_windows}\\Desktop\\cadastro_usuarios.pdf', pagesize=A4)
    pdf = canvas.Canvas("cadastro_usuarios.pdf")
    pdf.setFont("Times-Bold", 18)
    pdf.drawString(200, 800, "Usuários Cadastrados: ")
    # 200 é a distância do inicio do paragrafo levanto em conta a borda esquerda
    pdf.setFont("Times-Bold", 10)

    pdf.drawString(30, 750, "ID")
    pdf.drawString(60, 750, "Data Criação")
    pdf.drawString(180, 750, "Nome")
    pdf.drawString(300, 750, "Login")
    pdf.drawString(370, 750, "Email")

    for i in range(0, len(dados_lidos)):
        y = y + 25  # espaçamento entre linhas
        pdf.drawString(30, 750 - y, str(dados_lidos[i][0]))
        pdf.drawString(60, 750 - y, str(dados_lidos[i][1]))
        pdf.drawString(180, 750 - y, str(dados_lidos[i][2]))
        pdf.drawString(300, 750 - y, str(dados_lidos[i][3]))
        pdf.drawString(370, 750 - y, str(dados_lidos[i][4]))

    pdf.save()
    main_sc.label_20.setText("PDF Gerado com sucesso!!")
# END USERS


# START BATCH
def def_batch():
    main_sc.label_38.setText("")
    main_sc.lineEdit_9.setText("")
    main_sc.home.close()
    main_sc.users.close()
    main_sc.id_card.close()
    main_sc.reports_id.close()
    main_sc.about_app.close()
    main_sc.batch.show()


def def_check_batch():# Regularizar função
    nlote = int(main_sc.lineEdit_9.text())

    cursor = banco2.cursor()
    cursor.execute("SELECT lote FROM controle_lote1 order by lote desc")
    dados_lidos = cursor.fetchone()
    valor_id = dados_lidos[0]
    print(type(valor_id))
    print(type(nlote))

    if valor_id != nlote:
        cursor2 = banco2.cursor()
        abrir = ("Insert into controle_lote1 (id, lote, data_abert, data_fech, lote_status) values (null,'" + str(nlote) + "', now(), null, 'Aberto')")
        cursor2.execute(abrir)
        main_sc.label_38.setText("Novo Lote Aberto")
        def_list_batch()
        print("Aberto")
    else:
        main_sc.label_38.setText("Lote já está aberto")
        print("não deu")


def def_add_batch(): # Regularizar função - Erro no if com insert ???
    nlote = int(main_sc.lineEdit_9.text())
    print(nlote)
    print(30*"-")

    cursor = banco2.cursor()
    cursor.execute("SELECT lote FROM controle_lote1 order by lote desc")
    dados_lidos = cursor.fetchone()
    valor_id = dados_lidos[0]
    print(type(valor_id))
    print(type(nlote))

    if valor_id != nlote:
        cursor2 = banco2.cursor()
        abrir = ("Insert into controle_lote1 (id, lote, data_abert, data_fech, lote_status) values (null,'" + str(nlote) + "', now(), null, 'Aberto')")
        cursor2.execute(abrir)
        main_sc.label_38.setText("Novo Lote Aberto")
        def_list_batch()
        print("Aberto")
    else:
        main_sc.label_38.setText("Lote já está aberto")
        print("não deu")


def def_close_batch():
    nlote = main_sc.lineEdit_9.text()

    cursor2 = banco2.cursor()
    consulta = ("Update controle_lote1 set data_fech = now(), lote_status = 'Fechado' where lote = '" + nlote + "' ")
    cursor2.execute(consulta)
    main_sc.label_38.setText("O lote selecionado foi fechado")
    def_list_batch()


def def_del_batch():
    linha = main_sc.tableWidget_4.currentRow()

    if linha != -1:
        cursor = banco2.cursor()
        cursor.execute("SELECT id, lote_status FROM controle_lote1 order by id desc")
        dados_lidos = cursor.fetchall()
        valor_id = dados_lidos[linha][0]
        valor_id2 = dados_lidos[linha][1]
        if valor_id2 == "Aberto":
            main_sc.label_38.setText("O lote selecionado está aberto e não pode ser deletado!")
        else:
            main_sc.tableWidget_4.removeRow(linha)
            cursor.execute("DELETE FROM controle_lote1 WHERE id = " + str(valor_id))
            main_sc.label_38.setText("O lote selecionado foi deletado")
            def_list_batch()
    else:
        main_sc.label_38.setText("Escolha um lote ou vc não tem permissão!")


def def_list_batch():
    cursor = banco2.cursor()
    comando_sql1 = ("SELECT lote, date_format(data_abert, '%d-%m-%Y'), date_format(data_fech, '%d-%m-%Y'), lote_status FROM controle_lote1 order by lote desc")
    cursor.execute(comando_sql1)
    dados_lidos1 = cursor.fetchall()

    main_sc.tableWidget_4.setRowCount(len(dados_lidos1))
    main_sc.tableWidget_4.setColumnCount(4)

    for i in range(0, len(dados_lidos1)):
        for j in range(0, 4):
            main_sc.tableWidget_4.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos1[i][j])))


def def_pdf_batch(): # criar função
    pass
# END BATCH


# START ID CARD
def def_id_card():
    main_sc.home.close()
    main_sc.users.close()
    main_sc.batch.close()
    main_sc.reports_id.close()
    main_sc.about_app.close()
    main_sc.id_card.show()


def def_list_id():
    cursor = banco2.cursor()
    comando_sql2 = ("SELECT lote, date_format(data, '%d-%m-%Y'), nome, ra, tipo, categoria, user_cadastro FROM carteirinhas order by id desc LIMIT 7")
    cursor.execute(comando_sql2)
    dados_lidos = cursor.fetchall()

    main_sc.tableWidget_3.setRowCount(len(dados_lidos))
    main_sc.tableWidget_3.setColumnCount(7)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 7):
            main_sc.tableWidget_3.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


def def_add_idcard(): # Melhorar função
    global login_user

    lote1 = main_sc.lineEdit_6.text()
    nome1 = main_sc.lineEdit_7.text()
    ra1 = main_sc.lineEdit_8.text()


    tipo1 = ""
    if main_sc.radioButton.isChecked():
        tipo1 = "1ª Via"
    elif main_sc.radioButton_2.isChecked():
        tipo1 = "2ª Via"
    elif main_sc.radioButton_3.isChecked():
        tipo1 = "Atualização de Foto"
    else:
        tipo1 = ""

    if lote1 != "" and nome1 != "" and ra1 != "" and tipo1 != "":
        cursor = banco2.cursor()
        status_lote = ("select lote_status from controle_lote1 where lote = " + lote1)
        cursor.execute(status_lote)
        dados_lidos = cursor.fetchone()
        status = (str(dados_lidos[0]))
        if status == "Aberto":
            comando_sql = ("INSERT INTO carteirinhas (id, lote, data, nome, ra, tipo, categoria, user_cadastro) VALUES (null, '" + lote1 + "', now(),'" + nome1 + "','" + ra1 + "','" + tipo1 + "', 'Aluno', '" + login_user + "')")
            cursor.execute(comando_sql)
            banco2.commit()
            def_list_id()
            main_sc.label_29.setText("Cadastro Efetuado com sucesso!!")
            main_sc.lineEdit_7.setText("")
            main_sc.lineEdit_8.setText("")
        else:
            main_sc.label_29.setText("Lote já está fechado, abra outro primeiro!!")
    else:
        main_sc.label_29.setText("Preencha os dados para cadastrar")


def def_alter_idcard(): # Criar função
    pass


def def_del_idcard(): # Criar função
    pass
# END ID CARD


# START REPORTS
def def_reports_id():
    main_sc.home.close()
    main_sc.users.close()
    main_sc.batch.close()
    main_sc.id_card.close()
    main_sc.about_app.close()
    main_sc.reports_id.show()


def def_reports_all():
    main_sc.label_44.setText("")
    global busca_id
    #relcarteirinhas.show()

    if busca_id != "":
        cursor = banco2.cursor()
        comando_sql2 = ("SELECT lote, date_format(data, '%d-%m-%Y'), nome, ra, tipo, categoria, user_cadastro FROM carteirinhas where tipo = '" + busca_id + "' order by ID desc")
        cursor.execute(comando_sql2)
        dados_lidos = cursor.fetchall()
    else:
        cursor = banco2.cursor()
        comando_sql2 = ("SELECT lote, date_format(data, '%d-%m-%Y'), nome, ra, tipo, categoria, user_cadastro FROM carteirinhas order by ID desc")
        cursor.execute(comando_sql2)
        dados_lidos = cursor.fetchall()

    main_sc.tableWidget_5.setRowCount(len(dados_lidos))
    main_sc.tableWidget_5.setColumnCount(7)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 7):
            main_sc.tableWidget_5.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


def def_reports_name():
    main_sc.label_44.setText("")
    global busca_id
    global busca_id2
    global busca_id3
    #relcarteirinhas.show()

    if busca_id2 == 'nome':
        cursor = banco2.cursor()
        comando_sql2 = ("SELECT lote, date_format(data, '%d-%m-%Y'), nome, ra, tipo, categoria, user_cadastro FROM carteirinhas where nome like '%" + busca_id + "%' order by ID desc")
        cursor.execute(comando_sql2)
        dados_lidos = cursor.fetchall()
    elif busca_id2 == "ra":
        cursor = banco2.cursor()
        comando_sql2 = ("SELECT lote, date_format(data, '%d-%m-%Y'), nome, ra, tipo, categoria, user_cadastro FROM carteirinhas where ra like '%" + busca_id + "%' order by ID desc")
        cursor.execute(comando_sql2)
        dados_lidos = cursor.fetchall()
    elif busca_id2 == "lote":
        cursor = banco2.cursor()
        comando_sql2 = ("SELECT lote, date_format(data, '%d-%m-%Y'), nome, ra, tipo, categoria, user_cadastro FROM carteirinhas where lote like '%" + busca_id + "%' order by ID desc")
        cursor.execute(comando_sql2)
        dados_lidos = cursor.fetchall()
    elif busca_id2 == "usuario":
        cursor = banco2.cursor()
        comando_sql2 = ("SELECT lote, date_format(data, '%d-%m-%Y'), nome, ra, tipo, categoria, user_cadastro FROM carteirinhas where user_cadastro like '%" + busca_id + "%' order by ID desc")
        cursor.execute(comando_sql2)
        dados_lidos = cursor.fetchall()
    elif busca_id2 == "data":
        cursor = banco2.cursor()
        comando_sql2 = ("SELECT lote, date_format(data, '%d-%m-%Y'), nome, ra, tipo, categoria, user_cadastro FROM carteirinhas where data between '" + busca_id + "' and '" + busca_id3 + "' order by data desc")
        cursor.execute(comando_sql2)
        dados_lidos = cursor.fetchall()


    main_sc.tableWidget_5.setRowCount(len(dados_lidos))
    main_sc.tableWidget_5.setColumnCount(7)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 7):
            main_sc.tableWidget_5.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


def def_reports_type():
    main_sc.label_44.setText("")
    global busca_id
    global busca_id2
    global busca_id3
    # tipo1 = ""

    # if tipo1 == "teste":
    if main_sc.radioButton_4.isChecked():
        busca_id = "1ª Via"
        def_reports_all()
    elif main_sc.radioButton_5.isChecked():
        busca_id = "2ª Via"
        def_reports_all()
    elif main_sc.radioButton_6.isChecked():
        busca_id = "Atualização de foto"
        def_reports_all()
    elif main_sc.radioButton_8.isChecked():
        busca_id2 = "nome"
        busca_id = main_sc.lineEdit_10.text()
        def_reports_name()
    elif main_sc.radioButton_9.isChecked():
        busca_id2 = "ra"
        busca_id = main_sc.lineEdit_10.text()
        def_reports_name()
    elif main_sc.radioButton_10.isChecked():
        busca_id2 = "lote"
        busca_id = main_sc.lineEdit_10.text()
        def_reports_name()
    elif main_sc.radioButton_11.isChecked():
        busca_id2 = "usuario"
        busca_id = main_sc.lineEdit_10.text()
        def_reports_name()
    elif main_sc.radioButton_12.isChecked():
        busca_id2 = "data"
        busca_id = main_sc.dateEdit.text()
        busca_id3 = main_sc.dateEdit_2.text()
        def_reports_name()
    else:
        busca_id = ""
        def_reports_all()


def def_reports_date():
    pass


def def_reports_pdf():
    global busca_id
    global busca_id2
    global busca_id3
    #main_sc.label_44.setText("")

    if busca_id == "":
        cursor = banco2.cursor()
        comando_sql = ("SELECT lote, date_format(data, '%d-%m-%Y'), nome, ra, tipo, categoria, user_cadastro FROM carteirinhas order by ID desc")
        cursor.execute(comando_sql)
        dados_lidos = cursor.fetchall()

    elif busca_id == '1ª Via':
        cursor = banco2.cursor()
        comando_sql = ("SELECT lote, date_format(data, '%d-%m-%Y'), nome, ra, tipo, categoria, user_cadastro FROM carteirinhas where tipo = '" + busca_id + "' order by ID")
        cursor.execute(comando_sql)
        dados_lidos = cursor.fetchall()

    elif busca_id == '2ª Via':
        cursor = banco2.cursor()
        comando_sql = ("SELECT lote, date_format(data, '%d-%m-%Y'), nome, ra, tipo, categoria, user_cadastro FROM carteirinhas where tipo = '" + busca_id + "' order by ID")
        cursor.execute(comando_sql)
        dados_lidos = cursor.fetchall()

    elif busca_id == 'Atualização de foto':
        cursor = banco2.cursor()
        comando_sql = ("SELECT lote, date_format(data, '%d-%m-%Y'), nome, ra, tipo, categoria, user_cadastro FROM carteirinhas where tipo = '" + busca_id + "' order by ID")
        cursor.execute(comando_sql)
        dados_lidos = cursor.fetchall()

    elif busca_id2 == 'nome':
        cursor = banco2.cursor()
        comando_sql = ("SELECT lote, date_format(data, '%d-%m-%Y'), nome, ra, tipo, categoria, user_cadastro FROM carteirinhas where nome like '%" + busca_id + "%' order by ID desc")
        #comando_sql = ("SELECT lote, data, nome, ra, tipo, categoria, user_cadastro FROM carteirinhas where nome = '" + busca_id + "' order by ID")
        cursor.execute(comando_sql)
        dados_lidos = cursor.fetchall()

    elif busca_id2 == 'ra':
        cursor = banco2.cursor()
        comando_sql = ("SELECT lote, date_format(data, '%d-%m-%Y'), nome, ra, tipo, categoria, user_cadastro FROM carteirinhas where ra like '%" + busca_id + "%' order by ID desc")
        cursor.execute(comando_sql)
        dados_lidos = cursor.fetchall()

    elif busca_id2 == 'lote':
        cursor = banco2.cursor()
        comando_sql = ("SELECT lote, date_format(data, '%d-%m-%Y'), nome, ra, tipo, categoria, user_cadastro FROM carteirinhas where lote like '%" + busca_id + "%' order by ID desc")
        cursor.execute(comando_sql)
        dados_lidos = cursor.fetchall()

    elif busca_id2 == 'usuario':
        cursor = banco2.cursor()
        comando_sql = ("SELECT lote, date_format(data, '%d-%m-%Y'), nome, ra, tipo, categoria, user_cadastro FROM carteirinhas where user_cadastro like '%" + busca_id + "%' order by ID desc")
        cursor.execute(comando_sql)
        dados_lidos = cursor.fetchall()

    elif busca_id2 == 'data':
        cursor = banco2.cursor()
        comando_sql = ("SELECT lote, date_format(data, '%d-%m-%Y'), nome, ra, tipo, categoria, user_cadastro FROM carteirinhas where data between '" + busca_id + "' and '" + busca_id3 + "' order by data")
        cursor.execute(comando_sql)
        dados_lidos = cursor.fetchall()

    y = 0
    pdf = canvas.Canvas("cadastro_carteirinhas.pdf")
    pdf.setFont("Times-Bold", 18)
    pdf.drawString(200, 800, "Relatório - ID's Estudante: ")
    # 200 é a distância do inicio do paragrafo levanto em conta a borda esquerda
    pdf.setFont("Times-Bold", 10)

    pdf.drawString(20, 750, "Lote")
    pdf.drawString(50, 750, "Data")
    pdf.drawString(150, 750, "Nome")
    pdf.drawString(320, 750, "RA/CPF/RG")
    pdf.drawString(390, 750, "Tipo")
    pdf.drawString(500, 750, "Categoria")
    pdf.drawString(600, 750, "Cadastrado por")

    for i in range(0, len(dados_lidos)):
        y = y + 25  # espaçamento entre linhas
        pdf.drawString(20, 750 - y, str(dados_lidos[i][0]))
        pdf.drawString(50, 750 - y, str(dados_lidos[i][1]))
        pdf.drawString(150, 750 - y, str(dados_lidos[i][2]))
        pdf.drawString(320, 750 - y, str(dados_lidos[i][3]))
        pdf.drawString(390, 750 - y, str(dados_lidos[i][4]))
        pdf.drawString(500, 750 - y, str(dados_lidos[i][5]))
        pdf.drawString(600, 750 - y, str(dados_lidos[i][6]))

    pdf.save()
    main_sc.label_44.setText("PDF Gerado com sucesso!!")
# END REPORTS

# ABOUT
def def_about_app():
    main_sc.home.close()
    main_sc.users.close()
    main_sc.batch.close()
    main_sc.id_card.close()
    main_sc.reports_id.close()
    main_sc.about_app.show()

    global login_user

    cursor = banco2.cursor()
    sobre = ("select date_format(data, '%d-%m-%Y'), nome, email from login where login = '" + login_user + "'")
    cursor.execute(sobre)
    dados_lidos = cursor.fetchone()
    data = (str(dados_lidos[0]))
    nome = (str(dados_lidos[1]))
    email = (str(dados_lidos[2]))
    main_sc.label_50.setText(nome)
    main_sc.label_51.setText(login_user)
    main_sc.label_52.setText(email)
    main_sc.label_53.setText(data)


# LOGOFF
def def_logout():
    main_sc.close()
    login_sc.show()
    login_sc.lineEdit.setText("")
    login_sc.lineEdit_2.setText("")


# FORMS
app = QtWidgets.QApplication([])
login_sc = uic.loadUi("login.ui")
main_sc = uic.loadUi("main_window.ui")

# BUTTONS
# lOGIN
login_sc.b_login.clicked.connect(def_login)
# MAIN WINDOW
main_sc.pushButton.clicked.connect(def_home)
main_sc.pushButton_2.clicked.connect(def_users)
main_sc.pushButton_3.clicked.connect(def_batch)
main_sc.pushButton_4.clicked.connect(def_id_card)
main_sc.pushButton_5.clicked.connect(def_reports_id)
main_sc.pushButton_6.clicked.connect(def_about_app)
main_sc.pushButton_8.clicked.connect(def_add_idcard)
main_sc.pushButton_18.clicked.connect(def_logout)
# USERS
main_sc.pushButton_7.clicked.connect(def_add_users)
main_sc.pushButton_15.clicked.connect(def_list_users)
main_sc.pushButton_16.clicked.connect(def_del_users)
main_sc.pushButton_17.clicked.connect(def_users_pdf)
# BATCHES
main_sc.pushButton_9.clicked.connect(def_add_batch)
main_sc.pushButton_10.clicked.connect(def_close_batch)
main_sc.pushButton_11.clicked.connect(def_list_batch)
main_sc.pushButton_12.clicked.connect(def_del_batch)
# ID
main_sc.pushButton_19.clicked.connect(def_list_id)
# REPORTS
main_sc.pushButton_13.clicked.connect(def_reports_type)
main_sc.pushButton_14.clicked.connect(def_reports_pdf)


login_sc.show()
#main_sc.show()
app.exec()

