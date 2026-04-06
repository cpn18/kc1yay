import sys
import json

def mode_to_modulation(mode):
    if mode == "FM":
        return "Narrow FM"
    return mode

def write_bookmarks(filename, tags, stations):
    with open(filename, "w") as outfile:
        outfile.write("# Tag name          ;  color\n")
        for tag in tags:
            outfile.write("%-20s; %s\n" % (tag['name'], tag['color']))
        outfile.write("\n")
        outfile.write("# Frequency ; Name                     ; Modulation          ;  Bandwidth; Tags\n")
        outfile.write("   224440000; K1KZP                    ; Narrow FM           ;      10000; 220MHz\n")
        for station in stations['stations']:
            outfile.write("%12s; %-25s; %-20s; %10s; %s\n" % (
                int(station['freq_mHz'] * 1e6),
                station['callsign'],
                mode_to_modulation(station['modes'][0]),
                station.get('bw', 10000),
                station.get('tag', '')
            ))

def main(inputfile):
    tags = []
    with open(inputfile) as infile:
        stations = json.loads(infile.read())
    write_bookmarks(inputfile + ".csv", tags, stations)

if __name__ == "__main__":
    main(sys.argv[1])
