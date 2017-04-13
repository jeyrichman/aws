#!/bin/bash -e
BASEDIR=`dirname $0`/..


source $BASEDIR/env/bin/activate

python3.5 ip_ranges.py
