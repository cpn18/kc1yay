#!/usr/bin/env python3
"""
Scanner using GQRX API
"""
import os
import sys
import json
import time
from datetime import datetime

import gqrx

def scan_list(filename, step_hz=1e3, threshold_db=-40, dwell_sec=0.1, pause_sec=1, demod='FM'):
    """ Demo Code for Scanning """
    try:
        mysdr = gqrx.GQRX()
    except ConnectionRefusedError:
        print("Is GQRX running?")
        sys.exit(1)

    # Set up the radio
    mysdr.set_demod_mode(demod)
    mysdr.set_squelch(threshold_db)

    last_load = 0

    while True:
        mtime = os.stat(filename).st_mtime
        if mtime > last_load:
            print("Reading file")
            # Read the station list
            with open(filename) as infile:
                stations = json.loads(infile.read())
            last_load = mtime

        try:
            for station in stations['stations']:
                if demod not in station['modes']:
                    continue

                if station.get('scan', True) is False:
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

        except (KeyboardInterrupt, ConnectionAbortedError):
            break

if __name__ == "__main__":
    scan_list(sys.argv[1], threshold_db=-40.0, dwell_sec=0.5, pause_sec=10)
