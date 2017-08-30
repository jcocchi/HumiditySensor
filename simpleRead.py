import time
import Adafruit_ADS1x15

# Create the ADC 12 bit instance
adc = Adafruit_ADS1x15.ADS1015()

# Max reading value for 12 bit instance
MAX_READING_VAL = 2047

# Choose a gain depending on what range of voltages you expect
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
GAIN = 1

# Define channels each sensor is connected to
HUMIDITY_CHANNEL = 0
LIGHT_CHANNEL = 1

# Convert 12 bit reading to percent
def convert_to_percent(value):
    return 100 - ((float(value) / MAX_READING_VAL) * 100)

print '| Humidity | Light |'
print '--------------------'
while True:
    values = [0]*2

    # Read from channel 0 for the humidity value
    values[0] = convert_to_percent(adc.read_adc(HUMIDITY_CHANNEL, gain=GAIN))
    # Read from channel 1 for the light value
    values[1] = convert_to_percent(adc.read_adc(LIGHT_CHANNEL, gain=GAIN))

    print '| {0:>8} | {1:>5} |'.format(*values)
    time.sleep(0.5)
