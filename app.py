import cv2
import time
import json
import serial
from src.python.Storage import Storage
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

def text_image(text: str, value, image, position: tuple) -> None:
    """Menempelkan text ke image.
    
    Args:
        text (str): Judul dari text.
        value (any): Nilai yang ingin ditampilkan.
        image (cv2): Target gambar.
        position (tuple): Koordinat x dan y.
    """
    cv2.putText(image, f'{text}: {value}', (position[0], position[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

def main() -> None:
    """Bagian untuk dieksekusi."""
    # Inisialisasi mulai =======================================
    with open('setup.json', 'r') as json_file:
        setup = json.load(json_file)

    storage = Storage()
    storage.set_datasets_path(setup['path'])
    image_classifier = ImageClassifier()
    serial_connection = serial.Serial(setup['serial']['comPort'], 
                                      setup['serial']['baudrate'])
    camera = cv2.VideoCapture(0)
    stopwatch = time.time()
    interval = 60 # Detik
    sensor_data = None
    # Inisialisasi selesai =======================================

    # fungsi utama mulai =========================================
    while camera.isOpened():
        ret, frame = camera.read()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        classes = image_classifier.image_classification(frame_gray)
        if not ret:
            print("Error: Failed to capture frame from camera.")
            break

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

        text_image('MQ2', mq2_value, frame, (10, 30))
        text_image('MQ7', mq7_value, frame, (10, 50))
        text_image('MQ131', mq131_value, frame, (10, 70))
        text_image('MQ136', mq136_value, frame, (10, 90))
        text_image('NO2', no2_value, frame, (10, 110))
        text_image('Temperature', temperature, frame, (10, 130))
        text_image('Humidity', humidity, frame, (10, 150))
        text_image('Dust', dust_density, frame, (10, 170))
        text_image('Class', classes, frame, (10, 190))

        cv2.imshow('Frame', frame)
        key = cv2.waitKey(1) & 0xFF 
        countdown = time.time() - stopwatch

        if key == 13 or (countdown > interval):
            storage.save_image_dataset(frame)
            storage.save_pandas_dataframe(sensor_data)
            stopwatch = time.time()

        if key == 27:
            break

    camera.release()
    cv2.destroyAllWindows()
    serial_connection.close()
    # fungsi utama selesai =======================================


if __name__ == '__main__':
    main()