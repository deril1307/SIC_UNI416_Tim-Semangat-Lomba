# SIC_UNI416_Tim-Semangat-Lomba

# SENSOR :
1. DHT 11 : Suhu Dan Kelembapan.

2. Pir Sensor : Untuk mendeteksi Gerakan / Motion

## 📌 Penjelasan Kodingan
Berikut adalah penjelasan dari setiap file dalam proyek ini:

1. **`dht_mqtt.py`**  
   📡 Digunakan untuk script ESP32 yang mengirimkan data ke Ubidots untuk visualisasi.  
2. **`flask_api.py`**  
   🔗 Digunakan untuk menerima dan mengirimkan data ke MongoDB.  
3. **`delete.py`**  
   ❌ Digunakan untuk menghapus koleksi data di MongoDB.  

## 🔒 Keamanan
- **`.gitignore`** digunakan untuk menyembunyikan informasi sensitif seperti **username dan password** dari MongoDB.  
- Pastikan file `.env` tidak di-commit ke repository untuk menjaga keamanan data.

## 🚀 Cara Menjalankan
1. Clone repository ini:
   ```sh
   git clone https://github.com/username/repository.git
