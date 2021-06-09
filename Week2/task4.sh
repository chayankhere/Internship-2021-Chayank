#!/bin/bash

#TASK 4
echo "PRINT STATUS CODES RECEIVED BY EACH HOST"
awk '{ print $15 " " $7 }' access.log | sort | uniq
echo                    
