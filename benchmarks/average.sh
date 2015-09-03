#!/bin/bash

COUNTER=0
WDIR=$PWD
while [ $COUNTER -lt 10 ]; do

        echo $WDIR
	$( ./ndpiReader -i test.pcap >> $WDIR/log.txt )
        let COUNTER=COUNTER+1
        echo "Run number: $COUNTER"
       
done

 $( cat $WDIR/log.txt | grep "nDPI throughput" >> $WDIR/result.txt )
 
   $( echo "Average Results for 10 runs :" >> $WDIR/result.txt )
 
 $( cat $WDIR/result.txt | awk ' { sum+=$7} END {print sum/10 " Gb/sec" }' >> $WDIR/result.txt )
