#!/bin/bash
RANDOM_SIZE=1024
while :;
	do prog=random-lambda.blc;
	(until (echo $(head -c $RANDOM_SIZE /dev/urandom  | xxd -b | awk '{ print $2, $3}' | sed 's/ //g')  | sed 's/ //g' > $prog; blc $prog &> /dev/null); do :; done);
	start=$(date +%s); steps=$(blc $prog --verbose | wc -l); end=$(date +%s); duration=$((end-start));
	if (( $steps > 4 ));
	then
		cat $prog; echo "steps $steps duration $duration";
	fi;
done
