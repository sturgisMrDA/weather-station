import time
import Adafruit_DHT
from gpiozero import Button, LED

def get_reading():
    sensor = Adafruit_DHT.DHT11
    humidity = None
    temperature = None
    while humidity is None or temperature is None:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, DHT_PIN)
        if humidity is None or temperature is None:
            error_led.on()
        else:
            error_led.off()
    # Temperature is C by default.  Change to F if indicated by FAHRENHEIT flag:
    if FAHRENHEIT:
        temperature = temperature * 9 / 5 + 32
    return (humidity, temperature)

def write_data(humidity, temperature):
    with open(FILENAME, 'a') as data_file:
        timestamp = time.ctime()
        data = timestamp + ', ' \
               + str(humidity) + ', ' \
               + str(temperature) 
        if PRINT_DATA:
            print(data)
        data_file.write(data+ '\n')
        data_file.close()
    return

def initialize_file(name):
    """ Create blank data file and write headers. """
    data_file = open(FILENAME, 'w')
    if FAHRENHEIT:
        t_unit = 'F'
    else:
        t_unit = 'C'
    data_file.write('Time, Humidity (%), Temp (*' + t_unit + ')\n')
    data_file.close()
    return

def end_data_collection():
    """ Set logging to False to end data collection. """
    print("Data collection halted.  Wrapping up...")
    global logging
    logging = False
    error_led.on()
    return

# Global constants
STATUS_LED_PIN = 25 # GPIO pin for {green} status led
ERROR_LED_PIN = 16 # GPIO pin for {red} error led
BUTTON_PIN = 24 # GPIO pin for push button.
DHT_PIN = 23 # GPIO pin for dht temp/humidity sensor
READ_INTERVAL = 0.5 # Seconds between data readings.
FILENAME = 'weather.txt'
FAHRENHEIT = True # Set to False for Celsius readings.
PRINT_DATA = False # Whether to print data to screen.

# Create Button and LED objects
push_button = Button(BUTTON_PIN)
status_led = LED(STATUS_LED_PIN)
error_led = LED(ERROR_LED_PIN)

# Create blank data file and write headers.
initialize_file(FILENAME)

# Wait until button is pressed to begin recording data.
print('Press button to begin collecting data.')
push_button.wait_for_press()
time.sleep(1)
push_button.when_pressed = end_data_collection

# Collect data at intervals
print('Collecting data. Press button to stop.')
logging = True # Will be set to False when button is pressed.
while logging:
    status_led.on()
    humidity, temperature = get_reading()
    write_data(humidity, temperature)
    status_led.off()
    time.sleep(READ_INTERVAL)

error_led.off()
print('Done.')

