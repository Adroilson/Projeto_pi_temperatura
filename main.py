# Criando uma interface mais complexa para o medidor de temperatura
# Esse programa é a aplicação que exibe os dados de temperatura enviados de um raspberry pi
# O raspberry faz a leitura e armazena as medidas catalogadas com data e hora 
# O envio da informação é feito atravez do protocolo mqtt ( internet das coisas )
# 
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.uix.vkeyboard import VKeyboard
from kivy.uix.textinput import TextInput
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from datetime import datetime
from Grafico import Graph, MeshLinePlot

class Home(BoxLayout):
    def __init__(self,tipo):
        super(Home,self).__init__()
        self.tipo = tipo
        self.orientation = 'vertical'
        self.retornagrafico()
        self.add_widget(self.graph)
        self.button_voltar = Button(text='Voltar',size_hint_y=0.1)
        self.button_dia = Button(text='Diario')
        self.button_mes = Button(text='Mês')
        self.button_ano = Button(text='Ano') 
        box_buttons = BoxLayout(size_hint_y=0.2)
        box_buttons.add_widget(self.button_dia)
        box_buttons.add_widget(self.button_mes)
        box_buttons.add_widget(self.button_ano)
        self.add_widget(box_buttons)
        self.add_widget(self.button_voltar)
        self.button_voltar.on_press = self.mudapagina # Para implementar desse jeito tem que tomar cuidado na ordem de criação de telas e das instancias dos widgets
                                                # Criar instancias do widget antes de definir as telas irá resultar em erro 
        self.button_dia.on_press = self.grafico_dia
        self.button_mes.on_press = self.grafico_mes
        self.button_ano.on_press = self.grafico_ano
        

    def retornagrafico(self):
        if self.tipo == 'dia':
            self.graph = Graph(xlabel='Hora', ylabel='Temperatura', x_ticks_minor=1,
                x_ticks_major=2,y_ticks_minor=1, y_ticks_major=1,
                y_grid_label=True, x_grid_label=True, padding=5,
                x_grid=True, y_grid=True, xmin=0, xmax=24, ymin=18, ymax=35)
            self.plot = MeshLinePlot(color=[0, 1, 0, 1])
            #self.plot.points = [(x, 25) for x in range(0, 35)]
            self.plot.points = [(0,0)]
            self.graph.add_plot(self.plot)

        if self.tipo == 'mes':
            self.graph = Graph(xlabel='Dia', ylabel='Temperatura', x_ticks_minor=1,
                x_ticks_major=1,y_ticks_minor=1, y_ticks_major=1,
                y_grid_label=True, x_grid_label=True, padding=5,
                x_grid=True, y_grid=True, xmin=1, xmax=31, ymin=18, ymax=35)
            self.plot = MeshLinePlot(color=[0, 1, 0, 1])
            self.plot.points = [(0,0)]
            self.graph.add_plot(self.plot)

        if self.tipo == 'ano':
            self.graph = Graph(xlabel='Mês', ylabel='Temperatura', x_ticks_minor=1,
                x_ticks_major=1,y_ticks_minor=1, y_ticks_major=1,
                y_grid_label=True, x_grid_label=True, padding=5,
                x_grid=True, y_grid=True, xmin=1, xmax=12, ymin=18, ymax=35)
            self.plot = MeshLinePlot(color=[0, 1, 0, 1])
            self.plot.points = [(0,0)]
            self.graph.add_plot(self.plot)

    def plotPointMaker(self,tipo):
        """ pega uma amostragem para exibir no grafico
            ainda é só para testes, a intenção é mostrar as médias
            """
        if len(buffer.pointsource) > 0:
            #hoje = datetime(2020, 12, 10, 23, 10, 4, 341749) # para testes
            hoje = datetime.today()
            plot = []
            if tipo == 'dia':
                cont = 0
                for ponto in buffer.pointsource:    #(datetime.datetime(2020, 12, 8, 23, 47, 7), 27.50)
                    if ponto[0].strftime('%d/%m/%Y') == hoje.strftime('%d/%m/%Y'): # se for do mesmo dia
                        if ponto[0].hour == cont:
                            plot.append((ponto[0].hour,ponto[1]))
                            cont+=1                 
                print('dia: ',plot)

            elif tipo == 'mes':
                for ponto in buffer.pointsource:    
                    if ponto[0].strftime('%m/%Y') == hoje.strftime('%m/%Y'): #se for do mesmo mes
                        cont = ponto[0].day  # inicia uma varredura a partir do dia mais antigo no mês atual
                        break
                for ponto in buffer.pointsource:    
                    if ponto[0].strftime('%m/%Y') == hoje.strftime('%m/%Y'): #se for do mesmo mes
                        if ponto[0].day == cont:
                            plot.append((ponto[0].day,ponto[1]))
                            cont+=1                 
                print('mes: ',plot)

            elif tipo == 'ano':
                for ponto in buffer.pointsource:    #(datetime.datetime(2020, 12, 8, 23, 47, 7), 27.50)
                    if ponto[0].strftime('%Y') == hoje.strftime('%Y'): #se for do mesmo mes
                        cont = ponto[0].month
                        break
                for ponto in buffer.pointsource:    #(datetime.datetime(2020, 12, 8, 23, 47, 7), 27.50)
                    if ponto[0].strftime('%Y') == hoje.strftime('%Y'): #se for do mesmo mes
                        if ponto[0].month == cont:
                            plot.append((ponto[0].month,ponto[1]))
                            cont+=1  
                print('ano :',plot)                 
            return plot
        else:
            return [(0,0)]

    def grafico_dia(self):
        Meuapp.screen_grafico.remove_widget(Meuapp.home)
        Meuapp.home = Home('dia')
        Meuapp.screen_grafico.add_widget(Meuapp.home) 
        Meuapp.home.plot.points = self.plotPointMaker('dia')
        Meuapp.home.graph.add_plot(Meuapp.home.plot)
       
    def grafico_mes(self):
        Meuapp.screen_grafico.remove_widget(Meuapp.home)
        Meuapp.home = Home('mes')
        Meuapp.screen_grafico.add_widget(Meuapp.home)
        Meuapp.home.plot.points = self.plotPointMaker('mes')
        Meuapp.home.graph.add_plot(Meuapp.home.plot)
    
    def grafico_ano(self):
        Meuapp.screen_grafico.remove_widget(Meuapp.home)
        Meuapp.home = Home('ano')
        Meuapp.screen_grafico.add_widget(Meuapp.home)
        Meuapp.home.plot.points = self.plotPointMaker('ano')
        Meuapp.home.graph.add_plot(Meuapp.home.plot)

    def mudapagina(self):
        Meuapp.screen_manager.current = "home"

