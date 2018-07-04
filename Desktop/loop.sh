#!/bin/bash

./main.py set-degrees 1 120
./main.py set-degrees 2 120
./main.py set-degrees 3 120

while true; do
./main.py set-degrees 1 60
sleep 0.05
./main.py set-degrees 2 60
sleep 0.05
./main.py set-degrees 1 120
sleep 0.05
./main.py set-degrees 2 60
sleep 0.05
./main.py set-degrees 3 60
sleep 0.05
./main.py set-degrees 2 120
sleep 0.05
./main.py set-degrees 3 60
sleep 0.05
./main.py set-degrees 1 60
sleep 0.05
./main.py set-degrees 3 120
sleep 0.05
done;

./main.py set-degrees 1 120
./main.py set-degrees 2 120
./main.py set-degrees 3 120
