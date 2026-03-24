#!/usr/bin/env python
"""
Program to convert a RepeaterBook cut-n-paste tab-separated
text file into a JSON format

https://www.repeaterbook.com/repeaters/msResult.php?state_id%5B%5D=33&band%5B%5D=4&band%5B%5D=8&band%5B%5D=16&freq=&mode%5B%5D=1&status_id=%25&order=%60freq%60%2C+%60state_abbrev%60+ASC
"""
import sys
import json
import os
from datetime import datetime

# Example input
# ['', '449.8250 -', '82.5', 'NH', 'Whitefield', 'Coos', 'N1PCE', 'OPEN', 'FMAllStar', '🟢\n']


def split_freq(freq):
    """ Split into frequency and offset """
    freq = freq.split(' ')
    try:
        return float(freq[0]), freq[1]
    except:
        return freq[0], None

def decode_access(access_string):
    """ Convert tone to float """
    access = {}
    idx = 0
    symbols = access_string.split(' ')
    while idx < len(symbols):
        if symbols[idx] in ["CC", "NAC", "RAN"]:
            access[symbols[idx]] = symbols[idx+1]
            idx += 1
        elif symbols[idx] == "—":
            pass
        else:
            try:
                access["tone"] = float(symbols[idx])
            except:
                print(f"WARNING: {symbols[idx]}")
        idx += 1
    return access

def extract_modes(mode_string):
    """ Extract commom modes """
    modes = []
    features = []
    for mode in ["FM", "DMR", "D-Star", "M17", "NXDN", "P-25", "Fusion", "TETRA"]:
        if mode in mode_string:
            modes.append(mode)
    for feature in ["EchoLink", "AllStar", "IRLP", "WIRES-X", "ATV"]:
        if feature in mode_string:
            features.append(feature)
    return modes, features

def decode_status(status_string):
    """ Decode Unicode """
    if status_string == "🟢":
        return "Up"
    if status_string == "🔴":
        return "Down"
    if status_string == "⚪":
        return "Unknown"
    return status_string

def main(filename):
    repeaters = {
        "source": filename,
        "date": datetime.now().isoformat(),
        "data": []
    }
    with open(filename,'r') as infile:
        for line in infile:
            line = line.split('\t')
            #print(line)
            freq, offset = split_freq(line[1])
            modes, features = extract_modes(line[8])
            obj = {
                "freq_mHz": freq,
                "offset": offset,
                "access": decode_access(line[2]),
                "state": line[3],
                "location": line[4],
                "county": line[5],
                "callsign": line[6],
                "use": line[7],
                "modes": modes,
                "features": features,
                "status": decode_status(line[9].strip())
            }
            #print(obj)
            repeaters['data'].append(obj)

    outfile, _ext = os.path.splitext(filename)
    outfile += ".json"
    with open(outfile,"w") as outfile:
        outfile.write(json.dumps(repeaters, indent=2))

if __name__ == "__main__":
    main(sys.argv[1])
