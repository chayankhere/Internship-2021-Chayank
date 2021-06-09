#!/bin/bash



#TASK  6
echo
echo "Response time greater than 10"
echo
awk '{if ( $8 >= 10 )print $8 " -> " $9 }' access.log | sort | uniq | sort  -rn 
echo
echo "Response time greater than 5"
echo
awk '{if ( $8 >= 5 && $8 <10 )print $8 " -> " $9 }' access.log | sort | uniq | sort  -rn
echo
echo "Response time greater than 2" 
echo
awk '{if ( $8 >= 2 && $8 < 5 )print $8 " -> " $9 }' access.log | sort | uniq | sort  -rn  
echo
