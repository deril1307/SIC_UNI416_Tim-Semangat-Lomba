import network
import time
import ujson
import urequests  
from umqtt.simple import MQTTClient
import dht
from machine import Pin, reset

# Konfigurasi WiFi
SSID = "Tes"
PASSWORD = "12345678"

# Konfigurasi MQTT Ubidots
TOKEN = "BBUS-mzlEnMdMD0suNuMSCuVqs9bv27vckv"
MQTT_BROKER = "industrial.api.ubidots.com"
MQTT_TOPIC = "/v1.6/devices/sensor_dht11"

# Konfigurasi Flask API Menggunakan HTTP Post ke flask_api.py
FLASK_API_URL = "http://192.168.238.79:5000/sensor"

# Inisialisasi WiFi
def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(SSID, PASSWORD)

    attempt = 0
    while not wifi.isconnected():
        print("Menghubungkan ke WiFi...")
        time.sleep(2)
        attempt += 1
        if attempt > 5:  # Jika lebih dari 5 kali maka akan restart ESP32
            print("Gagal konek WiFi! Restart ESP32...")
            reset()
    
    print("Terhubung ke WiFi!")
    return wifi

wifi = connect_wifi()
sensor = dht.DHT11(Pin(4))
PIR_PIN = Pin(5, Pin.IN)   
LED_PIN = Pin(2, Pin.OUT)  

# Koneksi MQTT ke Ubidots
def connect_mqtt():
    try:
        client = MQTTClient("ESP32", MQTT_BROKER, user=TOKEN, password=TOKEN, port=1883)
        client.connect()
        print("Terhubung ke MQTT!")
        return client
    except Exception as e:
        print(f"Gagal terhubung ke MQTT: {e}")
        return None

client = connect_mqtt()

# Looping untuk mengirim data
while True:
    try:
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()
        motion_detected = PIR_PIN.value()

        if motion_detected:
            LED_PIN.on()
            print("Gerakan Terdeteksi. LED ON")
        else:
            LED_PIN.off()
            print("Tidak ada gerakan. LED OFF")

        # dengan Format data JSON untuk dikirimkan
        data = {
            "temperature": temperature,
            "humidity": humidity,
            "motion": motion_detected
        }

        json_data = ujson.dumps(data)

        # Kirim data ke Ubidots via MQTT 
        if client:
            try:
                client.publish(MQTT_TOPIC, json_data)
                print(f"Mengirim ke Ubidots: {json_data}")
            except Exception as e:
                print(f"Gagal mengirim ke Ubidots: {e}")
                client = connect_mqtt()
        else:
            print("reconnect...")
            client = connect_mqtt()

        try:
            headers = {"Content-Type": "application/json"}
            response = urequests.post(FLASK_API_URL, json=data, headers=headers)
            print(f"Response Flask: {response.text}")
            response.close()
        except Exception:
            print("Flask belum berjalan!")

    except Exception as e:
        print(f"Terjadi kesalahan")

    time.sleep(3)
