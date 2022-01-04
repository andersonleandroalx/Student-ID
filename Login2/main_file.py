# import do PyQt5 o módulo Qtwidgets e uic para carregar as telas e as funções atribuidas aos botões
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap
import mysql.connector
from reportlab.pdfgen import canvas
import datetime
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
#    global permissao

    login_sc.label_status.setText("")
    nome_user = login_sc.lineEdit.text()
    senha = login_sc.lineEdit_2.text()
    print(nome_user, senha)

    if nome_user and senha:
        try:
            cursor = banco2.cursor()
            #cursor.execute("Select login, senha from login where login ='" + nome_user + "' and senha='" + senha + "'")
            cursor.execute("Select login, senha from login")
            result = cursor.fetchall()
            print(result)
            #user_s, senha_s = result
            #print(user_s, senha_s)
            for user_s, senha_s in result:
                if nome_user == user_s and senha == senha_s:
                    #if result:
                    login_user = nome_user
                    main_sc.show()
                    def_home()
                    main_sc.label_8.setText(login_user)
                    login_sc.close()
                    print(user_s, senha_s)
                    #print("ok")
                    #print(30 * "-")
                    #break
                else:
                    login_sc.label_status.setText("Usuário ou senha incorretos!!")
        except mysql.connector.Error as err:
            print("deu erro: ", err)
            login_sc.lineEdit.setText("")
            login_sc.lineEdit_2.setText("")
            login_sc.label_status.setText("Erro de digitação")
    else:
        login_sc.label_status.setText("Preencha os dados")

    #    permissao = (str(result[2]))
        #if user_s == nome_user



# START HOME
def def_home():
    main_sc.users.close()
    main_sc.home.show()
    def_list_home()
    global busca_id
    global login_user
    dt = datetime.datetime.now()
    main_sc.label_34.setText(dt.strftime("%d/%b/%Y"))
    main_sc.label_45.setText(dt.strftime("%A"))

#    global permissao

def def_list_home():

    global login_user

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
    def_list_info_users()


def def_list_info_users():
    global login_user
    print(login_user)

    cursor = banco2.cursor()
    consulta = ("SELECT nome, login, email FROM login where login = '" + login_user + "'")
    cursor.execute(consulta)
    resultado = cursor.fetchone()
    print(resultado)
    nome_user, log_user, email_user = resultado

    print(nome_user, log_user, email_user)
    main_sc.label_69.setText(nome_user)
    main_sc.label_70.setText(log_user)
    main_sc.label_71.setText(email_user)
    main_sc.label_72.setPixmap(QPixmap('img_users/' + login_user + '.png'))
    main_sc.label_72.setGeometry(20, 30, 100, 80)


def def_alter_pwd_form():
    alt_pwd_user_sc.show()


def def_alter_pwd_user():
    global login_user

    senha1 = alt_pwd_user_sc.lineEdit.text()
    senha2 = alt_pwd_user_sc.lineEdit_2.text()

    print(senha1, senha2)
    if login_user:
        if senha1 == senha2:
            cursor = banco2.cursor()
            consulta = ("UPDATE login SET senha = '" + senha1 + "' where '" + login_user + "' = login")
            cursor.execute(consulta)
            main_sc.label_20.setText("Senha atualizada com sucesso!!")
            alt_pwd_user_sc.close()
        else:
            main_sc.label_20.setText("Senhas estão diferentes!")

    else:
        print("nenhum usuário selecionado")


def def_alter_user_form():
    alt_all_sc.show()

    cursor = banco2.cursor()
    consulta = ("SELECT nome, email FROM login where login = '" + login_user + "'")
    cursor.execute(consulta)
    resultado = cursor.fetchone()
    nome_user, email_user = resultado
    alt_all_sc.lineEdit.setText(nome_user)
    alt_all_sc.lineEdit_2.setText(email_user)

    print(nome_user, email_user)


def def_alter_self_user():
    global login_user

    nome_user = alt_all_sc.lineEdit.text()
    email_user = alt_all_sc.lineEdit_2.text()
    senha1 = alt_all_sc.lineEdit_3.text()
    senha2 = alt_all_sc.lineEdit_4.text()
    print(nome_user, email_user)
    if nome_user and email_user and senha1 == "" or senha1 or senha2:
        cursor = banco2.cursor()
        consulta = ("UPDATE login SET nome = '" + nome_user + "', email = '" + email_user + "'  where '" + login_user + "' = login")
        cursor.execute(consulta)
        #main_sc.label_20.setText("Nome e email atualizados!")
        def_list_info_users()
        alt_all_sc.close()
        print("user e email atualizados")
        if senha1 != "" and senha2 != "":
            if senha1 == senha1:
                cursor = banco2.cursor()
                consulta = ("UPDATE login SET nome = '" + nome_user + "', email = '" + email_user + "', senha = '" + senha1 + "'  where '" + login_user + "' = login")
                cursor.execute(consulta)
                #main_sc.label_20.setText("Senha atualizada com sucesso!!")
                #alt_pwd_user_sc.close()
                def_list_info_users()
                alt_all_sc.close()
                print("user, email e senhas atualizados")
            else:
                print("senhas não batem")
        else:
            pass

    else:
        print("Campos não podem ficar em branco")



