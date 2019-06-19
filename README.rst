====================
primitive-monitoring
====================

When the company has no money to buy full monitoring from a vendor, and colleagues who are not blinking, looking at "tail smth.log", this code will come to the rescue. 
We have 2 servers with an application that writes logs in smth.log. 
The employees working on Windows stations.
"monitoring.py" is our main file and we can make monitoring.exe for our employees.

Use:
====
* Put counterrors_TS.sh in the log directory on servers;
* Put errors.txt and alarm.mp3 in logs before 1st run;
* Run monitoring_v2.py (monitoring.exe) and login;
* Put tail_log.sh in the log directory on servers.

and

.. code-block::  python

  pip install paramiko
  pip install matplotlib
  pip install playsound

and

.. code-block:: bash

  $ /path_to_logs/tail_log.sh

Concepts
========
* "counterrors_TS.sh" counts the number of entries in the log file and writes it to error.txt;
* "monitoring_v2.py" downloads this file via ssh, reads lines, visualizes,plays "alarm.mp3" if there are a lot of errors and prints  time;
* "monitoring_v2.py" also run counterrors_TS.sh;
* "tail_log.sh" shows error strings and send mail alerts.

Configuration
=============
counterrors_TS.sh

.. code-block:: bash

  $ MASK='ext*.log' #Mask of log files
  $ ERR="(\sE\s\[)" #What to find
  $ MAXSIZE=102400 #Max size for error.txt in bytes
  $ cd /path_to_logs #paste the way to logs
  
monitoring.py

.. code-block::  python

  SERVER1='server1' #paste your server#1
  SERVER2='server2' #paste your server#2
  source='/path_to_logs/logs/errors.txt' #paste the way to logs
  cmd2='/path_to_logs/logs/counterrors_TS.sh &' #paste the way to logs
  for row in deque(f, 50): #50 means plot last 50 values
  ax.set_ylim((0, 100), auto=False) # means no autoscale and max(0Y) = 100
  plt.xlabel('') # 0X label
  plt.ylabel('Цена') # 0Y label
  plt.title('RED - 100 \n BLUE - 101') #title
  !!!new v2!!!:
  labelname=['Label1', 'Label2'] #paste your labels for legend
  plt.xlabel, plt.ylabel and plt.title has been deleted
  sound=os.path.join(os.path.abspath(os.curdir),'alarm.mp3') #alarm.mp3 is your alarm sound
  maxerrors=int(input('Enter maximum of errors: ')) #for dound alarm and 0y line
  timer = 6 #each 6 sec copy error file and check it for sound alarm
tail_log.sh

.. code-block:: bash

  $ ERROR_STR=50 #– max errors
  $ ERR="(\sE\s\[)" #look for " E ["
  $ MASK='ext*.log' #Mask of log files
  $ OCTA='172.10.' #first octets witch are same on all of your server where this *.sh would be put.
  $ recipients='mail@mail.com' #–past mail
    
Result:
=======
v2:

.. image:: https://github.com/ololobin/primitive-monitoring/blob/master/example_v2.png
.. image:: https://github.com/ololobin/primitive-monitoring/blob/master/example_tail.png
v1:

.. image:: https://github.com/ololobin/primitive-monitoring/blob/master/example.png
To create EXE
==============
.. code-block:: bash

  $ pip install pypiwin32
  $ pip install pyinstaller
  pyinstaller --onefile --icon=1.ico monitoring_v2.py
