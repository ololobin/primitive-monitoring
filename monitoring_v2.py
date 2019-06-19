import matplotlib.pyplot as plt
import matplotlib.animation as animation
import paramiko, os, time, threading, getpass, traceback
from collections import deque
from playsound import playsound

SERVER1='server1' #paste your server#1
SERVER2='server2' #paste your server#2
source='/path_to_logs/logs/errors.txt' #paste the way to logs
sound=os.path.join(os.path.abspath(os.curdir),'alarm.mp3')
localpath1=os.path.join(os.path.abspath(os.curdir),'error1.txt')
localpath2=os.path.join(os.path.abspath(os.curdir),'error2.txt')
port = 22
cmd1='ps ax |grep "counterrors_TS.sh" | awk \'{print  $5;}\'|grep "bash"'
cmd2='/path_to_logs/logs/counterrors_TS.sh &' #paste the way to logs
labelname=['Label1', 'Label2'] #paste your labels
timer=6

# make EXE for employee
# pip install pypiwin32
# pip install pyinstaller
#
# pyinstaller --onefile --icon=1.ico monitoring_PRODv2.py

user=input('Enter login: ')
passs=getpass.getpass(prompt='Enter password: ') #tiny security
maxerrors=int(input('Enter maximum of errors: '))

plt.style.use('dark_background')
gridsize = (3, 2)
fig = plt.figure(figsize=(12, 8))
ax = plt.subplot2grid(gridsize, (0, 0), colspan=2, rowspan=2)
ax1 = plt.subplot2grid(gridsize, (2, 0))
ax2 = plt.subplot2grid(gridsize, (2, 1))

def alarm():
    while True:
        err1 = open(localpath1, "r+")
        last_line = err1.readlines()[-1]
        if int(last_line)>maxerrors:
            try:
                playsound(sound)
            except:
                traceback.print_exc()
        err1.close()
        err2 = open(localpath2, "r+")
        last_line = err2.readlines()[-1]
        if int(last_line)>maxerrors:
            try:
                playsound(sound)
            except:
                traceback.print_exc()
        time.sleep(timer)

def animate(i): #this one w\o scale to clearly see the peak of failure
    with open(localpath1) as f:
        x1s = []
        y1s = []
        x1=0
        for row in deque(f, 50): #I am cool with 50 value in 0x line 
            x1 = x1+1
            y1 = row
            x1s.append(x1)
            y1s.append(float(y1))
    ax.clear()
    ax.plot(x1s, y1s,'r')
    ax.set_ylim((0, maxerrors), auto=False) #this maxerrors value means max critical for paying attention
    with open(localpath2) as f:        
        x2s = []
        y2s = []
        x2=0
        for row in deque(f, 50):
            x2 = x2+1
            y2 = row
            x2s.append(x2)
            y2s.append(float(y2))
    ax.plot(x2s, y2s,'b')
    ax.set_ylim((0, maxerrors), auto=False)
    ax.legend(labelname, loc='upper right', frameon=False)
def animate_scale(i): #this one with scale to see dynamic of errors
    with open(localpath1) as f:
        x1s = []
        y1s = []
        x1=0
        for row in deque(f, 50):
            x1 = x1+1
            y1 = row
            x1s.append(x1)
            y1s.append(float(y1))
    ax1.clear()
    ax1.plot(x1s, y1s,'r')
    with open(localpath2) as f:
        x2s = []
        y2s = []
        x2=0
        for row in deque(f, 50):
            x2 = x2+1
            y2 = row
            x2s.append(x2)
            y2s.append(float(y2))
    ax1.plot(x2s, y2s,'b')


def animate_scale2(i): #this one with scale to see dynamic of errors
    with open(localpath1) as f:
        x1s = []
        y1s = []
        x1=0
        for row in deque(f, 1000):
            x1 = x1+1
            y1 = row
            x1s.append(x1)
            y1s.append(float(y1))
    ax2.clear()
    ax2.plot(x1s, y1s,'r')
    with open(localpath2) as f:
        x2s = []
        y2s = []
        x2=0
        for row in deque(f, 1000):
            x2 = x2+1
            y2 = row
            x2s.append(x2)
            y2s.append(float(y2))
    ax2.plot(x2s, y2s,'b')

def run_sh1():
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER1,port,username=user,password=passs)
    stdin,stdout,stderr=ssh.exec_command(cmd1)
    outlines=stdout.readlines()
    if len(outlines)<3: #check to have only 1 running version of counterrors_TS.sh
        stdin,stdout,stderr=ssh.exec_command(cmd2)

def run_sh2():
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER2,port,username=user,password=passs)
    stdin,stdout,stderr=ssh.exec_command(cmd1)
    outlines=stdout.readlines()
    if len(outlines)<3:
        stdin,stdout,stderr=ssh.exec_command(cmd2)

def show_ts1():
    transport = paramiko.Transport((SERVER1, port))
    transport.connect(username=user, password=passs)
    sftp = paramiko.SFTPClient.from_transport(transport)
    while True:
        sftp.get(source, localpath1)
        time.sleep(timer)
    sftp.close()
    transport.close()

def show_ts2():
    transport2 = paramiko.Transport((SERVER2, port))
    transport2.connect(username=user, password=passs)
    sftp2 = paramiko.SFTPClient.from_transport(transport2)
    while True:
        sftp2.get(source, localpath2)
        time.sleep(timer)
    sftp2.close()
    transport2.close()

ani = animation.FuncAnimation(fig, animate, interval=1000)
ani1 = animation.FuncAnimation(fig, animate_scale, interval=1000)
ani2 = animation.FuncAnimation(fig, animate_scale2, interval=1000)

the_process1 = threading.Thread(target=run_sh1, args=())
the_process1.start()
the_process2 = threading.Thread(target=run_sh2, args=())
the_process2.start()
the_process3 = threading.Thread(target=show_ts1, args=())
the_process3.start()
the_process4 = threading.Thread(target=show_ts2, args=())
the_process4.start()
the_process5 = threading.Thread(target=plt.show(), args=())
the_process5.start()
the_process1.join()
the_process2.join()
the_process3.join()
the_process4.join()
the_process5.join()
