
#print("Start simulator (SITL)"
#import dronekit_sitl
#sitl = dronekit_sitl.start_default()
#connection_string = sitl.connection_string()
#connection_string = "/dev/serial/by-id/usb-3D_Robotics_PX4_FMU_v2.x_0-if00"
connection_string = "/dev/ttyUSB0,57600"
connection_string2 = "/dev/ttyUSB1,57600"

#connection_string = "/dev/ttyACM0,57600"
# Import DroneKit-Python
#from dronekit import connect, VehicleMode, CommandSequence, Command, mavutil, locations
from dronekit import *
import time,math


# Connect to the Vehicle.
print("Connecting to vehicle 1 on: %s" % (connection_string,))
#vehicle = connect(connection_string, wait_ready=True)
#vehicle = connect(connection_string, wait_ready=True, baud=57600)
vehicle = connect(connection_string)
#vehicle.battery = 4


print("Connecting to vehicle 2 on: %s" % (connection_string2,))
vehicle2 = connect(connection_string2)


# Get some vehicle attributes (state)
print("Get some vehicle 1 attribute values:")
print(" GPS: %s" % vehicle.gps_0)
print(" Battery: %s" % vehicle.battery)
print(" Last Heartbeat: %s" % vehicle.last_heartbeat)
print(" Armed?: %s" % vehicle.armed)
print(" Is Armable?: %s" % vehicle.is_armable)
print(" System status: %s" % vehicle.system_status.state)
print(" Mode: %s" % vehicle.mode.name)    # settable
#vehicle.mode = VehicleMode("MANUAL")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("Get some vehicle 2 attribute values:")
print(" GPS: %s" % vehicle2.gps_0)
print(" Battery: %s" % vehicle2.battery)
print(" Last Heartbeat: %s" % vehicle2.last_heartbeat)
print(" Armed?: %s" % vehicle2.armed)
print(" Is Armable?: %s" % vehicle2.is_armable)
print(" System status: %s" % vehicle2.system_status.state)
print(" Mode: %s" % vehicle2.mode.name)    # settable
print("\n\n")
def get_location_offset_meters(original_location, dNorth, dEast, alt):
    earth_radius=6378137.0 #Radius of "spherical" earth
    dLat = dNorth/earth_radius
    dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))
    newlat = original_location.lat + (dLat * 180/math.pi)
    newlon = original_location.lon + (dLon * 180/math.pi)
    return LocationGlobal(newlat, newlon,original_location.alt+alt)


#cmds = vehicle.commands
#cmds.clear()
#lat = -34.364114,
#lon = 149.166022
#altitude = 30.0
#cmd = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
#    0, 0, 0, 0, 0, 0,
#    lat, lon, altitude)
#cmds.add(cmd)
#cmds.upload()

# Set mode to guided - this is optional as the simple_goto method will change the mode if needed.


while vehicle.gps_0.fix_type < 3 or vehicle2.gps_0.fix_type < 3:
    print("V1 GPS %s" % vehicle.gps_0)
    print("V2 GPS %s" % vehicle2.gps_0)
    time.sleep(1)

print("V1 GPS %s" % vehicle.gps_0)
print("V1 GPS location: %s" % vehicle.location.global_frame)
print("V2 GPS %s" % vehicle2.gps_0)
print("V2 GPS location: %s" % vehicle2.location.global_frame)


home = vehicle.home_location
print("V1 Home: %s" % home)
home = vehicle.location.global_frame
home.alt = 30
vehicle.home_location = home
print("V1 Home: %s" % home)

home2 = vehicle2.home_location
print("V2 Home: %s" % home2)
home2 = vehicle2.location.global_frame
home2.alt = 30
vehicle2.home_location = home2
print("V2 Home: %s\n\n" % home2)


