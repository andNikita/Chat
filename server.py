"""
Programm - chat
Server

Oskolkov Nikita
"""
import asyncio


GET_MESS = "*"


class Database:
    def __init__(self, mode):
        self._f = open('database.txt', mode)

    def read(self):
        return self._f.read()

    def write(self, data):
        data = data + "\n"
        self._f.write(data)

    def close(self):
        self._f.close()


class Server:
    def __init__(self, host, port, loop=None):
        self._loop = loop or asyncio.get_event_loop()
        self._server = asyncio.start_server(self.handle_connection, host=host, port=port)

    def start(self):
        self._server = self._loop.run_until_complete(self._server)
        self._loop.run_forever()

    def stop(self):
        self._server.close()
        self._loop.close()

    async def handle_connetcion(self, reader, writer):
        pass


class Client:
    def __init__(self, nikname):
        self._nikname = nikname
        self._local_database = {}

    def rename(self, new_nikname):
        self._nikname = new_nikname

    def get_nik(self):
        return self._nikname


class Chat_Server(Server):
    def __init__(self, host, port, loop=None):
        Server.__init__(self, host, port, loop)
        self._local_database = {}

    def add_in_data(self, nikname):
        self._local_database[nikname] = []

    def put_ld(self, nikname, data):
        self._local_database[nikname].append(data)

    def is_mess_ld(self, nikname):
        if len(self._local_database[nikname]) > 0:
            return True
        else:
            return False

    def get_mess_ld(self, nikname):
        data = ""
        while len(self._local_database[nikname]) > 0:
            data += self._local_database[nikname].pop(0)

        return data

    def send_all(self, nikname, data):
        for key in self._local_database:
            if key != nikname:
                self.put_ld(key, data)

    def print_database(self):
        print(self._local_database)

    async def handle_connection(self, reader, writer):
        nikname = await reader.read(1024)

        database_start = Database('a+')
        client = Client(nikname.decode('utf-8'))
        self.add_in_data(client.get_nik())
        database_start.write(client.get_nik() + " connected")
        database_start.close()

        #try:
        while True:
            database = Database('a')

            recv_data = await reader.read(1024)

            if recv_data is not None and recv_data != "":
                if recv_data.decode('utf-8') == GET_MESS:
                    if self.is_mess_ld(client.get_nik()):
                        writer.write(self.get_mess_ld(client.get_nik()).encode('utf-8'))
                        await writer.drain()
                else:
                    gotten_str = client.get_nik() + ":" + recv_data.decode('utf-8')
                    database.write(gotten_str)
                    self.send_all(client.get_nik(), gotten_str)

            database.close()

        writer.close()


def _main():
    server = Chat_Server('127.0.0.1', 6666)
    try:
        server.start()
    except KeyboardInterrupt:
        print("server stopped")
    finally:
        server.stop()


if __name__ == '__main__':
    _main()
