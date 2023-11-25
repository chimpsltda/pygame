import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import threading

class MQTTConnection:
    def __init__(self):
        self.client = mqtt.Client()
        self.active = False

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe(self.nome)

    def connect_mqtt(self):
        # Additional MQTT connection logic goes here
        pass

    def create_room(self):
        opcao = input("Deseja criar uma sala? (s/n): ")
        if opcao == 's':
            self.nome = input("Digite o nome da sala: ")
            self.client.on_connect = self.on_connect
            self.client.connect("localhost", 1883, 60)  # Replace with your broker address
            threading.Thread(target=self.client.loop_forever).start()
        

        

