import sys
import numpy as np

time_to_depart, bus_list = list(sys.stdin)[:2]
time_to_depart = int(time_to_depart)
bus_durations = [int(x) for x in bus_list.split(",") if x != "x"]
bus_starts = [(x - (time_to_depart % x)) % x + time_to_depart for x in bus_durations]

i = np.argmin(bus_starts)
print((bus_starts[i] - time_to_depart) * bus_durations[i])
