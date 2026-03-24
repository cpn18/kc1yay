#!/usr/bin/env python3
"""
GQRX API

Partial implementation based on:

https://github.com/gqrx-sdr/gqrx/blob/master/resources/remote-control.txt
"""
import sys
import json
import time
from datetime import datetime

import gqrx

def scan_list(filename, step_hz=1e3, threshold_db=-40, dwell_sec=0.1, pause_sec=1, demod='FM'):
    """ Demo Code for Scanning """
    mysdr = gqrx.GQRX()
    mysdr.set_demod_mode(demod)

    with open(filename) as infile:
        stations = json.loads(infile.read())

    while True:
        try:
            for station in stations['data']:
                if demod not in station['modes']:
                    continue

                freq = station['freq_mHz']*1e6
                mysdr.set_freq(freq)
                time.sleep(dwell_sec)
                st_dbfs = mysdr.get_signal_strength()
                if st_dbfs > threshold_db:
                    print(datetime.now().isoformat(), freq, st_dbfs, station['location'], station['callsign'])
                    time.sleep(pause_sec)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    scan_list(sys.argv[1], dwell_sec=0.5, pause_sec=10)
