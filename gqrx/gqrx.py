"""
GQRX API

Partial implementation based on:

https://github.com/gqrx-sdr/gqrx/blob/master/resources/remote-control.txt
"""
import socket
import time
from datetime import datetime

class GQRX():
    """ Python Interface with GQRX """

    def __init__(self, host='localhost', port=7356):
        """ Initialize a connection """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

    def __del__(self):
        """ Close the connection """
        self.close()
        self.client.close()

    def get_response(self):
        """ Get Response """
        return self.client.recv(64).decode().strip()

    def status(self):
        """ Check for status """
        data = self.get_response()
        if data == "RPRT 0":
            return True
        if data == "RPRT 1":
            return False
        raise ValueError

    def get_freq(self):
        """ Get Frequency """
        self.client.send(b"f\n")
        data = self.get_response()
        return int(data)

    def set_freq(self,freq):
        """ Set Frequency """
        cmd = "F %d\n" % freq
        self.client.send(cmd.encode())
        return self.status()

    def get_gain(self):
        """ Get Audio Gain """
        self.client.send(b"l AF\n")
        data = self.get_response()
        return int(data)

    def set_gain(self,gain):
        """ Set Audio Gain """
        cmd = "L AF %f\n" % gain
        self.client.send(cmd.encode())
        return self.status()

    def get_demod_mode(self):
        """ Get Demodulator Mode """
        cmd = "m\n"
        self.client.send(cmd.encode())
        data = self.get_response()
        return str(data)

    def set_demod_mode(self,mode):
        """ Set Demodulator Mode """
        cmd = "M %s\n" % mode
        self.client.send(cmd.encode())
        return self.status()

    def get_signal_strength(self):
        """ Get Signal Strength """
        self.client.send(b"l STRENGTH\n")
        data = self.get_response()
        return float(data)

    def get_squelch(self):
        """ Get Squelch Threshold """
        cmd = "l SQL\n"
        self.client.send(cmd.encode())
        data = self.get_response()
        return float(data)

    def set_squelch(self,dbfs):
        """ Set Squelch Threshold """
        cmd = "L SQL %s\n" % dbfs
        self.client.send(cmd.encode())
        return self.status()

    def get_record(self):
        """ Get Recorder Status """
        cmd = "u RECORD\n"
        self.client.send(cmd.encode())
        data = self.get_response()
        return str(data)

    def set_record(self,status):
        """ Set Recorder Status """
        cmd = "U RECORD %s\n" % status
        self.client.send(cmd.encode())
        return self.status()

    def close(self):
        """ Close Connection """
        cmd = "c\n"
        self.client.send(cmd.encode())
        return self.status()

    def aos(self):
        """ Acquisition of Signal """
        cmd = "AOS\n"
        self.client.send(cmd.encode())
        return self.status()

    def los(self):
        """ Loss of Signal """
        cmd = "LOS\n"
        self.client.send(cmd.encode())
        return self.status()


def scan(low_hz, high_hz, step_hz=1e3, threshold_db=-40, pause_sec=1):
    """ Demo Code for Scanning """
    gqrx = GQRX()
    while True:
        try:
            freq = gqrx.get_freq()
            freq += step_hz
            if freq > high_hz or freq < low_hz:
                freq = low_hz
            gqrx.set_freq(freq)
            st_dbfs = gqrx.get_signal_strength()
            if st_dbfs > threshold_db:
                print(datetime.now().isoformat(), freq, st_dbfs)
                time.sleep(pause_sec)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    scan(420e6, 450e6)  # 70cm
    #scan(144e6, 148e6)  # 2m
    #scan(220e6, 225e6)  # 1.25m