class Pag1(BoxLayout):
    def __init__(self,**kwargs):
        super(Pag1,self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.label = Label(text = 'Temp',font_size=100)                                        
        self.add_widget(self.label)
        self.button = Button(text='Gráfico',size_hint_y=0.1)
        self.add_widget(self.button)
        Clock.schedule_interval(self.update,1)
        self.button.on_press = self.mudapagina # Para implementar desse jeito tem que tomar cuidado na ordem de criação de telas e das instancias dos widgets
                                                # Criar instancias do widget antes de definir as telas irá resultar em erro
    def mudapagina(self):
        publish.single("Deni/temp/requi",'OK', hostname="test.mosquitto.org")
        Meuapp.screen_manager.current = "grafico"
    
    def update(self,time):
        self.label.text = buffer.temp

class Login(BoxLayout): # a ser implementado
    ''' A ser implementado 
    '''
    def mudapagina(self):
        Meuapp.screen_manager.current = "home"

        

class TesteDeTelaApp(App):
    def build(self):
        self.screen_manager = ScreenManager() # Cria o objeto ScreenManager para controlar as paginas
        self.screen_pag1 = Screen(name="home") # Cria as paginas "Screen" com seus respectivos nomes, é obrigatorio ter um nome
        self.screen_grafico = Screen(name="grafico") #
        self.screen_manager.add_widget(self.screen_grafico) #
        self.screen_manager.add_widget(self.screen_pag1) # Adiciona as paginas criadas ao ScreenManager.
        self.home = Home('dia')  #
        self.pag1 = Pag1()  # Cria intancias dos widgets para serem adicionados a paginas
        self.screen_grafico.add_widget(self.home)   #
        self.screen_pag1.add_widget(self.pag1)   # Adiciona os widgets as suas paginas, nesse caso todos são BoxLayout 
        self.screen_manager.current = "home"    # define pagina inicial
        return self.screen_manager

class Buffer(object):
    def __init__(self, temp='0',dados = '0',pointsource = [] ):
        self.temp = temp
        self.dados = dados
        self.pointsource = pointsource

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("Deni/temp")

def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    buffer.temp = str(msg.payload)[2:-1]+' C'

def on_connect_data(client, userdata, flags, rc):
    print("Connected to receive data with result code "+str(rc))
    client.subscribe("Deni/temp/dados")
    
def on_message_data(client, userdata, msg):
    """ Aqui a mensagem é recebida e decodificada novamente para o formato [(datetimeObj,floatvalue)]
        ex: [(datetime.datetime(2020, 12, 8, 23, 47, 7), 27.50)] onde cada item da lista é uma tupla
        com dois itens: 
        * um objeto que guarda as informaçoes de data e hora da medição: (datetime.datetime(2020, 12, 8, 23, 47, 7)
        * um numero float que representa o valor medido, neste exemplo um valor de temperatura: 27.50
        
        Para transmissão dos dados é necessário transformar a informação em uma unica string. O publish recebe essa
        string e transforma em um array de bits, então quando ela chega no client deve ser tratada e transformada
        novamente para seu formato original.
        O array, quando transformado em string novamente acaba modificando o primeiro e o ultimo item da lista original
        (preciso estudar isso a fundo pra ter certeza) de modo que compromete esses dados na hora da conversão. Por hora
        eu adicionei valores descartaveis na string para não comprometer os dados recebidos.

        A mensagem é armazenada em buffer.dados ao ser recebida e é armazenada em buffer.pointsource a lista tratada
    """
    print(msg.topic+" recebeu dados! ")
    buffer.dados = str(msg.payload)
    listabruta = buffer.dados.split(',') # lista mas com data e temperatura no mesmo lugar
    #print('listabruta: ', listabruta[0]) # ["'08/12/2020-23:47:07-27.50'", " '08/12/2020-23:48:09-27.50'"]
    lista = [] # lista com data hora e temperatura separadas
    for item in listabruta:
        lista.append(item.split('-')) 
    #print('lista: ',lista[0:3]) # [['b"inicio '], ["'08/12/2020", '23:47:07', "27.50'"], [" '08/12/2020", '23:48:09', "27.50'"]]

    data_list = [] # Lista com data e hora como datetime object ( muito melhor ) e temperatura em uma tupla
    for item in lista:
        if item != lista[0] and item != lista[-1]: # exclui o primeiro e o ultimo item, preservando os dados.
            temp = item[2].replace("'","")
            date_obj = datetime.strptime(item[0][2:]+' '+item[1], '%d/%m/%Y %H:%M:%S')
            data_list.append((date_obj,float(temp)))
    #print('data_list: ',data_list[0]) # [(datetime.datetime(2020, 12, 8, 23, 47, 7), 27.50), (datetime.datetime(2020, 12, 8, 23, 48, 9), 27.50)]
    buffer.pointsource = data_list

buffer = Buffer()

client = mqtt.Client('P2')    
client.on_connect = on_connect
client.on_message = on_message

client_dados = mqtt.Client('dados')
client_dados.on_connect = on_connect_data
client_dados.on_message = on_message_data

client.connect("test.mosquitto.org", 1883, 60)
client_dados.connect("test.mosquitto.org", 1883, 60)
client.loop_start()
client_dados.loop_start()

Meuapp = TesteDeTelaApp()
Meuapp.run()