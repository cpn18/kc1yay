"""
GQRX API

Partial implementation based on:

https://github.com/gqrx-sdr/gqrx/blob/master/resources/remote-control.txt
"""
import sys
import time
from datetime import datetime

import gqrx

def scan(low_hz, high_hz, step_hz=1e3, threshold_db=-40, dwell_sec=0.1, pause_sec=1, demod='FM'):
    """ Demo Code for Scanning """
    mysdr = gqrx.GQRX()
    mysdr.set_demod_mode(demod)
    while True:
        try:
            freq = mysdr.get_freq()
            freq += step_hz
            if freq > high_hz or freq < low_hz:
                freq = low_hz
            mysdr.set_freq(freq)
            time.sleep(dwell_sec)
            st_dbfs = mysdr.get_signal_strength()
            if st_dbfs > threshold_db:
                print(datetime.now().isoformat(), freq, st_dbfs)
                time.sleep(pause_sec)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    if sys.argv[1] == "70cm":
        scan(420e6, 450e6)  # 70cm
    elif sys.argv[1] == "2m":
        scan(144e6, 148e6)  # 2m
    elif sys.argv[1] == "1.25m":
        scan(220e6, 225e6)  # 1.25m
    elif sys.argv[1] == "fm":
        scan(88.1e6, 107.9e6, step_hz=0.2e6, pause_sec=5, demod='WFM_ST')  # FM radio
    elif sys.argv[1] == "air":
        scan(108e6, 137e6)  # Air
    else:
        scan(int(sys.argv[1]), int(sys.argv[2]))
