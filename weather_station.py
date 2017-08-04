import time
import Adafruit_DHT

def get_reading():
    sensor = Adafruit_DHT.DHT11
    pin = 23
    humidity = None
    temperature = None
    while humidity is None or temperature is None:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    # temperature is C by default.  Change to F:
    temperature = temperature * 9 / 5 + 32
    return (humidity, temperature)

def write_data(humidity, temperature):
    with open(FILENAME, 'a') as data_file:
        timestamp = time.ctime()
        data = timestamp + ', ' \
               + str(humidity) + ', ' \
               + str(temperature) + '\n'
        data_file.write(data)
        data_file.close()
    return

READ_INTERVAL = 30 # Seconds between data readings.
FILENAME = 'weather.txt'
turned_on = True

data_file = open(FILENAME, 'w')
data_file.write('Time, Humidity (%), Temp (F)\n')
data_file.close()
while turned_on:
    humidity, temperature = get_reading()
    write_data(humidity, temperature)
    time.sleep(READ_INTERVAL)


