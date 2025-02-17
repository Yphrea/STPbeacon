import matplotlib.pyplot as plt
from math import sqrt
from scipy.interpolate import make_smoothing_spline
import numpy as np


"""plotting of test data for quality evaluation"""


def read_data_from_file(filename):
    """read data from file (collect with 'scan.py')"""

    
    RSSI=[]; time=[]
    start_time = None; true_time = None

    with open(filename,'r') as fil:
        for line in fil:
            try:
                line = line.split()
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
        time_consecutive = [sum(time[:i+1]) for i in range(len(time))]
        return (time_consecutive, RSSI, true_time)


def panelplot_test_data(list_of_data_files, show=False, save=None, bin_time=False, N=10):

    if type(list_of_data_files) != list:
        list_of_data_files = [list_of_data_files]

    # Panel layout
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
            axes[i].hist(time, density=True, stacked=True, bins=N)
        else: # plain plot RSSI(time) from start of data sampling
            axes[i].plot(time,RSSI,'*')
            ylim = axes[i].get_ylim()
            time_aux = np.arange(0, max(time), 0.05)
            spl = make_smoothing_spline(time, RSSI, lam=None)
            spl_RSSI = spl(time_aux)
            i_spl_max = spl_RSSI.argmax(axis=0)
            axes[i].plot(time_aux, spl_RSSI, '-.')
            axes[i].plot([time_aux[i_spl_max]]*2, ylim,'--k', label='evaluated')
            print('diff in s:', true_time - time_aux[i_spl_max])
            try:
                #axes[i].plot(true_time, max(RSSI),'*')
                axes[i].plot([true_time]*2, ylim,'-k', label='facit')
            except ValueError:
                pass # If true_time is None, i.e. not registered
    if save != None:
        plt.savefig(save, dpi=300)
    if show:
        plt.legend()
        plt.show()


#panelplot_test_data('test_data/noise/noise_Nano_32', show=True, save='noise_Nano_32.2.png')
#panelplot_test_data(['test_data/noise/noise_Nano_32', 'test_data/noise/noise_Nano_40'], N=30, bin_time=True, show=True)
#panelplot_test_data(['test_data/walking_it2/juniper_a',
#                     'test_data/walking_it2/juniper_b',
#                     'test_data/walking_it2/juniper_c',
#                     'test_data/walking_it2/juniper_d',
#                     'test_data/walking_it2/juniper_e',
#                     'test_data/walking_it2/juniper_f'], show=True)
panelplot_test_data(['test_data/walking_it2/Nano_a',#],show=True)
                     'test_data/walking_it2/Nano_b',
                     'test_data/walking_it2/Nano_c',
                     'test_data/walking_it2/Nano_d',
                     'test_data/walking_it2/Nano_e',
                     'test_data/walking_it2/Nano_f'], show=True)

