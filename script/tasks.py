import numpy as np
from byte_trigger import ParallelPortTrigger

from cardio_audio_sleep.config.constants import TRIGGERS
from cardio_audio_sleep.tasks import asynchronous, baseline, isochronous, synchronous
from cardio_audio_sleep.utils import generate_sequence, search_ANT_amplifier

# %% Triggers
trigger = ParallelPortTrigger("/dev/parport0")


# %% LSL Streams
stream_name = search_ANT_amplifier()
ecg_ch_name = "AUX7"


# %% Synchronous

# Peak detection settings
peak_height_perc = 97.5  # %
peak_prominence = 500
peak_width = None  # ms | None
# Sequence
sequence = generate_sequence(100, 0, 10, TRIGGERS)
# Task
sequence_timings = synchronous(
    trigger,
    TRIGGERS,
    sequence,
    stream_name,
    ecg_ch_name,
    peak_height_perc,
    peak_prominence,
    peak_width,
)


# %% Isochronous

# Compute inter-stimulus delay
delay = np.median(np.diff(sequence_timings))
# Sequence
sequence = generate_sequence(100, 0, 10, TRIGGERS)
# Task
isochronous(trigger, TRIGGERS, sequence, delay)


# %% Asynchronous

# Sequence
sequence = generate_sequence(100, 0, 10, TRIGGERS)
# Task
asynchronous(trigger, TRIGGERS, sequence, sequence_timings)


# %% Baseline

# Compute duration
duration = 5 * 60  # seconds
# Task
baseline(trigger, TRIGGERS, duration)
