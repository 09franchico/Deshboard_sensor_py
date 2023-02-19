from database import bd
import requests
import json

Token_msg = 'RTWQB7CUN1YOTCRESA0CI0HAU8E3JKQ39WLV230KCI3HWEHD6DWYREPM1AUVR2XWXJKWGRY5T4UFEYN1LA2BZFPB6GQU6XHA2ODD5FIZIQE5DDNNLW6RIM74ZBQMOFFV'

def configSMS(numero,msg):
    req = requests.get('https://api.smsdev.com.br/v1/send?key='+Token_msg+'&type=9&number='+numero+'&msg='+msg+'')
    res = json.loads(req.content)
    return res


def enviarMsg(u,t):
    config = bd.selectConfig()
    if len(config) == 1:
        for i in config:
            telefone = i[6]
        
        resposta = configSMS(str(telefone),''+u+'umidade e'+t+'ºC temperatura no local')
        if resposta["situacao"] == 'OK':
            print("Mensagem enviada com sucesso!!")
        
        if resposta['situacao'] == 'ERRO':
            print(resposta['descricao'])
    else:
        print('Configurações não implementado')
    
    


     
    