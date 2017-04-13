#!/bin/bash -e

BASEDIRECTORY=`dirname $0`/..

rm -rf $BASEDIRECTORY/.tox $BASEDIRECTORY/env $BASEDIRECTORY/dist $BASEDIRECTORY/build
find $BASEDIRECTORY -name '*.pyc' -delete
echo "Deleted virtualenv"

