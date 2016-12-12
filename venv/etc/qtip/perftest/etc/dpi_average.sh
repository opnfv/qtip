#!/bin/bash

COUNTER=0
WDIR=$PWD
while [ $COUNTER -lt 10 ]; do

        echo $WDIR
	$( ./ndpiReader -i test.pcap >> $WDIR/dpi_dump.txt )
        let COUNTER=COUNTER+1
        echo "Run number: $COUNTER"
       
done

 
