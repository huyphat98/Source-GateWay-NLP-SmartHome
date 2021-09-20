import eventlet
from flask import (
    Flask,
    render_template
)
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from lora import Lora
import serial

eventlet.monkey_patch()

ser = serial.Serial(
        port = '/dev/ttyAMA0',
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 2
    )

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'm16.cloudmqtt.com'
app.config['MQTT_BROKER_PORT'] = 10823
app.config['MQTT_USERNAME'] = 'qozkcyle'
app.config['MQTT_PASSWORD'] = '2cL7j6TDnqrF'
app.config['MQTT_REFRESH_TIME'] = 1.0

lora = Lora(ser)
mqtt = Mqtt(app)
socketio = SocketIO(app)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('id1')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    # emit a mqtt_message event to the socket containing the message data
    text = data['payload']
    try:
        if text == "bat_den":
            lora.lorasend(b"1")
            status=lora.lorareceive()

        elif text == "tat_den":
            lora.lorasend(b"2")
            status=lora.lorareceive()

        elif text == "bat_bom":
            lora.lorasend(b"3")
            status=lora.lorareceive()

        elif text == "tat_bom":
            lora.lorasend(b"4")
            status=lora.lorareceive()
        else:
            status = "error"
    except:
        status = "error"
    if status != "error":
        socketio.emit('mqtt_message', data=status)

@app.route('/', methods=['GET', 'POST'])
def index():
    lora.lorasend(b"5")
    first_status=lora.lorareceive()
    return render_template('receive.html', status=first_status)

@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    pass

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3000, use_reloader=False, debug=True)