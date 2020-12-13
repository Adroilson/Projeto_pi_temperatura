#!/usr/bin/python
# -*- coding: UTF-8 -*-
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from datetime import datetime

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("Deni/temp/requi")

def on_message(client, userdata, msg):
    print(msg.topic+" recebeu a requisicao "+str(msg.payload))    
    rel = open('Relatorio.csv','r')
    bruto = rel.readlines()
    valores = []
    for valor in bruto:
        valores.append(valor[:-1]) # valor[:-1 pra tirar o \n da string, pra minha surpresa é apenas um char, não dois]
    string = 'inicio ,'+str(valores).strip('[]')+' , fim' # string unica que deve ser enviada, "inicio" e "fim" são destruidos depois da transmissão
    publish.single("Deni/temp/dados", string, hostname="test.mosquitto.org")
    print(string)

client = mqtt.Client('backend')    
client.on_connect = on_connect
client.on_message = on_message
client.connect("test.mosquitto.org", 1883, 60)
client.loop_forever()