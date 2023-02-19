import sqlite3
import os
from datetime import datetime


simp_path = 'database/banco.db'
path = os.path.abspath(simp_path)

#-----------------------------------------------------Criar base de dados -------------------------------------------------------
def createBD():
        try:
            banco = sqlite3.connect(path)
            cursor = banco.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS dados(id INTEGER PRIMARY KEY AUTOINCREMENT, temperatura float,umidade float,indice float,data date)")
            banco.commit() 
            banco.close()
        except sqlite3.Error as erro:
            print("Erro ao criar tabela: ",erro)
            
        try:
            banco = sqlite3.connect(path)
            cursor = banco.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS configuracao(id INTEGER PRIMARY KEY AUTOINCREMENT, host varchar,porta varchar,email varchar,email_receber varchar,senha varchar,telefone interge)")
            banco.commit() 
            banco.close()
        except sqlite3.Error as erro:
            print("Erro ao criar tabela: ",erro)
        
        
 

#------------------------------------------------------------Sensor---------------------------------------------------------------     
#inserir na base dados SQLite       
def insert(temperatura,umidade,indice):
    data = datetime.now()
    data = data.strftime('%d/%m/%Y')
    
    try:
        banco = sqlite3.connect(path)
        cursor = banco.cursor()
        cursor.execute("INSERT INTO dados (temperatura,umidade,indice,data) VALUES ('"+temperatura+"','"+umidade+"','"+indice+"','"+data+"')")
        banco.commit() 
        banco.close()
        
    except sqlite3.Error as erro:
        print("Erro ao inserir os dados: ",erro)

 
#buscar todos os dados    
def select():
    try:
        banco = sqlite3.connect(path)
        cursor = banco.cursor()
        cursor.execute("SELECT * from dados")
        arrayItem = cursor.fetchall()
        banco.close()
        return arrayItem
        
    except sqlite3.Error as erro:
        print("Erro ao inserir os dados: ",erro)
        
def selectMax(coluna):
    try:
        banco = sqlite3.connect(path)
        cursor = banco.cursor()
        cursor.execute("Select Max("+coluna+") from dados")
        arrayItem = cursor.fetchone()
        banco.close()
        return arrayItem
        
    except sqlite3.Error as erro:
        print("Erro ao inserir os dados: ",erro)
    
#------------------------------------------------------------Configurações--------------------------------------------------------------- 

def deleteConfig():
    try:
        banco = sqlite3.connect(path)
        cursor = banco.cursor()
        cursor.execute("DELETE FROM configuracao")
        banco.commit() 
        banco.close()
        
    except sqlite3.Error as erro:
        print("Erro ao deletar os dados: ",erro)
 
   
def insertConfig(host,porta,email,email_receber,senha,telefone):
    try:
        banco = sqlite3.connect(path)
        cursor = banco.cursor()
        cursor.execute("INSERT INTO configuracao (host,porta,email,email_receber,senha,telefone) VALUES ('"+
                       host+"','"+
                       porta+"','"+
                       email+"','"+
                       email_receber+"','"+
                       senha+"','"+telefone+"')")
        banco.commit() 
        banco.close()
        
    except sqlite3.Error as erro:
        print("Erro ao inserir os dados: ",erro)

 
def selectConfig():
    try:
        banco = sqlite3.connect(path)
        cursor = banco.cursor()
        cursor.execute("SELECT * from configuracao")
        arrayItem = cursor.fetchall()
        banco.close()
        return arrayItem
        
    except sqlite3.Error as erro:
        print("Erro ao listar os dados: ",erro)   