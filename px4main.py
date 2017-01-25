
#print "Start simulator (SITL)"
#import dronekit_sitl
#sitl = dronekit_sitl.start_default()
#connection_string = sitl.connection_string()
#connection_string = "/dev/serial/by-id/usb-3D_Robotics_PX4_FMU_v2.x_0-if00"
connection_string = "/dev/ttyUSB0,57600"
#connection_string = "/dev/ttyACM0,57600"
# Import DroneKit-Python
#from dronekit import connect, VehicleMode, CommandSequence, Command, mavutil, locations
from dronekit import *
import time,math


# Connect to the Vehicle.
print("Connecting to vehicle on: %s" % (connection_string,))
#vehicle = connect(connection_string, wait_ready=True)
#vehicle = connect(connection_string, wait_ready=True, baud=57600)
vehicle = connect(connection_string)
#vehicle.battery = 4

# Get some vehicle attributes (state)
print "Get some vehicle attribute values:"
print " GPS: %s" % vehicle.gps_0
print " Battery: %s" % vehicle.battery
print " Last Heartbeat: %s" % vehicle.last_heartbeat
print " Armed?: %s" % vehicle.armed
print " Is Armable?: %s" % vehicle.is_armable
print " System status: %s" % vehicle.system_status.state
print " Mode: %s" % vehicle.mode.name    # settable
#vehicle.mode = VehicleMode("MANUAL")

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


while vehicle.gps_0.fix_type < 3:
	print " GPS %s" % vehicle.gps_0
	time.sleep(1)

print " GPS %s" % vehicle.gps_0
print " GPS location: %s" % vehicle.location.global_frame

home = vehicle.home_location
print " Home: %s" % home
home = vehicle.location.global_frame
home.alt = 30
vehicle.home_location = home
print " Home: %s" % home

print "Trying to move this thing"
vehicle.armed = True
time.sleep(3)
vehicle.mode = VehicleMode("GUIDED")
time.sleep(5)
print " Mode: %s" % vehicle.mode.name

vehicle.simple_takeoff(vehicle.location.global_frame.alt + 15)
print " Taking off"
time.sleep(5)
print " GPS location: %s" % vehicle.location.global_frame
time.sleep(5)
print " GPS location: %s" % vehicle.location.global_frame
time.sleep(5)
print " GPS location: %s" % vehicle.location.global_frame

print " System status: %s" % vehicle.system_status.state
vehicle.system_status.state = "ACTIVE"
print " System status: %s" % vehicle.system_status.state


# Set the LocationGlobal to head towards
a_location = LocationGlobal(-35.364114, 149.166022, 30)
print " location created: %s " % a_location
vehicle.simple_goto(a_location)
print "going"
time.sleep(5)

#home = vehicle.location.global_frame
#wp = get_location_offset_meters(home, 0, 0, 10);
#cmd = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)



#print " count: %s" % currcmds.count
#loc = LocationGlobalRelative(34.364114,-84.166022,30.0)
#print " Made location %s" % loc
currcmds = vehicle.commands
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
print " current num of commands: %s" % currcmds.count
count = 0
while(vehicle.last_heartbeat < 29.0 and count < 2000):
	count += 1
	print " GPS: %s" % vehicle.gps_0
	print " GPS location: %s" % vehicle.location.global_frame
	print " Last heartbeat: %s" % vehicle.last_heartbeat
	print " Is Armable?: %s" % vehicle.is_armable
	print " Armed?: %s" % vehicle.armed
	print " System status: %s" % vehicle.system_status.state
	time.sleep(1.0)



# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator
#sitl.stop()
print("Completed")
