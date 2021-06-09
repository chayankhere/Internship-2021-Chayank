
#! /bin/bash

#TASK 1
printf "HIGHEST REQUESTED HOST"
awk '{print $15}' access.log |sort |uniq -c|sort -rn| head -1
printf "\n" 

echo "HIGHEST REQUESTED UPSTREAM:IP"
awk '{count[$10]++} END {for ( i in count ) print i, count[i] }' access.log | sort -n -r| head -1
echo \n

echo "MOST REQUESTED PATH"
awk '{print $5}' access.log |sort |uniq -c|sort -rn| head -1
echo \n