def def_list_users():
    #global permissao
    #print(type(permissao))
    #if permissao == '1':

    cursor = banco2.cursor()
    comando_sql1 = ("SELECT date_format(data, '%d-%m-%Y')data, nome, login, email FROM login order by id")
    cursor.execute(comando_sql1)
    dados_lidos1 = cursor.fetchall()

    main_sc.tableWidget_6.setRowCount(len(dados_lidos1))
    main_sc.tableWidget_6.setColumnCount(4)

    for i in range(0, len(dados_lidos1)):
        for j in range(0, 4):
            main_sc.tableWidget_6.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos1[i][j])))
    #else:
        #main_sc.label_20.setText("Usuário sem permissão")


def def_add_users():
    nome = main_sc.lineEdit.text()
    login1 = main_sc.lineEdit_2.text()
    senha1 = main_sc.lineEdit_3.text()
    senha2 = main_sc.lineEdit_4.text()
    email = main_sc.lineEdit_5.text()

    if nome and login1 and senha1 and senha2 and email:
        if '@' in email and '.' in email[email.find('@'):]:
            if senha1 == senha2:
                cursor = banco2.cursor()
                cursor.execute("Insert into login (data, nome, login, senha, email) Values (now(), '" + nome + "','" + login1 + "','" + senha1 + "', '" + email + "')")
                main_sc.label_20.setText("Usuário cadastrado com Sucesso!!")
                main_sc.lineEdit.setText("")
                main_sc.lineEdit_2.setText("")
                main_sc.lineEdit_3.setText("")
                main_sc.lineEdit_4.setText("")
                main_sc.lineEdit_5.setText("")
                def_list_users()
            else:
                main_sc.label_20.setText("Senhas  digitadas são diferentes!")
        else:
            main_sc.label_20.setText("Formato de email inválido")
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


def def_check_batch():
    global permissao

    cursor = banco2.cursor()
    cursor.execute("SELECT lote, lote_status FROM controle_lote1 order by lote desc")
    dados_lidos = cursor.fetchone()
    permissao = dados_lidos


def def_add_batch():
    #def_check_batch()
    nlote = main_sc.lineEdit_9.text()
    print(nlote)

    if nlote:
        cursor2 = banco2.cursor()
        abrir = ("Insert into controle_lote1 (lote, data_abert, data_fech, lote_status) values ('" + nlote + "', now(), null, 'Aberto')")
        cursor2.execute(abrir)
        main_sc.label_38.setText("Novo Lote Aberto")
        def_list_batch()
        alert_sc.show()
        alert_sc.controle_alert.setText("add_id")
        alert_sc.label.setText("Deseja cadastrar novos cartões de estudante agora?")
    else:
        main_sc.label_38.setText("Preencha o lote")


def def_close_batch():
    nlote = main_sc.lineEdit_9.text()

    if nlote:
        cursor2 = banco2.cursor()
        consulta = ("Update controle_lote1 set data_fech = now(), lote_status = 'Fechado' where lote = '" + nlote + "' ")
        cursor2.execute(consulta)
        main_sc.label_38.setText("O lote selecionado foi fechado")
        def_list_batch()
        alert_sc.show()
        alert_sc.controle_alert.setText("add_rem")
        alert_sc.label.setText("Deseja abrir um arquivo de remessa agora?")
    else:
        main_sc.label_38.setText("Preencha o lote")


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
    #def_check_batch()

    '''global permissao
    print("lote do add-id:", permissao)
    lote, lote_status = permissao
    print(lote)
    print(type(lote))
    print(lote_status)
    main_sc.label_65.setText(str(lote))
    main_sc.label_24.setText(str(lote_status))'''


def def_list_id():
    cursor = banco2.cursor()
    comando_sql2 = ("SELECT lote, date_format(data, '%d-%m-%Y'), nome, ra, tipo, categoria, user_cadastro FROM carteirinhas order by id desc LIMIT 7")
    cursor.execute(comando_sql2)
    dados_lidos = cursor.fetchall()
    print(dados_lidos)

    main_sc.tableWidget_3.setRowCount(len(dados_lidos))
    main_sc.tableWidget_3.setColumnCount(7)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 7):
            main_sc.tableWidget_3.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


