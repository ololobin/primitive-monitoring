====================
primitive-monitoring
====================

When the company has no money to buy full monitoring from a vendor, and colleagues who are not blinking, looking at "tail smth.log", this code will come to the rescue. 
We have 2 servers with an application that writes logs in smth.log. 
The employees working on Windows stations.
"monitoring.py" is our main file and we can make monitoring.exe for our employees.

To create EXE
==============
.. code-block:: bash

  $ pip install pypiwin32
  $ pip install pyinstaller
  pyinstaller --onefile --icon=1.ico monitoring.py
  
Use:
====

* Put counterrors_TS.sh in the log directory on servers.
* Put errors.txt in logs before 1st run
* Run monitoring.py (monitoring.exe) and login.

Concepts
========
* "counterrors_TS.sh" counts the number of entries in the log file and writes it to error.txt.
* "monitoring.py" downloads this file via ssh, reads lines and visualizes on two graphs.
* "monitoring.py" also run counterrors_TS.sh

Configuration
=============
counterrors_TS.sh

.. code-block:: bash

  $ MASK='ext*.log' #Mask of log files
  $ ERR="(\sE\s\[)" #What to find
  $ MAXSIZE=204800 #Max size for error.txt in bytes
  
monitoring.py

.. code-block::  python

  SERVER1='server1' #paste your server#1
  SERVER2='server2' #paste your server#2
  source='/path_to_logs/logs/errors.txt' #paste the way to logs
  cmd2='/path_to_logs/logs/counterrors_TS.sh &' #paste the way to logs
