import time
import Adafruit_ADS1x15

# Create the ADC 12 bit instance
adc = Adafruit_ADS1x15.ADS1015()

# Choose a gain depending on what range of voltages you expect
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
GAIN = 1

print('| Humidity | Light |')
while True:
    values = [0]*2
    for i in range(2):
        values[i] = adc.read_adc(i, gain=GAIN)
    print('| {0:>8} | {1:>5} |'.format(*values))
    time.sleep(0.5)
    