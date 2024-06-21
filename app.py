import cv2
import time
import json
import serial
import numpy as np
import pandas as pd
from picamera2 import Picamera2
from src.python.Storage import Storage
from src.python.RequestPost import RequestPost
from sklearn.neighbors import KNeighborsClassifier
from src.python.ImageClassifier import ImageClassifier


def read_serial_data(serial: serial) -> dict:
    """Membaca data serial dari sensor.
    
    Args:
        serial (serial): Komunikasi serial.
    
    Returns:
        dict: Data sensor dalam bentuk format json.
    """
    if serial.in_waiting > 0:
        line = serial.readline().decode('utf-8').strip()
        if line:
            try:
                sensor_data = json.loads(line)
                return sensor_data
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                print(f"Received line: {line}")
        else:
            print("Received empty line from serial port.")
    return None

def text_image(text: str, value, image, position: tuple, code: str = 'B') -> None:
    """Menempelkan text ke image.
    
    Args:
        text (str): Judul dari text.
        value (any): Nilai yang ingin ditampilkan.
        image (cv2): Target gambar.
        position (tuple): Koordinat x dan y.
        code (str, optional): Kode untuk warna text. Default 'B' (Biru). Gunakan 'W' (Putih).
    """
    if code == 'W':
        color = (255, 255, 255)
    elif code == 'B':
        color = (255, 0, 0)
    elif code =='G':
        color = (0, 255, 0)

    cv2.putText(image, f'{text}: {value}', (position[0], position[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

def main() -> None:
    """Bagian untuk dieksekusi."""
    # Inisialisasi mulai =======================================
    with open('setup.json', 'r') as json_file:
        setup = json.load(json_file)

    storage = Storage()
    storage.set_datasets_path(setup['path'])
    send_post = RequestPost(setup['urlAPI'])
    image_classifier = ImageClassifier()
    serial_connection = serial.Serial(setup['serial']['comPort'], 
                                      setup['serial']['baudrate'])
    
    camera = Picamera2()
    camera.preview_configuration.main.size=(640,480)
    camera.preview_configuration.main.format='RGB888'
    camera.start()
    stopwatch = time.time()
    interval = 60 # Detik
    sensor_data = None
    count = 0

    # Datasets
    data = pd.read_csv(storage.get_pandas_dataset())
    x = data[['mq2', 'mq7', 'mq131', 'mq136', 'no2', 'temperature', 'humidity', 'dust']].values
    y = data['status'].values
    knn = KNeighborsClassifier()
    knn.fit(x, y)
    # Inisialisasi selesai =======================================

    # fungsi utama mulai =========================================
    while True:
        raw_frame = camera.capture_array()
        frame_gray = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2GRAY)
        classes = image_classifier.image_classification(frame_gray)

        new_sensor_data = read_serial_data(serial_connection)
        if new_sensor_data:
            sensor_data = new_sensor_data

        if sensor_data:
            mq2_value = sensor_data.get('MQ2', 'N/A')
            mq7_value = sensor_data.get('MQ7', 'N/A')
            mq131_value = sensor_data.get('MQ131', 'N/A')
            mq136_value = sensor_data.get('MQ136', 'N/A')
            no2_value = sensor_data.get('NO2', 'N/A')
            temperature = sensor_data.get('Temperature', 'N/A')
            humidity = sensor_data.get('Humidity', 'N/A')
            dust_density = sensor_data.get('Dust', 'N/A')
        
        # Prediksi
        data_sensor_test = np.array([
            [mq2_value, mq7_value, mq131_value, mq136_value, 
            no2_value, temperature, humidity,  dust_density]
        ])
        predict_result = knn.predict(data_sensor_test)[0]

        # Pojok Kiri atas
        frame = raw_frame.copy()
        text_image('CO2', mq2_value, frame, (10, 30))
        text_image('CO', mq7_value, frame, (10, 50))
        text_image('O3', mq131_value, frame, (10, 70))
        text_image('SO2', mq136_value, frame, (10, 90))
        text_image('NO2', no2_value, frame, (10, 110))
        text_image('Temperature', temperature, frame, (10, 130))
        text_image('Humidity', humidity, frame, (10, 150))
        text_image('PM10', dust_density, frame, (10, 170))

        # Pojok kanan bawah
        text_image('Lokasi', setup['lokasi'], frame, (450, 400), code='W')
        text_image('Class', classes, frame, (450, 420), code='W')
        text_image('Kualitas', predict_result, frame, (450, 440), code='W')

        # Pojok kanan atas
        display_frame = frame.copy()
        text_image('Gambar', count, display_frame, (430, 30), code='W')
        text_image('ESC', 'Keluar Program', display_frame, (430, 50), code='W')
        text_image('Enter', 'Ambil Data', display_frame, (430, 70), code='W')

        cv2.imshow('GUI versi Alpha', display_frame)
        key = cv2.waitKey(1) & 0xFF 
        countdown = time.time() - stopwatch

        if key == 13 or (countdown > interval):
            status_raw = storage.save_image_dataset(raw_frame, setup['lokasi'], count, 'raw')
            status_send = storage.save_image_dataset(frame, setup['lokasi'], count, 'send')

            if status_send:
                data_sensor_send = {
                    'pm10':int(dust_density),
                    'no2':no2_value,
                    'so2':mq136_value,
                    'co2':mq2_value,
                    'co':mq7_value,
                    'o3':mq131_value,
                    's_gambar':classes,
                    's_sensor':predict_result,
                    'temp':temperature,
                    'huma':humidity,
                    'id_pin':1
                }
                send_post.post(data=data_sensor_send, image_path=status_send)
            else:
                print('No path image')

            stopwatch = time.time()
            count += 1

        if key == 27:
            break

    camera.stop()
    cv2.destroyAllWindows()
    serial_connection.close()
    # fungsi utama selesai =======================================


if __name__ == '__main__':
    main()