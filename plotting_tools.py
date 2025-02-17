import matplotlib.pyplot as plt
from math import sqrt


"""plotting of test data for quality evaluation"""


def read_data_from_file(filename):
    """read data from file (collect with 'scan.py')"""

    
    RSSI=[]; time=[]
    start_time = None; true_time = None

    with open(filename,'r') as fil:
        for line in fil:
            try:
                line= line.split()
                try:
                    int(line[1])
                    assert int(line[1]) < 0 #manually marked "true time" indicated by RSSI=0 in test data file
                    RSSI.append(int(line[1]))
                except ValueError:
                    start_time = [float(i) for i in line[-1].split(':')]
                    start_time = start_time[0]*3600+start_time[1]*60+start_time[2]
                    continue
                except AssertionError:
                    true_time = [float(i) for i in line[-1].split(':')]
                    true_time = true_time[0]*3600+true_time[1]*60+true_time[2]
                    continue
                aux_time = line[-1].split(':')
                time.append(float(aux_time[-2])+float(aux_time[-1]))
            except IndexError:
                break

        try:
            true_time = true_time - start_time
            print(true_time)
        except TypeError:
            pass
        time_con = [sum(time[:i]) for i in range(len(time))]
        return (time_con, RSSI, true_time)


def panelplot_test_data(list_of_data_files, show=False, save=None, bin_time=False, N=10):

    if type(list_of_data_files) != list:
        list_of_data_files = [list_of_data_files]
        
    m = len(list_of_data_files)
    sq_m = sqrt(m)
    width = int(sq_m); height = int(sq_m)

    if m > int(sq_m)**2:
        width += 1
    if m > int(sq_m)*(int(sq_m)+1):
        height += 1
        
    fig, axes = plt.subplots(height, width, sharey=True)
    try:
        axes = axes.flatten()
    except AttributeError:
        axes = [axes]
    
    for i, data_file in enumerate(list_of_data_files):
        time, RSSI, true_time = read_data_from_file(data_file)
        if bin_time: # histogram over time between advertisements in sample data
            time = [0]+[time[i+1]-time[i] for i in range(len(time)-1)] # time difference between data points
            print(axes)
            axes[i].hist(time, density=True, stacked=True, bins=N)
        else: # plain plot RSSI(time) from start of data sampling
            axes[i].plot(time,RSSI,'*')
            try:
                axes[i].plot(true_time, max(RSSI),'*')
            except ValueError:
                pass # If true_time is None, i.e. not registered
    if save != None:
        plt.savefig(save, dpi=300)
    if show:
        plt.show()


#panelplot_test_data(['test_data/noise/noise_leyrien',
#                     'test_data/noise/noise_leyrien_ch1',
#                     'test_data/noise/noise_leyrien_ch2',
#                     'test_data/noise/noise_leyrien_ch3'], show=True, bin_time=True)
#panelplot_test_data('test_data/noise/noise_Nano_32', show=True, save='noise_Nano_32.2.png')
#panelplot_test_data(['test_data/noise/noise_Nano_32', 'test_data/noise/noise_Nano_40'], N=30, bin_time=True, show=True)
panelplot_test_data(['test_data/walking_it2/juniper_a',
                     'test_data/walking_it2/juniper_b',
                     'test_data/walking_it2/juniper_c',
                     'test_data/walking_it2/juniper_d',
                     'test_data/walking_it2/juniper_e',
                     'test_data/walking_it2/juniper_f'], show=True)

