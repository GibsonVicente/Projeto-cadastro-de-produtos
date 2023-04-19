from PyQt5 import QtWidgets,uic
import mysql.connector
from reportlab.pdfgen import canvas

#Está linha de codigos serve para fazer a conexão com o banco de dados

banco = mysql.connector.connect(
    user='root', password='',
    host='localhost',
    database='cadastro_produtos',
    port='3307'
)

numero_id = 0


#essa função serve para excluir registros do banco de dados
def excluir_dados():
    linha = tela2.tableWidget.currentRow()
    tela2.tableWidget.removeRow(linha)

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM produtos WHERE id="+str(valor_id))
    banco.commit()

#essa função serve para programar e chamar a tela para editar e salvar os registros editaos
def editar_dados():
    global numero_id
    linha = tela2.tableWidget.currentRow()

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM produtos WHERE id=" + str(valor_id))
    produto = cursor.fetchall()
    tela3.show()

    numero_id = valor_id

    tela3.lineEdit.setText(str(produto[0][0]))
    tela3.lineEdit_2.setText(str(produto[0][1]))
    tela3.lineEdit_3.setText(str(produto[0][2]))
    tela3.lineEdit_4.setText(str(produto[0][3]))
    tela3.lineEdit_5.setText(str(produto[0][4]))



#função para salvar o registro e atualizar as telas
def salvar_dados_editados():
    global numero_id

    codigo = tela3.lineEdit_2.text()
    nome = tela3.lineEdit_3.text()
    preco = tela3.lineEdit_4.text().replace(',','.')
    categoria = tela3.lineEdit_5.text()

    cursor = banco.cursor()
    cursor.execute("UPDATE produtos SET codigo = '{}', nome = '{}', preco = '{}', categoria = '{}' WHERE id = '{}'".format(codigo, nome, preco, categoria, numero_id))
    banco.commit()
    tela3.close()
    tela2.close()
    listar_dados()



#função responsavél por gerar o PDF
def gerar_pdf():
    cursor = banco.cursor()
    comando_sql_lerdados = "SELECT * FROM produtos"
    cursor.execute(comando_sql_lerdados)
    dados_lidos = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("cadastro_produtos.pdf")
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(200, 800, "Produtos Cadastrados: ")
    pdf.setFont("Times-Bold", 18)

    pdf.drawString(10, 750, "ID")
    pdf.drawString(110, 750, "Código")
    pdf.drawString(210, 750, "Produto")
    pdf.drawString(310, 750, "Preço")
    pdf.drawString(410, 750, "Categoria")

    # Esse for serve para definir a posição dos registros no pdf a ser gerado
    for i in range(0, len(dados_lidos)):
        y = y + 50
        pdf.drawString(10, 750 - y, str(dados_lidos[i][0]))
        pdf.drawString(110, 750 - y, str(dados_lidos[i][1]))
        pdf.drawString(210, 750 - y, str(dados_lidos[i][2]))
        pdf.drawString(310, 750 - y, str(dados_lidos[i][3]))
        pdf.drawString(410, 750 - y, str(dados_lidos[i][4]))

    pdf.save()
    print("O PDF foi gerado com sucesso!")


#função resposavél pelo algoritimo da tela1
def controle():
    linha1 = tela1.lineEdit.text()
    linha2 = tela1.lineEdit_2.text()
    linha3 = tela1.lineEdit_3.text()

    categoria = ""

    print('codigo:{}'.format(linha1))
    print('nome:{}'.format(linha2))
    print('preço:{}'.format(linha3))

    if tela1.radioButton.isChecked():
        print('A categoria escolhida foi Informática')
        categoria = "Informatica"
    elif tela1.radioButton_2.isChecked():
        print('A categotia escolhida foi Alimentos')
        categoria = "Alimentos"
    else:
        print('A categoria escolhida foi Eletronico')
        categoria = "Eletronico"

    cursor = banco.cursor()
    comando_sql = "INSERT INTO produtos (codigo, nome, preco, categoria) VALUES (%s,%s,%s,%s)"
    dados = (str(linha1), str(linha2), str(linha3).replace(',','.'), categoria)
    cursor.execute(comando_sql, dados)
    banco.commit()
    cursor.close()
    #comando para limpar os campos após clicar no botão enviar
    tela1.lineEdit.setText("")
    tela1.lineEdit_2.setText("")
    tela1.lineEdit_3.setText("")


def listar_dados():
    tela2.show()
    cursor = banco.cursor()
    # os codigos a seguir tem a função de mostrar os registros de produtos cadastrados, na tela2
    comando_sql_lerdados = "SELECT * FROM produtos"
    cursor.execute(comando_sql_lerdados)
    # os registros obtidos são salvos nessa variavél
    dados_lidos = cursor.fetchall()
    # define o a tabela da tela2 com linhas variaves de acordo com os dados lidos e as colunas fixas
    tela2.tableWidget.setRowCount(len(dados_lidos))
    tela2.tableWidget.setColumnCount(5)
    # comando para percorrer as linhas e colunas do banco de dados
    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            tela2.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


app = QtWidgets.QApplication([])
tela1 = uic.loadUi("tela1.ui")
tela1.pushButton.clicked.connect(controle)
#carrega a tela de listar_dados
tela2 = uic.loadUi("tela2.ui")
tela3 = uic.loadUi("tela3.ui")
tela3.pushButton.clicked.connect(salvar_dados_editados)
tela1.pushButton_2.clicked.connect(listar_dados)
tela2.pushButton.clicked.connect(gerar_pdf)
tela2.pushButton_2.clicked.connect(excluir_dados)
tela2.pushButton_3.clicked.connect(editar_dados)
tela1.show()
app.exec()
