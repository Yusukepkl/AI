# mqtt_iot.py
import paho.mqtt.client as mqtt
from config import config
from logger import logger

# Renomeia variável para evitar shadowing
mqtt_client = mqtt.Client()

# Callbacks com parâmetros não usados prefixados para silenciar avisos

def on_connect(_client, _userdata, _flags, _rc):
    """
    Conectado ao broker MQTT. Inscreve nos tópicos desejados.
    """
    logger.info(f'MQTT connected with result code {_rc}')
    mqtt_client.subscribe('lia/commands')
    mqtt_client.subscribe('lia/control')


def on_message(_client, _userdata, msg):
    """
    Recebe mensagens MQTT e encaminha ao logger ou fila.
    """
    logger.info(f'MQTT message on {msg.topic}: {msg.payload}')
    # Aqui você pode encaminhar msg.payload para sua fila de comandos

# Associa callbacks ao cliente
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Conecta e inicia loop em background
mqtt_client.connect(config.MQTT_BROKER, 1883, 60)
mqtt_client.loop_start()


def mqtt_publish(topic: str, payload: bytes) -> None:
    """
    Publica uma mensagem no tópico MQTT especificado.
    """
    mqtt_client.publish(topic, payload)
    logger.debug(f'MQTT published to {topic}: {payload}')
