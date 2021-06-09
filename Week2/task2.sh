#!/bin/bash

#TASK 2

echo "TOTAL REQUESTS PER STATUS CODES"
echo
echo "No. of REQUESTS        STATUS CODE"
awk '{print "               " $7}' access.log | sort | uniq -c | sort -nr                                          
echo
