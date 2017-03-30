
#print "Start simulator (SITL)"
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
print "Get some vehicle 1 attribute values:"
print " GPS: %s" % vehicle.gps_0
print " Battery: %s" % vehicle.battery
print " Last Heartbeat: %s" % vehicle.last_heartbeat
print " Armed?: %s" % vehicle.armed
print " Is Armable?: %s" % vehicle.is_armable
print " System status: %s" % vehicle.system_status.state
print " Mode: %s" % vehicle.mode.name    # settable
#vehicle.mode = VehicleMode("MANUAL")
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "Get some vehicle 2 attribute values:"
print " GPS: %s" % vehicle2.gps_0
print " Battery: %s" % vehicle2.battery
print " Last Heartbeat: %s" % vehicle2.last_heartbeat
print " Armed?: %s" % vehicle2.armed
print " Is Armable?: %s" % vehicle2.is_armable
print " System status: %s" % vehicle2.system_status.state
print " Mode: %s" % vehicle2.mode.name    # settable
print "\n\n"
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
	print "V1 GPS %s" % vehicle.gps_0
	print "V2 GPS %s" % vehicle2.gps_0
	time.sleep(1)

print "V1 GPS %s" % vehicle.gps_0
print "V1 GPS location: %s" % vehicle.location.global_frame
print "V2 GPS %s" % vehicle2.gps_0
print "V2 GPS location: %s" % vehicle2.location.global_frame


home = vehicle.home_location
print "V1 Home: %s" % home
home = vehicle.location.global_frame
home.alt = 30
vehicle.home_location = home
print "V1 Home: %s" % home

home2 = vehicle2.home_location
print "V2 Home: %s" % home2
home2 = vehicle2.location.global_frame
home2.alt = 30
vehicle2.home_location = home2
print "V2 Home: %s\n\n" % home2



while vehicle.mode != 'GUIDED' or vehicle2.mode != 'GUIDED':
 	print("Setting mode GUIDED for V1")
	vehicle.mode = VehicleMode("GUIDED")
	print("Setting mode GUIDED for V2")
	vehicle2.mode = VehicleMode("GUIDED")
	time.sleep(3)


time.sleep(5)

print "V1 Mode: %s" % vehicle.mode.name
print "V2 Mode: %s" % vehicle2.mode.name

while vehicle.armed != True or  vehicle2.armed != True:
	print "Arming vehicles"
	vehicle.armed = True
	vehicle2.armed = True
	time.sleep(3)

print "V1 is %s" % vehicle.armed
print "V2 is %s" % vehicle2.armed



#vehicle.simple_takeoff(vehicle.location.global_frame.alt + 15)
#print " Taking off"
# time.sleep(5)
# print " GPS location: %s" % vehicle.location.global_frame
# time.sleep(5)
# print " GPS location: %s" % vehicle.location.global_frame
# time.sleep(5)
# print " GPS location: %s" % vehicle.location.global_frame

print "Setting V1 (System status: %s)" % vehicle.system_status.state
vehicle.system_status.state = "ACTIVE"
print "V1 System status: %s" % vehicle.system_status.state


print "Setting V2 (System status: %s)" % vehicle2.system_status.state
vehicle2.system_status.state = "ACTIVE"
print "V2 System status: %s" % vehicle2.system_status.state

# Set the LocationGlobal to head towards
a_location = LocationGlobal(32.8271423,-83.6498889, 30)
a_location2 = LocationGlobal(32.8271299,-83.6497213, 30)
a_location3 = LocationGlobal(32.8269879,-83.6497682, 30)
a_location4 = LocationGlobal(32.8269586,-83.6496784,30)
a_location5 = LocationGlobal(32.8267986, -83.6497951,30)
print "1st location created: %s " % a_location
print "2nd location created: %s " % a_location2
print "3rd location created: %s " % a_location3
print "4th location created: %s " % a_location4
print "5th location created: %s " % a_location5

goTOLocation = a_location5
time.sleep(10)
print "Sending V1 to location %s" % goTOLocation
vehicle.simple_goto(goTOLocation)
print "Sending V2 to location %s" % goTOLocation
vehicle2.simple_goto(goTOLocation)
print "Sending V1 to location %s" % goTOLocation
vehicle.simple_goto(goTOLocation)
print "Sending V2 to location %s" % goTOLocation
vehicle2.simple_goto(goTOLocation)
print "Sending V1 to location %s" % goTOLocation
vehicle.simple_goto(goTOLocation)
print "Sending V2 to location %s" % goTOLocation
vehicle2.simple_goto(goTOLocation)
print "going"
time.sleep(5)

#home = vehicle.location.global_frame
#wp = get_location_offset_meters(home, 0, 0, 10);
#cmd = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)



#print " count: %s" % currcmds.count
#loc = LocationGlobalRelative(34.364114,-84.166022,30.0)
#print " Made location %s" % loc
# currcmds = vehicle.commands
#print " vehicle.commands"
#print " count: %s" % currcmds.count
#currcmds.clear()
#print " clear()"
#currcmds.add(cmd)
#print " add(location)"
#print " count: %s" % currcmds.count
#currcmds.upload()
#print " Uploading...."
#time.sleep(5)
#currcmds.download()
#currcmds.waitReady()
# print " current num of commands: %s" % currcmds.count
count = 0
print "V1 Home: %s" % home
print "V2 Home: %s" % home2

print "V1 GPS: %s" % vehicle.gps_0
print "V1 GPS location: %s" % vehicle.location.global_frame
print "V1 Last heartbeat: %s" % vehicle.last_heartbeat
print "V1 Is Armable?: %s" % vehicle.is_armable
print "V1 Armed?: %s" % vehicle.armed
print "V1 System status: %s" % vehicle.system_status.state
print "V2 GPS: %s" % vehicle2.gps_0
print "V2 GPS location: %s" % vehicle2.location.global_frame
print "V2 Last heartbeat: %s" % vehicle2.last_heartbeat
print "V2 Is Armable?: %s" % vehicle2.is_armable
print "V2 Armed?: %s" % vehicle2.armed
print "V2 System status: %s" % vehicle2.system_status.state


while(vehicle.last_heartbeat < 29.0 and vehicle2.last_heartbeat < 29.0):
	count += 1
	print "---------------------------------------------------------------------------------------"
	print "V1 GPS: %s" % vehicle.gps_0
	print "V1 GPS location: %s" % vehicle.location.global_frame
	print "V1 Last heartbeat: %s" % vehicle.last_heartbeat
	print "V1 System status: %s" % vehicle.system_status.state
	print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	print "V2 GPS: %s" % vehicle2.gps_0
	print "V2 GPS location: %s" % vehicle2.location.global_frame
	print "V2 Last heartbeat: %s" % vehicle2.last_heartbeat
	print "V2 System status: %s" % vehicle2.system_status.state
	time.sleep(1.0)



# Close vehicle object before exiting script
vehicle.close()
vehicle2.close()

# Shut down simulator
#sitl.stop()
print("Completed")
