When the company has no money to buy full monitoring from a vendor, and colleagues who are not blinking, looking at "tail *.log", this code will come to the rescue. 
We have a server with an application that writes logs in *.log. 
The employees working on Windows stations.
"counterrors_TS.sh" should be put in the log directory. 
"monitoring.py" is our main file and we can make monitoring.exe for our employees.

"counterrors_TS.sh" counts the number of entries in the log file and writes it to error.txt.
"monitoring.py" downloads this file via ssh, reads lines and visualizes on two graphs.