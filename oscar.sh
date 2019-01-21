#!/bin/bash
clear

function timer () {
	clear
	seconds=300; date1=$((`date +%s` + $seconds));
	while [ "$date1" -ge `date +%s` ]; do
		echo -ne "--: Time until next check: $(date -u --date @$(($date1 - `date +%s` )) +%H:%M:%S)\r";
	done
}

while :
do
	/usr/bin/python3 $PWD/main.py
	timer
done