def def_add_idcard(): # Melhorar função
    global login_user
    #global permissao
    #lote2, lote_status = permissao
    #print(permissao)
    lote_status = "Fechado"

    #lote1 =  main_sc.label_65.text()
    #print(lote_status)
    lote1 = main_sc.lineEdit_6.text()
    nome1 = main_sc.lineEdit_7.text()
    ra1 = main_sc.lineEdit_8.text()
    print(lote1, nome1, ra1)
    print(type(lote1))
    print(type(nome1))
    print(type(ra1))

    tipo1 = ""

    if main_sc.radioButton.isChecked():
        tipo1 = "1ª Via"
    elif main_sc.radioButton_2.isChecked():
        tipo1 = "2ª Via"
    elif main_sc.radioButton_3.isChecked():
        tipo1 = "Atualização de Foto"
    else:
        tipo1 = ""

    print(30*"-")
    print(type(tipo1))
    print(tipo1)

    if lote_status == "Aberto":
        if lote1 and nome1 and ra1 and tipo1:
            cursor = banco2.cursor()
            comando_sql = ("INSERT INTO carteirinhas (id, lote, data, nome, ra, tipo, categoria, user_cadastro) VALUES (null, '" + lote1 + "', now(),'" + nome1 + "','" + ra1 + "','" + tipo1 + "', 'Aluno', '" + login_user + "')")
            cursor.execute(comando_sql)
            print("ok")
        else:
            print("erro")
    else:
        print("Lote está fechado, abra outro para iniciar")

    #cursor = banco2.cursor()
    #comando_sql = ("INSERT INTO carteirinhas (id, lote, data, nome, ra, tipo, categoria, user_cadastro) VALUES (null, '" + lote1 + "', now(),'" + nome1 + "','" + ra1 + "','" + tipo1 + "', 'Aluno', '" + login_user + "')")
    #cursor.execute(comando_sql)

    #if lote_status == "Aberto":
    #if lote1 and nome1 and ra1 and tipo1:
        #cursor = banco2.cursor()
        #status_lote = ("select lote_status from controle_lote1 where lote = " + lote1)
        #cursor.execute(status_lote)
        #dados_lidos = cursor.fetchone()
        #status = (dados_lidos[0])
        #if status == "Aberto":
        #if lote_status == "Aberto":
        #if lote1 and nome1 and ra1 and tipo1:
         #   cursor = banco2.cursor()
          #  comando_sql = ("INSERT INTO carteirinhas (id, lote, data, nome, ra, tipo, categoria, user_cadastro) VALUES (null, '" + lote1 + "', now(),'" + nome1 + "','" + ra1 + "','" + tipo1 + "', 'Aluno', '" + login_user + "')")
           # cursor.execute(comando_sql)
            #banco2.commit()
            #def_list_id()
         #   main_sc.label_29.setText("Cadastro Efetuado com sucesso!!")
         #   main_sc.lineEdit_7.setText("")
         #   main_sc.lineEdit_8.setText("")
        #else:
        #    main_sc.label_29.setText("Lote já está fechado, abra outro primeiro!!")
    #else:
    #    main_sc.label_29.setText("Preencha os dados para cadastrar")


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

    pdf.drawString(20, 780, "Quantidade de ID's: ")
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
    main_sc.label_44.setText("PDF Gerado com sucesso1!!")
# END REPORTS

# ABOUT
def def_about_app():
    main_sc.home.close()
    main_sc.users.close()
    main_sc.batch.close()
    main_sc.id_card.close()
    main_sc.reports_id.close()
    main_sc.about_app.show()


# LOGOFF
def def_logout():
    main_sc.close()
    login_sc.show()
    login_sc.lineEdit.setText("")
    login_sc.lineEdit_2.setText("")


# ALERT
def def_alert_close():
    alert_sc.close()


def def_alert_id_open():
    indicador = alert_sc.label.text()
    indicador2 = alert_sc.controle_alert.text()
    print(indicador)
    print(type(indicador2))

    if indicador2 == "add_id":
        alert_sc.close()
        main_sc.id_card.show()
    else:
        alert_sc.close()
        print("add rem")


# FORMS
app = QtWidgets.QApplication([])
login_sc = uic.loadUi("login.ui")
main_sc = uic.loadUi("main_window.ui")
alert_sc = uic.loadUi("alerta.ui")
alt_pwd_user_sc = uic.loadUi("alt_pwd.ui")
alt_all_sc = uic.loadUi("alt_all.ui")

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
main_sc.pushButton_23.clicked.connect(def_alter_pwd_form)
main_sc.pushButton_24.clicked.connect(def_alter_user_form)


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
# POP UPS
# ALERT
alert_sc.pushButton.clicked.connect(def_alert_id_open)
alert_sc.pushButton_2.clicked.connect(def_alert_close)
# ALT PWD
alt_pwd_user_sc.pushButton.clicked.connect(def_alter_pwd_user)
# ALT USERS DATA
alt_all_sc.pushButton.clicked.connect(def_alter_self_user)



login_sc.show()
#main_sc.show()
app.exec()

