#!/bin/bash

while true; do
	echo '==================================================================='
	echo '=                       Restarting                                ='
	echo '==================================================================='

	git pull
	make
	pip install -U -r requirements.txt
	python3 -m Chess_Bot $@

	(($? == 69)) && break
done
