import time
import Adafruit_ADS1x15

# Create an ADS1015 ADC (12-bit) instance.
adc = Adafruit_ADS1x15.ADS1015()
humidityChannel = 0
maxVal = 2047

print('Reading humidity values...')
while True:
    # Read proper ADC channel value
    temp = adc.read_adc(humidityChannel)
    print(100 - (float(temp) / maxVal) * 100)
    time.sleep(5)
