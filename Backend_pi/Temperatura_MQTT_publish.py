#teste de leitura de sensor com o MQTT 
#   Sensor de temperatura DS18B20 (EF52) Configurado como W1 (conexao one wire)
#   Pinagem no Raspberry:
#   terra= pino 9
#   vcc = pino 1 (3,3V)
#   porta = pino 11 (GPIO 17)

from time import sleep
from datetime import datetime
from os import system
import paho.mqtt.publish as publish
import RPi.GPIO as GPIO
from w1thermsensor import W1ThermSensor

GPIO.setmode(GPIO.BCM) 
sensor = W1ThermSensor()

def guardaData(data,dados):
    rel = open('Relatorio.csv','a')
    rel.write(data+'-'+dados+'\n')
    rel.close()
now = datetime.now()
while 1:
    try:
        relogio = datetime.now()
        contador = relogio - now
        agora = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
        temp = float(sensor.get_temperature())
        strtemp = format(temp,'.2f')
        send = strtemp
        print(send)
        publish.single("Deni/temp", send, hostname="test.mosquitto.org")
        if contador.seconds >= 60: # tempo de espera em segundos
            now = datetime.now()
            relogio = datetime.now()
            guardaData(agora,send)
    except Exception as e:
        print('Falha ao publicar temperatura')
        print(datetime.now())
        print(e)
