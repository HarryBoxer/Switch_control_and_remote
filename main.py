import time
import network
import _thread
from machine import Pin, PWM
from umqtt.robust import MQTTClient

led = Pin(5,Pin.OUT)
        # led.value(0) เปิด
        # led.value(1) ปิด
sw = Pin(22,Pin.IN)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
print("*** Connecting to WiFi...")
wlan.connect("KUWIN","")
while not wlan.isconnected():
    time.sleep(0.5)
print("*** Wifi connected")

def sub_callback(topic, payload):
    if topic == b"ku/cpe/karn/light":
        try:
            # print(payload)
            led.value(1 - int(payload))
        except ValueError:
            pass

mqtt = MQTTClient("karn5555555555","ecourse.cpe.ku.ac.th")
print("*** Connecting to MQTT broker...")
mqtt.connect()
print("*** MQTT broker connected")
mqtt.set_callback(sub_callback)
mqtt.subscribe(b"ku/cpe/karn/light")

def check_switch():
    while True:
        while sw.value() == 1:
            time.sleep_ms(0)

        time.sleep_ms(100)
        led.value(1 - led.value())
        mqtt.publish("ku/cpe/karn/light", str(1 - led.value()))

        while sw.value() == 0:
            time.sleep_ms(0)
            
        time.sleep_ms(100)

def check_mqtt():
    # mqtt.check_msg()
    while True:
        mqtt.check_msg()
        time.sleep_ms(0)

_thread.start_new_thread(check_mqtt, [])
_thread.start_new_thread(check_switch, [])

while True:
    time.sleep(1)

# def sub_callback(topic,payload):
