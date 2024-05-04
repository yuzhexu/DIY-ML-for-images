#!/bin/bash

python3 run.py &
python3 worker.py
wait
