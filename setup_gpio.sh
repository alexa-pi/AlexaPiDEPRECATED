#! /bin/bash

echo 409  | sudo tee /sys/class/gpio/export
cat /sys/class/gpio/gpio409/direction
cat /sys/class/gpio/gpio409/value
