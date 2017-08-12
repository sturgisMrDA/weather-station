import time
import Adafruit_DHT
from gpiozero import Button, LED
import lcd

# Global constants
STATUS_LED_PIN = 25 # GPIO pin for {green} status led
ERROR_LED_PIN = 16 # GPIO pin for {red} error led
BUTTON_PIN = 24 # GPIO pin for push button.
DHT_PIN = 23 # GPIO pin for dht temp/humidity sensor
READ_INTERVAL = 2 # Seconds between data readings.
FILENAME = 'weather.txt'
FAHRENHEIT = True # Set to False for Celsius readings.
PRINT_DATA = False # Whether to echo data to screen.
PRINT_MESSAGES = False # Whether to echo messages to the screen.

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
    t_unit = 'F' if FAHRENHEIT else 'C'
    data_file.write('Time, Humidity (%), Temp (*' + t_unit + ')\n')
    data_file.close()
    return

def end_data_collection():
    """ Set logging to False to end data collection. """
    lcd.write_lines('Wrapping up...','',PRINT_MESSAGES)
    global logging
    logging = False
    error_led.on()
    return

# Main code
# Create Button and LED objects
push_button = Button(BUTTON_PIN)
status_led = LED(STATUS_LED_PIN)
error_led = LED(ERROR_LED_PIN)

# Create blank data file and write headers.
initialize_file(FILENAME)

# Initialize LCD screen.
lcd.init()

# Wait until button is pressed to begin recording data.
lcd.write_lines('Press button', 'to begin.',PRINT_MESSAGES)
push_button.wait_for_press()
time.sleep(1)
push_button.when_pressed = end_data_collection

# Collect data at intervals
lcd.write_lines('Collecting data.', 'Press to stop.',PRINT_MESSAGES)
time.sleep(3)
logging = True # Will be set to False when button is pressed.
while logging:
    status_led.on()
    humidity, temperature = get_reading()
    write_data(humidity, temperature)
    lcd.write_line("T: {} *{}".format(temperature,'F' if FAHRENHEIT else 'C'),1)
    lcd.write_line("H: {}%".format(humidity),2)
    status_led.off()
    time.sleep(READ_INTERVAL)

error_led.off()
lcd.write_lines('Done. Data in',FILENAME,PRINT_MESSAGES)
time.sleep(5)
lcd.clear()

