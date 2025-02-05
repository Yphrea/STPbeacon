import datetime
import pexpect
import sys
import matplotlib.pyplot as plt
import math

#this is the mac address of the beacon
#look_for_mac = "1C:1B:B5:77:54:10" #Patchouli
#look_for_mac = "A0:A4:C5:EC:2A:AB" #Leyrien
#look_for_mac = "E4:A7:A0:A6:56:7A" #Juniper
look_for_mac = "5C:F3:70:9C:02:DF" #dongle

def scan_for_beacon(look_for_mac):
    proc = pexpect.spawn('bluetoothctl', encoding='utf-8')
    proc.expect(['bluetooth'])
    proc.sendline('menu scan')
    proc.sendline('duplicate-data on')
    proc.sendline('back')
    proc.sendline('scan on')

    last_detection = None
    while True:
        try:
            proc.expect('RSSI:', timeout=None) #look for advertisement signal strength
            try:
                mac = proc.before.split()[-1] #get mac address
                if not mac == look_for_mac:
                    continue
            except IndexError:
                continue
            proc.expect('\\n')
            rest_of_line = proc.before.split()
            #different versions of bluetoothctl uses a different formatting...
            if len(rest_of_line) == 1:
                RSSI = int(rest_of_line[0])
            elif len(rest_of_line) == 2:
                RSSI = rest_of_line[1].replace('(','')
                RSSI = RSSI.replace(')','')
                RSSI = int(RSSI)

            #time from last advertisement
            now = datetime.datetime.now()
            try:
                diff = now-last_detection
                print(mac, RSSI, diff)
            except TypeError:
                pass
            last_detection = now
                        
            sys.stdout.flush()
        except KeyboardInterrupt: #bluetoothctl runs interactively, this avoids unnessecary error message when killing the process
            print()
            break

def read_data_from_file(filename):
    RSSI=[]; time=[]

    with open(filename,'r') as fil:
        for line in fil:
            try:
                line= line.split()
                RSSI.append(int(line[1]))
                aux_time = line[-1].split(':')
                time.append(float(aux_time[-2])+float(aux_time[-1]))
            except IndexError:
                time_con = [sum(time[:i]) for i in range(len(time))]
                return (time_con, RSSI)


def plot_measurement(time, RSSI):
    plt.plot(time, RSSI,'*')
    plt.show()

def plot_panelplot(list_of_data_files):
    fig, axes = plt.subplots(2,2)
    axes = axes.flatten()
    print(axes)
    
    for i, data_file in enumerate(list_of_data_files):
        time, RSSI = read_data_from_file(data_file)
        axes[i].plot(time,RSSI,'*')
    plt.show()
            
time, RSSI = read_data_from_file('noise_dongle_2')
plot_measurement(time, RSSI)
#plot_panelplot(['output_a', 'output_b', 'output_c', 'output_d'])
#plot_panelplot(['dongle_a', 'dongle_b', 'dongle_c', 'dongle_d'])
#scan_for_beacon(look_for_mac)
