import subprocess
import shlex
import re
import time
import datetime


"""
Provides features for scanning for BLE beacon, identifying and printing relevant information.
Hopefully data will eventually be saved and processed but that's not here yet. 
"""


#Colors for coloring terminal output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


shellcmd = shlex.split("{   printf 'scan on\\n';     sleep 2;     printf5'devices\\n';     printf 'quit\\n'; } | bluetoothctl")
shellcmd = "{   printf 'scan on\\n';     sleep 1;     printf 'quit\\n'; } | bluetoothctl"


mac = "0C:19:F8:96:13:D2" #mac address of desired BLE decive
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])') #regex for removing color coding before interpreting process output

def BTscan_bluetoothctl():
    """Scan using bluetoothctl"""
    while True:
        try:
            scan = subprocess.run(shellcmd, shell=True, stdout=subprocess.PIPE, check=True, text=True)
            result = ansi_escape.sub('', scan.stdout) #remove color coding in output

            #Look for the interesting lines, not developed..
            for line in result.split("\n"):
                if "004c" in line:
                    #print(line)
                    pass
                elif mac in line:
                    print()
                    print(bcolors.OKGREEN+line+bcolors.ENDC)
                elif 'Perillyne' in line:
                    print()
                    print(bcolors.OKGREEN+line+bcolors.ENDC)
            print("-",end="", flush=True)
        

        except KeyboardInterrupt: #bluetoothctl runs interactively, this avoids unnessecary error message when killing the process
            exit()



def BTscan_btmgmt():
    """Scan using btmgmt"""
    proc = subprocess.Popen(['sudo','btmgmt','--timeout','60','find'], stdout=subprocess.PIPE, universal_newlines=True)
    #proc = subprocess.Popen(['sudo','btmgmt','--timeout','60','find'], universal_newlines=True)
    #proc = subprocess.Popen(['sudo','btmgmt','advmon','on','&&','sudo','btmgmt','--timeout','60','find'], universal_newlines=True)
    print('looking for:',mac)
    
    try:
        while proc.poll()!=0: #is process proc (the scane) still running?
            for line in proc.stdout: #continuous monitoring of scan output
                line=line.split()
                print(line)
                try:
                    if 'rssi' in line and int(line[line.index('rssi')+1]) > -75:
                        print(line[0:-1], datetime.datetime.now())
                except IndexError:
                    pass
                except ValueError:
                    pass
                
            time.sleep(.5)
    except KeyboardInterrupt:
        exit()
        
    
BTscan_btmgmt()



#the following seems to do the same as "bluetoothctl show":
#import pydbus
#bus = pydbus.SystemBus()
#obj_mngr = bus.get('org.bluez', '/')
#mngd_objs = obj_mngr.GetManagedObjects()
#for path, obj in mngd_objs.items():
#    for key, item in obj.items():
#        #print(key, item)
#        for keyy, itemm in item.items():
#            print(keyy, itemm)
