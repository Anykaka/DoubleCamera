#!/bin/bash
cd /sys/class/pwm/pwmchip1/
echo 0 > export
cd pwm0/
echo 10000 > period
echo 5000 > duty_cycle
echo 1 >enable
