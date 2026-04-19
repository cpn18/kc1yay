#!/usr/bin/env python3
"""
Based on https://github.com/brannondorsey/chirp-files/blob/master/empty-chirp-file.csv
"""
import sys
import csv
import json


def json_to_chirp_csv(stations, filename):
    """ Write out a chirp compatible CSV file """
    with open(filename, 'w', newline='') as outfile:
        fieldnames = [
            "Location",
            "Name",
            "Frequency",
            "Duplex",
            "Offset",
            "Tone",
            "rToneFreq",
            "cToneFreq",
            "DtcsCode",
            "DtcsPolarity",
            "Mode",
            "TStep",
            "Skip",
            "Comment",
            "URCALL",
            "RPT1CALL",
            "RPT2CALL",
            "DVCODE",
        ]
        writer=csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        data = []
        location = 0
        for station in stations['stations']:
            data.append({
                "Location": location,
                "Name": station["callsign"],
                "Frequency": station["freq_mHz"],
                "Duplex": "",
                "Offset": float(station["offset"]+"0.5"),
                "Tone": station["access"].get("tone", ""),
                "rToneFreq": "",
                "cToneFreq": "",
                "DtcsCode": "",
                "DtcsPolarity": "",
                "Mode": station["modes"][0],
                "TStep": "",
                "Skip": "",
                "Comment": f"{station['location']}, {station['state']}",
                "URCALL": "",
                "RPT1CALL": "",
                "RPT2CALL": "",
                "DVCODE": "",
            })
            location += 1
        writer.writerows(data)


def main(filename):
    """ Main Application """
    with open(filename) as infile:
        stations = json.loads(infile.read())

    json_to_chirp_csv(stations, filename.replace('.json', '.csv'))

if __name__ == "__main__":
    main(sys.argv[1])
