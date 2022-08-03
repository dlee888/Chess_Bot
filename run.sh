#!/bin/bash

# [ -e environment ] && . ./environment

while true; do
	echo '==================================================================='
	echo '=                       Restarting                                ='
	echo '==================================================================='

	git pull

	python3 -m Chess_Bot

	(($? == 69)) && break
done
