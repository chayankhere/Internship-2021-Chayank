#!/bin/bash

#TASK 3
echo "TOP 5 MOST HOST"
awk '{print $15}' access.log |sort |uniq -c|sort -rn| head -5
echo 

echo "TOP 5 BODYBYTES"
awk '{count[$10]++} END {for ( i in count ) print i, count[i] }' access.log | sort -n -r| head -5
echo

echo "TOP 5 UPSTREAM IP: PORT"
awk '{count[$9]++} END {for ( i in count ) print i, count[i] }' access.log | sort -n -r| head -5
echo

echo "TOP 5 RESPONSE TIME"
awk '{count[$8]++} END {for ( i in count ) print i, count[i] }' access.log | sort -n -r| head -5
echo

echo "TOP 5 MOST REQUESTED PATH"
awk '{print $5}' access.log |sort |uniq -c|sort -rn| head -5
echo 
