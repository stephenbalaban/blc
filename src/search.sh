#!/bin/bash
RANDOM_SIZE=127
RANDOM_OUTFILE=$1
MIN_STEPS=$2
while :;
	do
	prog=$RANDOM_OUTFILE
	(until (echo $(head -c $RANDOM_SIZE /dev/urandom  | xxd -b | awk '{ print $2, $3}' | sed 's/ //g')  | sed 's/ //g' > $prog; blc $prog &> /dev/null); do :; done);
	start=$(date +%s); steps=$(blc $prog --verbose | wc -l); end=$(date +%s); duration=$((end-start));
	if (( $steps > $MIN_STEPS ));
	then
		cat $prog; echo "steps $steps duration $duration";
	fi;
done
