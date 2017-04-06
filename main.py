#!/usr/bin/python
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

print "Starting Node API server..."
subprocess.Popen(["node", "/home/pi/Projects/nodehooks/bin/www"])
print "Node API server started, output piped here."

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
                print "Killing Node process, PID: ", pid
                os.kill(int(pid), signal.SIGKILL)
            print "Performing Git Pull..."
            g = git.cmd.Git('/home/pi/Projects/nodehooks')
            g.pull()
            print "Git Pull complete, restarting Node API server..."
            subprocess.Popen(["node", "/home/pi/Projects/nodehooks/bin/www"])
            print "Node API server restarted, output piped here."

    conn.close()