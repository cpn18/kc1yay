#!/usr/bin/env python3
"""
Scanner using GQRX API
"""
import sys
import json
import time
from datetime import datetime

import gqrx

def scan_list(filename, step_hz=1e3, threshold_db=-40, dwell_sec=0.1, pause_sec=1, demod='FM'):
    """ Demo Code for Scanning """
    mysdr = gqrx.GQRX()

    # Set up the radio
    mysdr.set_demod_mode(demod)
    mysdr.set_squelch(threshold_db)


    # Read the station list
    with open(filename) as infile:
        stations = json.loads(infile.read())

    while True:
        try:
            for station in stations['data']:
                if demod not in station['modes']:
                    continue

                # Update from radio
                squelch = mysdr.get_squelch()
                if threshold_db != squelch:
                    threshold_db = squelch
                    print(f"Squelch = {squelch:0.1f}")

                # Tune the radio
                freq = station['freq_mHz']*1e6
                mysdr.set_freq(freq)
                time.sleep(dwell_sec)

                # Check signal strength
                st_dbfs = mysdr.get_signal_strength()
                if st_dbfs > threshold_db:
                    print("%s %0.6f %0.1f dB %s %s" % (datetime.now().isoformat(), freq/1e6, st_dbfs, station['location'], station['callsign']))
                    time.sleep(pause_sec)

        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    scan_list(sys.argv[1], threshold_db=-40.0, dwell_sec=0.5, pause_sec=10)
