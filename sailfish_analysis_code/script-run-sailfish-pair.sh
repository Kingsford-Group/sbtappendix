#!/bin/bash
(time ~/Sailfish-0.6.3-Linux_x86-64/bin/sailfish quant -p 16 -i ~/Sailfish-0.6.3-Linux_x86-64/bin/index -l "T=PE:S=U" -1 <(gunzip -c $1) -2 <(gunzip -c $2) -o $3) 2> "${3}_timing.txt"
