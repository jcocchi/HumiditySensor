import re
import sys
import time
import random
import Adafruit_ADS1x15
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue

MESSAGE_TIMEOUT = 10000

# global counters
MESSAGE_COUNT = 0
TWIN_CONTEXT = 0
SEND_REPORTED_STATE_CONTEXT = 0
SEND_CALLBACKS = 0
TWIN_CALLBACKS = 0
SEND_REPORTED_STATE_CALLBACKS = 0

# chose HTTP, AMQP or MQTT as transport protocol
PROTOCOL = IoTHubTransportProvider.MQTT

# ADC Variables
HUMIDITY_CHANNEL = 0
LIGHT_CHANNEL = 1
MAX_READING_VAL = 2047

# Set up message skeleton
MSG_TXT = "{\"deviceId\": \"Raspberry Pi - Python\",\"light\": %f,\"hum\": %f}"

# Verify that the connection string is present and correct
if len(sys.argv) < 2:
    print ( "You need to provide the device connection string as command line arguments." )
    sys.exit(0)

def is_correct_connection_string():
    m = re.search("HostName=.*;DeviceId=.*;", CONNECTION_STRING)
    if m:
        return True
    else:
        return False

CONNECTION_STRING = sys.argv[1]

if not is_correct_connection_string():
    print ( "Device connection string is not correct." )
    sys.exit(0)


def send_confirmation_callback(message, result, user_context):
    global SEND_CALLBACKS
    print ( "Confirmation[%d] received for message with result = %s" % (user_context, result) )
    SEND_CALLBACKS += 1
    print ( "    Total calls confirmed: %d" % SEND_CALLBACKS )


def device_twin_callback(update_state, payload, user_context):
    global TWIN_CALLBACKS
    print ( "\nTwin callback called with:\nupdateStatus = %s\npayload = %s\ncontext = %s" % (update_state, payload, user_context) )
    TWIN_CALLBACKS += 1
    print ( "Total calls confirmed: %d\n" % TWIN_CALLBACKS )


def send_reported_state_callback(status_code, user_context):
    global SEND_REPORTED_STATE_CALLBACKS
    print ( "Confirmation for reported state received with:\nstatus_code = [%d]\ncontext = %s" % (status_code, user_context) )
    SEND_REPORTED_STATE_CALLBACKS += 1
    print ( "    Total calls confirmed: %d" % SEND_REPORTED_STATE_CALLBACKS )


# Convert 12 bit reading to percent
def convert_to_percent(value):
    return 100 - ((float(value) / MAX_READING_VAL) * 100)


def iothub_client_init():
    # prepare iothub client
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
 
    # set options
    client.set_option("messageTimeout", MESSAGE_TIMEOUT)
    client.set_option("logtrace", 0)

    # set callbacks
    client.set_device_twin_callback(
        device_twin_callback, TWIN_CONTEXT)
        
    return client


def iothub_client_sample_run():
    try:
        client = iothub_client_init()

        reported_state = "{\"newState\":\"standBy\"}"
        client.send_reported_state(reported_state, len(reported_state), send_reported_state_callback, SEND_REPORTED_STATE_CONTEXT)

        adc = Adafruit_ADS1x15.ADS1015()

        while True:
            global MESSAGE_COUNT
            # send a few messages every minute
            print ( "IoTHubClient sending %d messages" % MESSAGE_COUNT )

            # read the sensor values for light and humidity
            light = convert_to_percent(adc.read_adc(LIGHT_CHANNEL))
            humidity = convert_to_percent(adc.read_adc(HUMIDITY_CHANNEL))
                
            # format, print, and send the message
            msg_txt_formatted = MSG_TXT % (
                light,
                humidity)
            print (msg_txt_formatted)
            message = IoTHubMessage(msg_txt_formatted)
            client.send_event_async(message, send_confirmation_callback, MESSAGE_COUNT)

            # verify the message was sent
            status = client.get_send_status()
            print ( "Send status: %s" % status )
            MESSAGE_COUNT += 1
            time.sleep(2)

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )


if __name__ == "__main__":
    print ( "IoT Hub Client for Python" )

    iothub_client_sample_run()