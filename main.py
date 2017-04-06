import socket
import os
import signal
import subprocess
import git

TCP_IP = '127.0.0.1'
TCP_PORT = 6006
BUFFER_SIZE = 60

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

while True:
    conn, addr = s.accept()
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            break
        print "Data Received: ", data
        if data == "git restart":
            proc = subprocess.Popen(["pgrep", "node"], stdout=subprocess.PIPE)
            for pid in proc.stdout:
                os.kill(int(pid), signal.SIGKILL)
            g = git.cmd.Git('C:\\Users\\ADunigan\\WebstormProjects\\nodehooks')
            g.pull()
            subprocess.Popen(["node", "/home/pi/Projects/nodehooks/bin/www"])

    conn.close()