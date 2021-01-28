# -*- coding: utf-8 -*-

from netmiko import ConnectHandler
from pymongo import MongoClient
import urllib.parse
import json
import re
import time

def captura_mac_address(lista_de_switchs, user, password, collection_currency):

    validacao = re.compile(r"\w\w\w\w.\w\w\w\w.\w\w\w\w")
    chaves = ["Vlan", "Mac-address", "Type", "Port"]

    for switch in lista_de_switchs:
        lista = []
        device = {"host": switch,
            "username": user,
            "password": password,
            "device_type": "cisco_ios",
            }
        device = ConnectHandler(**device)
        device.enable()
        output = device.send_command(f"show mac address-table") #comando para chamar a tabela mac address dos dispositivos switchs
        for linha in output.split('\n'):
            search = validacao.search(linha)
            if search:
                teste = linha.split()
                if "Po1" not in teste and "Po2" not in teste and "CPU" not in teste and "Total" not in teste and "age" not in teste and "Secure" not in teste and "NTFY" not in teste:
                    if  len(teste) > 4: #caso esteja fazendo com switchs nexus,eles possuem campos adicionais que não são necessarios, portanto a variavel teste
                        #fica maior que 4, portanto, nesse ponto, o programa verifica se essa variavel é maiorq que 4, caso seja, ele exclui o adicional
                        teste.pop(0)
                        teste.pop(3)
                        teste.pop(4)
                        teste.pop(3)
                    estrutura = dict(zip(chaves, teste)) #cria a esturura de um dicionario
                    estrutura["ip"] = switch #cria um campo chamado "ip"
                    lista.append(estrutura)
                else:
                    pass
            else:
                pass
        collection_currency.insert_many(lista) #irá adicionar todos os switchs capiturados na collection criada
      
inicio = time.time()

usernamedb = urllib.parse.quote_plus("") #Digite o username do cluster criado no mongodb
passworddb =  urllib.parse.quote_plus("") ##Digite o password do cluster criado no mongodb
dbname = urllib.parse.quote_plus("")  ##Digite o nome do cluster do cluster criado no mongodb
mongourl = "mongodb+srv://"+usernamedb+":"+passworddb+"@macadress.x6hmp.mongodb.net/"+dbname+"?retryWrites=true&w=majority" #varivel obtida no proprio site
#cada pessoa tera uma chave de acesso disponibilizada pelo proprio mongoDB, consulte a documentação, essa chave é baseada na versão 3.11 ou superior do pymongo
client = MongoClient(mongourl) #variavel para conexão
db = client[""] #essa variavel ira criar um banco de dados, coloque o nome que desejar
if len(db.list_collection_names()) > 0: #irá checar se existe collections criados no banco de dados informado acima
    for collections in db.list_collection_names():
        client[""].drop_collection(collections) #coloque o nome do banco de dados criado acima
    else:
        pass
collection_currency = db[""] #cria uma collections com o nome passado como parametro
        
lista_de_switchs = [] # aqui precisa ser passado uma lista com o ip dos switchs que queira conectar via ssh
user = #insira o username para o acesso ssh
password = #insira a senha
captura_mac_address(lista_de_switchs, user, password, collection_currency) #chama a função
"""
lista_de_switchs = [] #campo opcional caso tenha switchs com usuario e senha diferentes
user = #idem variavel anterior
password = #idem variavel anterior
captura_mac_address(lista_de_switchs, user, password, collection_currency)
fim = time.time()
diferenca = fim - inicio
print(f"tempo de execucao {round(diferenca,2)}s") #item de suporte para saber quanto tempo está demorando para completar a tarefa
"""