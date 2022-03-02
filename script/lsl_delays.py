from matplotlib import pyplot as plt
from pylsl import local_clock

from cardio_audio_sleep import Detector
from cardio_audio_sleep.utils import search_ANT_amplifier


#%% LSL Streams
stream_name = search_ANT_amplifier()
ecg_ch_name = 'AUX7'

#%% Peak detection
peak_height_perc = 98
peak_prominence = 1000

#%% Loop
detector = Detector(
    stream_name, ecg_ch_name, duration_buffer=3,
    peak_height_perc=peak_height_perc, peak_prominence=peak_prominence)
detector.prefill_buffer()

counter = 0
delays = list()
while counter <= 100:
    detector.update_loop()
    pos = detector.new_peaks()
    if pos is not None:
        # compute where we are relative to the r-peak
        delay = local_clock() - detector.timestamps_buffer[pos]
        delays.append(delay)
        counter += 1

#%% Plot
f, ax = plt.subplots(1, 1)
ax.set_title('LSL delays')
ax.hist(delays)
