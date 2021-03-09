import uuid
import threading
import os
import sys
import time
#sys.path.append('C:/comgas/FIRMWARE/utils/lib')
sys.path.append('/home/pi/pitagoras/devops/comgas/FIRMWARE/utils/lib')
import vars
##Version 1.0
vars.Version="3.0"
import defs
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse

def app():
    try:
        print ("FIRMWARE "+Version+"\nStarting Services..." )
        #iothub connect
        print ("Connecting IoT Hub..." )
        client = defs.iothub_client_init()
        #provision device
        print ("Provisioning Device on IoT Hub...\n.\n." )
        defs.iothub_provision_device()
        #Paralel methods
        print ("Starting Listener method...\n.\n." )
        device_method_thread = threading.Thread(target=defs.device_method_listener, args=(vars.client,))
        device_method_thread.daemon = True
        device_method_thread.start()
        print ("Starting twin devices update method...\n.\n." )
        twin_update_listener_thread = threading.Thread(target=defs.twin_update_listener, args=(vars.client,))
        twin_update_listener_thread.daemon = True
        twin_update_listener_thread.start()
        ##Twin report patch
        reported_patch = {"FirmwareVersion": vars.Version}
        vars.client.patch_twin_reported_properties(reported_patch)
        if vars.registration_result.status == "assigned": print("Provision result: ", vars.registration_result.status)
        while True:
            defs.send_mqtt()
    except KeyboardInterrupt:
        print ( "App stopped")

if __name__ == '__main__':
    print ( "Starting App" )
    print ( "Press Ctrl-C to exit" )
    app()



