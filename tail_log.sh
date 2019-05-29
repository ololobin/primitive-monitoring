# !/bin/bash
trap "kill 0" EXIT
WATCHFILE="log.txt" #just to start
ERROR_STR=50 #– max errors
ERROR_NOW=""
ERR="(\sE\s\[)" #look for " E "
MASK='ext*.log'
OCTA='172.10.' #first octets witch are same on all of your server where this *.sh would be put.
#MAIL TIME!
recipients='mail@mail.com' #–past mail
SERVER=$(ip addr show | grep $OCTA | awk '{print  $2;}') #get ip

while (true)
do
NEWFILE=$(ls -t $MASK | head -n 1)
if [ "$NEWFILE" != "$WATCHFILE" ]; then
            ERROR_NOW=$(grep -E $ERR $WATCHFILE | wc -l) # 1>/dev/null
            if [ "$ERROR_NOW" -gt "$ERROR_STR" ]; then # if a lot of errors
                        echo -e "\e[31;5mALARM\e[0m" $ERROR_NOW ERRORS HAVE BEEN FOUND !!! #– console attention
                        /usr/sbin/sendmail $recipients << EOF #and send mail
Subject: ALERT TS ERRORS!!!
$ERROR_NOW errors in $WATCHFILE 
$SERVER
$(date "+%A %e %b %Y %T")
EOF
            fi

lol=$(ps -e l | grep $WATCHFILE | awk '{print  $3;}') #pid of tail for old WATCHFILE
kill -9  $lol 2>/dev/null
WATCHFILE=$NEWFILE
fi
tail -f $WATCHFILE | grep --color=auto -E $ERR & #pid of child process
GREPPID=$!
sleep 5
kill -9  $GREPPID 2>/dev/null
done 2>/dev/null
