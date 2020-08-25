"""
Programm - chat
Client

Oskolkov Nikita
"""
import socket
import os
import time
import signal


GET_MESS = "*"


class Client:
    def __init__(self, host, port, nikname):
        self._host = host
        self._port = port
        self._nikname = nikname

        try:
            self.conn = socket.create_connection((host, port))
        except Exception:
            pass

    def rename(self):
        new_nikname = input()
        self._nikname = new_nikname

    def get_nik(self):
        return self._nikname

    def close(self):
        try:
            self.conn.close()
        except Exception:
            pass

    def send_message(self, message):
        try:
           self.conn.sendall(message.encode())
        except KeyboardInterrupt:
            raise KeyboardInterrupt()

    def get_data(self):
        return self.conn.recv(1024)


def _main():
    print("Enter your nikname:")

    nikname = input()

    client = Client('127.0.0.1', 6666, nikname)
    client.send_message(client.get_nik())
    pid_get = os.fork()
    if pid_get != 0:
        pid_check = os.fork()
        if pid_check != 0:
            try:
                while True:
                    message = input()

                    client.send_message(message)
                    if (message != GET_MESS):
                        print("you send message: ", message)

                os.wait()
            except KeyboardInterrupt:
                print("catch interrupt")
                os.kill(pid_check, signal.SIGKILL)
                os.kill(pid_get, signal.SIGKILL)
            finally:
                client.close()
        else:
            while True:
                time.sleep(1)
                client.send_message(GET_MESS)
    else:
        while True:
            data = client.get_data()
            if not data:
                continue

            print(data.decode('utf-8'))


if __name__ == '__main__':
    _main()
