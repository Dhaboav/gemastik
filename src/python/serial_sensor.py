import serial
import json

# Configure serial port
ser = serial.Serial() 

while True:
    if ser.in_waiting > 0:
        # Read line from serial
        line = ser.readline().decode('utf-8').strip()
        
        try:
            # Parse JSON data
            sensor_data = json.loads(line)
            
            # Access sensor values
            mq2_value = sensor_data['MQ2']
            mq7_value = sensor_data['MQ7']
            mq131_value = sensor_data['MQ131']
            mq136_value = sensor_data['MQ136']
            no2_value = sensor_data['NO2']
            temperature = sensor_data['Temperature']
            humidity = sensor_data['Humidity']
            dust_density = sensor_data['Dust']
            
            # Print or process sensor values
            print(sensor_data)
            
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")