while (vehicle.mode != 'GUIDED' or vehicle2.mode != 'GUIDED'):
    print("Setting mode GUIDED for V1")
    vehicle.mode = VehicleMode("GUIDED")
    print("Setting mode GUIDED for V2")
    vehicle2.mode = VehicleMode("GUIDED")
    time.sleep(3)


time.sleep(5)

print("V1 Mode: %s" % vehicle.mode.name)
print("V2 Mode: %s" % vehicle2.mode.name)

while vehicle.armed != True or  vehicle2.armed != True:
    print("Arming vehicles")
    vehicle.armed = True
    vehicle2.armed = True
    time.sleep(3)

print("V1 is %s" % vehicle.armed)
print("V2 is %s" % vehicle2.armed)



#vehicle.simple_takeoff(vehicle.location.global_frame.alt + 15)
#print(" Taking off"
# time.sleep(5)
# print(" GPS location: %s" % vehicle.location.global_frame
# time.sleep(5)
# print(" GPS location: %s" % vehicle.location.global_frame
# time.sleep(5)
# print(" GPS location: %s" % vehicle.location.global_frame

print("Setting V1 (System status: %s)" % vehicle.system_status.state)
vehicle.system_status.state = "ACTIVE"
print("V1 System status: %s" % vehicle.system_status.state)


print("Setting V2 (System status: %s)" % vehicle2.system_status.state)
vehicle2.system_status.state = "ACTIVE"
print("V2 System status: %s" % vehicle2.system_status.state)

# # Set the LocationGlobal to head towards
# a_location = LocationGlobal(32.8271423,-83.6498889, 30)
# a_location2 = LocationGlobal(32.8271299,-83.6497213, 30)
# a_location3 = LocationGlobal(32.8269879,-83.6497682, 30)
# a_location4 = LocationGlobal(32.8269586,-83.6496784,30)
# a_location5 = LocationGlobal(32.8267986, -83.6497951,30)
# print("1st location created: %s " % a_location)
# print("2nd location created: %s " % a_location2)
# print("3rd location created: %s " % a_location3)
# print("4th location created: %s " % a_location4)
# print("5th location created: %s " % a_location5)
def goToLocation(latitude, longtitude):
    goTOLocation = LocationGlobal(latitude, longtitude, 30)
    print("Location created: %s " % goToLocation)

    time.sleep(10)
    print("Sending V1 to location %s" % goTOLocation)
    vehicle.simple_goto(goTOLocation)
    print("Sending V2 to location %s" % goTOLocation)
    vehicle2.simple_goto(goTOLocation)
    time.sleep(1)
    print("Sending V1 to location %s" % goTOLocation)
    vehicle.simple_goto(goTOLocation)
    print("Sending V2 to location %s" % goTOLocation)
    vehicle2.simple_goto(goTOLocation)
    time.sleep(1)
    print("Sending V1 to location %s" % goTOLocation)
    vehicle.simple_goto(goTOLocation)
    print("Sending V2 to location %s" % goTOLocation)
    vehicle2.simple_goto(goTOLocation)
    print("going")
    time.sleep(5)

    # count = 0
    print("V1 Home: %s" % home)
    print("V2 Home: %s" % home2)

    print("V1 GPS: %s" % vehicle.gps_0)
    print("V1 GPS location: %s" % vehicle.location.global_frame)
    print("V1 Last heartbeat: %s" % vehicle.last_heartbeat)
    print("V1 Is Armable?: %s" % vehicle.is_armable)
    print("V1 Armed?: %s" % vehicle.armed)
    print("V1 System status: %s" % vehicle.system_status.state)
    print("---------------------------------------------------")
    print("V2 GPS: %s" % vehicle2.gps_0)
    print("V2 GPS location: %s" % vehicle2.location.global_frame)
    print("V2 Last heartbeat: %s" % vehicle2.last_heartbeat)
    print("V2 Is Armable?: %s" % vehicle2.is_armable)
    print("V2 Armed?: %s" % vehicle2.armed)
    print("V2 System status: %s" % vehicle2.system_status.state)
    print("\n-----------------------------------------------------------------------------------------\n\n")


    while(vehicle.last_heartbeat < 29.0 and vehicle2.last_heartbeat < 29.0):
        # count += 1
        print("---------------------------------------------------------------------------------------")
        print("V1 GPS: %s" % vehicle.gps_0)
        print("V1 GPS location: %s" % vehicle.location.global_frame)
        print("V1 Last heartbeat: %s" % vehicle.last_heartbeat)
        print("V1 System status: %s" % vehicle.system_status.state)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("V2 GPS: %s" % vehicle2.gps_0)
        print("V2 GPS location: %s" % vehicle2.location.global_frame)
        print("V2 Last heartbeat: %s" % vehicle2.last_heartbeat)
        print("V2 System status: %s" % vehicle2.system_status.state)
        time.sleep(1.0)

    endItAll()


