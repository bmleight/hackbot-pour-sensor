import time
import datetime
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

LAST_FLOW_TIME = datetime.datetime.now()
IS_FLOWING = False

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # client.subscribe([("hackbot/drive", 0)])

client = mqtt.Client()
client.on_connect = on_connect

client.connect("hackbot-mqtt.local", 1883, 60)

client.loop_start()


def sensorCallback(channel):

    global IS_FLOWING, LAST_FLOW_TIME

    # Called if sensor output changes
    # timestamp = time.time()
    LAST_FLOW_TIME = datetime.datetime.now()
    # stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S:%f')
    
    # if GPIO.input(channel):
        # No magnet
        # print("Sensor HIGH " + stamp)
    # else:
        # Magnet
        # print("Sensor LOW " + stamp)
    
    if (not IS_FLOWING):
        client.publish("hackbot/flow-start")
        IS_FLOWING = True

GPIO.setmode(GPIO.BCM)

print("Setup GPIO pin as input on GPIO")

# Set Switch GPIO as input
# Pull high by default
GPIO.setup(17 , GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(17, GPIO.BOTH, callback=sensorCallback, bouncetime=200)


run = True
while run:

    cur_time = datetime.datetime.now()

    if (IS_FLOWING):

        diff = cur_time - LAST_FLOW_TIME
        if (diff.microseconds > 250000):
            
            IS_FLOWING = False
            client.publish("hackbot/flow-end")

    time.sleep(0.01)
    # client.publish("hackbot/status", json.dumps({"battery": robot.readmainbattery()}, sort_keys=True))
