For this calibration, we assume that you are using the same types of components and in the same configuration, and that your robot is built the same. We also assume you are running on Linux Ubuntu or Mint (Though other distros will work, they will have slightly different package installation) and that you are capable of entering commands into a terminal for these systems. Commands for the terminal are shown in brackets; the brackets should be removed when entering the command. To configure it before running:
Download and install APM Planner for Linux as seen here http://ardupilot.org/planner2/docs/installation-for-linux.html
Connect device to Pixhawk over USB to mini USB cable
Change APM Planner to advanced mode by changing the option in File (top left)
Connect the robot and run through the Wizard under Config/Tuning (upload firmware, calibrate compass, and calibrate accelerometer)
Go to Full Parameters List under Config/Tuning and change:
SKID_STEER_OUT from 0 to 1
PRE_ARMING_CHECK from any # to 2048
If you have not already done so, install python 2.X [apt-get install python2.X] where 2.X is the latest version of python 
If you have not already done so, install pip and python-dev [sudo apt-get install python-pip python-dev]
Install DroneKit [pip install dronekit]
Install Tornado [pip install tornado]
We will assume you already have Firefox installed. If not: [apt-get install firefox]
If you have not already done so, disconnect the robot from the wired connection, and instead power it on with battery power. Make sure all components are connected properly and the ground station device has all radios connected as well. 
Once all of the above are done, use git to clone the source code for this project: [git clone https://github.com/williamdewitt95/MercerSwarmRobots.git]
Navigate to the test2 folder, and open the background script with: [python livemap.py]
Inside the test2 folder, navigate to the static folder and open the map.html file with Firefox
Wait for the back end script to say Opened Socket XXXX. The system is now calibrated and ready to run.


For questions, email williamdewitt95@gmail.com
