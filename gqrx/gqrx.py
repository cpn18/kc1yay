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
        return self.client.recv(64).decode().strip()

    def status(self):
        """ Check for status """
        data = self.get_response()
        if data == "RPRT 0":
            return True
        if data == "RPRT 1":
            return False
        raise ValueError(data)

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

    def set_demod_mode(self, mode):
        """ Set Demodulator Mode """
        if mode not in self.demod_modes:
            raise ValueError("Unsupported Demod Mode")

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

    def set_squelch(self, dbfs):
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

    def set_record(self, status):
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

if __name__ == "__main__":
    mygqrx = GQRX()
    print(mygqrx.demod_modes)

    mygqrx.set_freq(443.850e6)
    mygqrx.set_demod_mode("FM")
