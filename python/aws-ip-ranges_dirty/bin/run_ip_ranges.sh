#!/bin/bash -e
BASEDIR=`dirname $0`/..


source $BASEDIR/env/bin/activate

python2.7 iprange-report-ref.py
