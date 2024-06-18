import cv2
import time
import json
import serial
from src.python.Storage import Storage
from src.python.ImageClassifier import ImageClassifier


def read_serial_data(ser):
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        if line:  # Ensure line is not empty
            try:
                sensor_data = json.loads(line)
                return sensor_data
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                print(f"Received line: {line}")
        else:
            print("Received empty line from serial port.")
    return None

def main():
    with open('setup.json', 'r') as json_file:
        setup = json.load(json_file)

    storage = Storage()
    storage.set_image_path(setup['path'])
    image_classifier = ImageClassifier()
    serial_connection = serial.Serial(setup['serial']['comPort'], 
                                      setup['serial']['baudrate'])
    
    stopwatch = time.time()
    interval = 60 # Detik

    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Error: Could not open video capture.")
        return

    sensor_data = None
    while camera.isOpened():
        ret, frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        classes = image_classifier.image_classification(gray)
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
            
            cv2.putText(frame, f"MQ2: {mq2_value}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            cv2.putText(frame, f"MQ7: {mq7_value}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            cv2.putText(frame, f"MQ131: {mq131_value}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            cv2.putText(frame, f"MQ136: {mq136_value}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            cv2.putText(frame, f"NO2: {no2_value}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            cv2.putText(frame, f"Temperature: {temperature}", (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            cv2.putText(frame, f"Humidity: {humidity}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            cv2.putText(frame, f"Dust: {dust_density}", (10, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            cv2.putText(frame, f"Kelas: {classes}", (10, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        cv2.imshow('Frame', frame)
        key = cv2.waitKey(1) & 0xFF 
        countdown = time.time() - stopwatch
        if key == 13 or (countdown > interval):
            storage.save_image_dataset(frame)
            stopwatch = time.time()
        if key == 27:
            break

    # Release resources
    camera.release()
    cv2.destroyAllWindows()
    serial_connection.close()

if __name__ == '__main__':
    main()