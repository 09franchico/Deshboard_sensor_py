from PyQt5 import  uic,QtWidgets
from threading import Thread
from threading import Event
from database import bd
from src.services import sms,emailGoogle
import serial
import t as graf


global verificar
verificar = False

event = Event()

#banco de dados
bd.createBD()

def inicarColeta():
    global verificar
    global event
    global arduino
    verificar = True
    
    def inicar(event):
        arduino = serial.Serial('COM3',9600)
        notificar = []
        while verificar:
            linha = str(arduino.readline())
            linha = linha[2:-5]
            dados = linha.split('e')
            bd.insert(dados[1],dados[0],dados[2])
            
            #envio de mensagem
            if float(dados[1])>20 and len(notificar) == 0:
                 notificar.append(1)
                 sms.enviarMsg(dados[0],dados[1])
                 emailGoogle.envioEmail(dados[0],dados[1])
            if(float(dados[1])>40 and len(notificar) == 1):
                 notificar.append(2)
                 sms.enviarMsg(dados[0],dados[1])
                 emailGoogle.envioEmail(dados[0],dados[1])
            if(float(dados[1])>50 and len(notificar) == 2):
                 notificar.append(3)
                 sms.enviarMsg(dados[0],dados[1])
                 emailGoogle.envioEmail(dados[0],dados[1])
                 
            #visualizar os dados no destboard
            destboard.lb_umi.setText(dados[0])
            destboard.lb_temp.setText(dados[1])
            destboard.lb_indece.setText(dados[2])
        
        if event.is_set():
                arduino.close()
            
    #criar e configurar um novo thread
    thread = Thread(target=inicar, args=(event,),name='minhaThread')
    thread.start()
  
def stop():
    global verificar
    verificar = False
    event.set()
    print('STOP!')

#----------------------------------------------------------configuração-----------------------------------------------------

def config():
    cadastro.show()
    dados = bd.selectConfig()
    cadastro.lb_error.setText("")
    if len(dados) > 0:
        for i in dados:
            cadastro.edit_host.setText(str(i[1]))
            cadastro.edit_porta.setText(str(i[2]))
            cadastro.edit_email.setText(str(i[3]))
            cadastro.edit_emailr.setText(str(i[4]))
            cadastro.edit_senha.setText(str(i[5]))
            cadastro.edit_telefone.setText(str(i[6]))
    
def salvarConfig():
    host = cadastro.edit_host.text()
    porta = cadastro.edit_porta.text()
    email = cadastro.edit_email.text()
    emailReceber = cadastro.edit_emailr.text()
    senha = cadastro.edit_senha.text()
    telefone = cadastro.edit_telefone.text()
     
    if(host !='' and porta !='' and email !='' and emailReceber != '' and senha != '' and telefone!=''):
        #salva na base de dados
        bd.deleteConfig()
        bd.insertConfig(host,porta,email,emailReceber,senha,telefone)
        cadastro.edit_host.setText("")
        cadastro.edit_porta.setText("")
        cadastro.edit_email.setText("")
        cadastro.edit_emailr.setText("")
        cadastro.edit_senha.setText("")
        cadastro.edit_telefone.setText("")
        cadastro.lb_error.setText("")
        cadastro.close()
    else:
        cadastro.lb_error.setText("Preencha todos os campos.")

def Grafico():
    graf.window.show()


#---------------------------------------------------------chamadas de telas ----------------------------------------------------    
app= QtWidgets.QApplication([])
destboard=uic.loadUi("src/view/destboard.ui")
cadastro = uic.loadUi("src/view/cadastro.ui")
destboard.iniciar.clicked.connect(inicarColeta)
destboard.actiondados.triggered.connect(config)
destboard.actionTemp_umid.triggered.connect(Grafico)
destboard.stop.clicked.connect(stop)
cadastro.btn_cadastrar.clicked.connect(salvarConfig)

destboard.show()
app.exec()

