#!/bin/bash
(time ~/Sailfish-0.6.3-Linux_x86-64/bin/sailfish quant -p 16 -i ~/Sailfish-0.6.3-Linux_x86-64/bin/index -l "T=SE:S=U" -r <(gunzip -c $1) -o $2) 2> "${2}_timing.txt"