def endItAll():
    # Close vehicle object before exiting script
    vehicle.close()
    vehicle2.close()

    # Shut down simulator
    #sitl.stop()
    print("Completed")




def parseMessage(message):
    latitude = message[1:message.find(',')]
    longtitude = message[message.find(''):message.length()-1]
    goToLocation(float(latitude), float(longtitude))









































































"""Playing with tornado.websocket, to add markers to a Google Map using WebSockets
$ pip install tornado
$ python livemap.py --port=8888
Open http://localhost:8888 in one window
Each time http://localhost:8888/ping is opened in a second window, a
new marker is added to the map (at a random location)
Written with tornado==2.3
"""


import os
import json
import logging

import tornado.ioloop
import tornado.web
import tornado.websocket

from tornado.options import define, options


log = logging.getLogger(__name__)
WEBSOCKS = []


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect("/static/map.html")


class RandomLatLngSender(tornado.web.RequestHandler):
    """When an HTTP request is sent to /ping,
    this class sends a random lat/lng coord out
    over all websocket connections
    """

    def get(self):
        global WEBSOCKS
        log.debug("pinging: %r" % WEBSOCKS)

        import random
        # latlng = {#32.827695, -83.640428
        #     'lat': 32.827695
        #     'lng': -83.640428
        #     'title': "Thing!",
        # }
        latlng = {
            'lat': random.randint(30, 33),
            'lng': random.randint(-84, -82),
            'title': "Thing!",
        }   

        data = json.dumps(latlng)
        for sock in WEBSOCKS:
            sock.write_message(data)
        print(latlng)

class WebSocketBroadcaster(tornado.websocket.WebSocketHandler):
    """Keeps track of all websocket connections in
    the global WEBSOCKS variable.
    
    """
    def __init__(self, *args, **kwargs):
        super(EchoWebSocket, self).__init__(*args, **kwargs)

    def open(self):
        log.info("Opened socket %r" % self)
        print("Opened socket %r" % self)
        global WEBSOCKS
        WEBSOCKS.append(self)

    def on_message(self, message):
        log.info(u"Got message from websocket: %s" % message)
        print("Got message from websocket: %s" % message)

    def on_close(self):
        log.info("Closed socket %r" % self)
        print("Closed socket %r" % self)
        global WEBSOCKS
        WEBSOCKS.remove(self)

class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(u"You said: " + message)
        print("You said: "+message)
        parseMessage(message)

    def on_close(self):
        print("WebSocket closed")

settings = {
    # FIXME: Should really move maps.html into static/, and change the last
    # empty quotes to "static" (it's in same dir for gist)
    'static_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"),
}
print settings

application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/ping", RandomLatLngSender),
        (r"/sock", WebSocketBroadcaster),
        (r"/websocket", EchoWebSocket),
        ],
    **settings)


if __name__ == "__main__":
    define("port", default=8888, help="Run server on a specific port", type=int)
    tornado.options.parse_command_line()

    application.listen(options.port)
tornado.ioloop.IOLoop.instance().start()