"""
GQRX API

Partial implementation based on:

https://github.com/gqrx-sdr/gqrx/blob/master/resources/remote-control.txt
"""
import socket

class GQRX():
    """ Python Interface with GQRX """

    def __init__(self, host='localhost', port=7356):
        """ Initialize a connection """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((host, port))
        except ConnectionRefusedError as ex:
            print("Check RemoteControl Settings")
            raise ex
        # Get Demod Modes
        cmd = "M ?\n"
        self.client.send(cmd.encode())
        self.demod_modes = self.get_response().split(" ")

    def __del__(self):
        """ Close the connection """
        self.client.close()

    def get_response(self):
        """ Get Response """
        data = self.client.recv(64).decode().strip()
        if len(data) == 0:
            raise ConnectionAbortedError
        return data

    def status(self):
        """ Check for status """
        try:
            data = self.get_response()
            if data == "RPRT 0":
                return True
            if data == "RPRT 1":
                return False
        except Exception as ex:
            raise ex
        raise ValueError(data)

    def get_freq(self):
        """ Get Frequency """
        try:
            self.client.send(b"f\n")
            data = self.get_response()
            return int(data)
        except Exception as ex:
            raise ex

    def set_freq(self,freq):
        """ Set Frequency """
        try:
            cmd = "F %d\n" % freq
            self.client.send(cmd.encode())
            return self.status()
        except Exception as ex:
            raise ex

    def get_gain(self):
        """ Get Audio Gain """
        try:
            self.client.send(b"l AF\n")
            data = self.get_response()
            return int(data)
        except Exception as ex:
            raise ex

    def set_gain(self,gain):
        """ Set Audio Gain """
        try:
            cmd = "L AF %f\n" % gain
            self.client.send(cmd.encode())
            return self.status()
        except Exception as ex:
            raise ex

    def get_demod_mode(self):
        """ Get Demodulator Mode """
        try:
            cmd = "m\n"
            self.client.send(cmd.encode())
            data = self.get_response()
            return str(data)
        except Exception as ex:
            raise ex

    def set_demod_mode(self, mode):
        """ Set Demodulator Mode """
        if mode not in self.demod_modes:
            raise ValueError("Unsupported Demod Mode")

        try:
            cmd = "M %s\n" % mode
            self.client.send(cmd.encode())
            return self.status()
        except Exception as ex:
            raise ex

    def get_signal_strength(self):
        """ Get Signal Strength """
        try:
            self.client.send(b"l STRENGTH\n")
            data = self.get_response()
            return float(data)
        except Exception as ex:
            raise ex

    def get_squelch(self):
        """ Get Squelch Threshold """
        try:
            cmd = "l SQL\n"
            self.client.send(cmd.encode())
            data = self.get_response()
            return float(data)
        except Exception as ex:
            raise ex

    def set_squelch(self, dbfs):
        """ Set Squelch Threshold """
        try:
            cmd = "L SQL %s\n" % dbfs
            self.client.send(cmd.encode())
            return self.status()
        except Exception as ex:
            raise ex

    def get_record(self):
        """ Get Recorder Status """
        try:
            cmd = "u RECORD\n"
            self.client.send(cmd.encode())
            data = self.get_response()
            return str(data)
        except Exception as ex:
            raise ex

    def set_record(self, status):
        """ Set Recorder Status """
        try:
            cmd = "U RECORD %s\n" % status
            self.client.send(cmd.encode())
            return self.status()
        except Exception as ex:
            raise ex

    def close(self):
        """ Close Connection """
        try:
            cmd = "c\n"
            self.client.send(cmd.encode())
            return self.status()
        except Exception as ex:
            raise ex

    def aos(self):
        """ Acquisition of Signal """
        try:
            cmd = "AOS\n"
            self.client.send(cmd.encode())
            return self.status()
        except Exception as ex:
            raise ex

    def los(self):
        """ Loss of Signal """
        try:
            cmd = "LOS\n"
            self.client.send(cmd.encode())
            return self.status()
        except Exception as ex:
            raise ex

if __name__ == "__main__":
    mygqrx = GQRX()
    print(mygqrx.demod_modes)

    mygqrx.set_freq(443.850e6)
    mygqrx.set_demod_mode("FM")
