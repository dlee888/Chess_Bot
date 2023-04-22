#!/bin/bash

source venv/bin/activate

nohup ./loop.sh $@ &
