# !/bin/bash
#trap "kill 0" EXIT
cd /path_to_logs #paste the way to logs
WATCHFILE=$(ls -t ext*.log | head -n 1) #in my case i am watching files with "ext*.log" mask
file=errors.txt #put errors.txt in logs before 1st run
maxsize=204800 #200KB
while (true)
do
    actualsize=$(wc -c <"$file")
    NEWFILE=$(ls -t ext*.log | head -n 1)
    if [ "$NEWFILE" != "$WATCHFILE" ]; then #New log file
        grep -E "(\sE\s\[)" $WATCHFILE | wc -l >> $file #in my case i am checking " E "
        if [ $actualsize -ge $maxsize ]; then #if size(errors.txt)>200KB
            sed -i '1,10000d' $file #cut first 10000 raws
        fi
        WATCHFILE=$NEWFILE #watching new ext*.log
    fi
sleep 5
done 2>/dev/null #wipe all errors
