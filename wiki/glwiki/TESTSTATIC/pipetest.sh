#!/bin/sh

echo "Pipetest output"
echo "$1"
echo "$2"
env | sort
echo "end"
